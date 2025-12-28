#!/usr/bin/env python3
"""
CADAM-X Benchmark System
Tests multiple LLM models and prompting strategies for CAD code generation.
"""

import json
import time
import subprocess
import requests
from pathlib import Path
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass, asdict
import re

# ============================================================================
# CONFIGURATION
# ============================================================================

# Backend configuration
BACKEND_URL = 'http://localhost:8000'
BACKEND_TIMEOUT = 180  # 3 minutes timeout

# Models to test (local Ollama models)
MODELS = [
    'codellama:7b',
    'deepseek-coder:6.7b',
    'qwen2.5-coder:7b',
    'qwen2.5-coder:14b',
    'mistral:7b'
]

# Prompting approaches to test
APPROACHES = [
    'zero-shot',
    'one-shot',
    'few-shot-2',
    'few-shot-3',
    'cot',
    'multi-agent'  # Uses your existing backend
]

# Test suite selection
TEST_SUITE = 'simple_medium'  # Options: quick_test, simple_only, medium_only, complex_only, simple_medium, full_benchmark

# Output directory
RESULTS_DIR = Path('./results')
RESULTS_DIR.mkdir(exist_ok=True)

# ============================================================================
# FEW-SHOT EXAMPLES
# ============================================================================

EXAMPLE_PIPE = """
# Example: Pipe with chamfers
import cadquery as cq

outer_radius = 20
inner_radius = 15
length = 150
chamfer = 1

result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
    .faces(">Z")
    .chamfer(chamfer)
    .faces("<Z")
    .chamfer(chamfer)
)
"""

EXAMPLE_GLASS = """
# Example: Glass with hollow interior
import cadquery as cq

diameter = 60
height = 100
bottom_thickness = 3
wall_thickness = 2

result = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .circle((diameter / 2) - wall_thickness)
    .cutBlind(-(height - bottom_thickness))
    .edges(">Z")
    .fillet(1)
)
"""

EXAMPLE_SCREW = """
# Example: Screw with hex head
import cadquery as cq

shaft_radius = 4
shaft_length = 50
head_diameter = 12
head_height = 5

shaft = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(shaft_length)
)

head = (
    cq.Workplane("XY")
    .polygon(6, head_diameter)
    .extrude(head_height)
)

result = shaft.union(head.translate((0, 0, shaft_length)))
"""

# ============================================================================
# PROMPT BUILDERS
# ============================================================================

def build_zero_shot_prompt(prompt: str) -> str:
    """Simple prompt without examples"""
    return f"""Generate CadQuery Python code for this CAD model:

{prompt}

Requirements:
- Use CadQuery API only
- Store final shape in variable named 'result'
- Include necessary imports
- Use parametric dimensions when possible"""


def build_one_shot_prompt(prompt: str) -> str:
    """Prompt with one example"""
    return f"""Generate CadQuery Python code for this CAD model.

{EXAMPLE_PIPE}

Now generate code for this prompt:
{prompt}

Requirements:
- Follow the example style
- Store final shape in 'result' variable
- Use CadQuery API only"""


def build_few_shot_prompt(prompt: str, num_examples: int = 2) -> str:
    """Prompt with 2 or 3 examples"""
    examples = [EXAMPLE_PIPE, EXAMPLE_GLASS]
    if num_examples >= 3:
        examples.append(EXAMPLE_SCREW)
    
    examples_text = "\n\n".join(examples)
    
    return f"""Generate CadQuery Python code based on these examples:

{examples_text}

Now generate code for this prompt:
{prompt}

Requirements:
- Follow the examples' patterns
- Store final shape in 'result' variable
- Use CadQuery API methods shown in examples"""


def build_cot_prompt(prompt: str) -> str:
    """Chain-of-Thought prompt"""
    return f"""Generate CadQuery Python code for this CAD model using step-by-step reasoning:

{prompt}

Think through this in steps:
1. What are the main geometric features needed?
2. What CadQuery methods should be used?
3. In what order should operations be applied?
4. What are the key dimensions and parameters?
5. How should the code be structured?

Then generate the complete CadQuery code with 'result' variable."""


# ============================================================================
# BACKEND INTERFACE
# ============================================================================

def call_backend_sse(prompt: str, timeout: int = BACKEND_TIMEOUT) -> Dict[str, Any]:
    """
    Call the CADAM-X backend via SSE endpoint.
    Parses the streaming response to get final code and metadata.
    """
    try:
        url = f"{BACKEND_URL}/api/generate"
        
        response = requests.post(
            url,
            json={"prompt": prompt},
            headers={"Content-Type": "application/json"},
            stream=True,
            timeout=timeout
        )
        
        if response.status_code != 200:
            return {
                'success': False,
                'code': '',
                'generation_time': 0,
                'tokens_input': 0,
                'tokens_output': 0,
                'error': f"HTTP {response.status_code}: {response.reason}"
            }
        
        # Parse SSE stream
        code = ''
        execution_time = 0
        success = False
        errors = []
        
        start_time = time.time()
        buffer = ''
        
        for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
            if chunk:
                buffer += chunk
                lines = buffer.split('\n')
                buffer = lines.pop() if lines else ''
                
                for line in lines:
                    if not line.strip() or not line.startswith('data: '):
                        continue
                    
                    data_str = line[6:]  # Remove 'data: ' prefix
                    
                    try:
                        data = json.loads(data_str)
                        
                        if data.get('type') == 'code':
                            code = decode_escaped_string(data.get('code', ''))
                        
                        elif data.get('type') == 'complete':
                            success = data.get('success', False)
                            if data.get('code'):
                                code = data.get('code')
                            execution_time = data.get('execution_time', 0)
                            if not success:
                                errors = data.get('errors', [])
                        
                        elif data.get('type') == 'error':
                            success = False
                            errors = data.get('errors', [])
                            execution_time = data.get('execution_time', 0)
                    
                    except json.JSONDecodeError:
                        continue
        
        generation_time = time.time() - start_time
        
        return {
            'success': success and bool(code),
            'code': code,
            'generation_time': generation_time,
            'tokens_input': 0,  # Backend doesn't expose this
            'tokens_output': 0,
            'execution_time': execution_time,
            'error': ', '.join(errors) if errors else None
        }
    
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'code': '',
            'generation_time': timeout,
            'tokens_input': 0,
            'tokens_output': 0,
            'error': 'Request timeout'
        }
    except Exception as e:
        return {
            'success': False,
            'code': '',
            'generation_time': 0,
            'tokens_input': 0,
            'tokens_output': 0,
            'error': str(e)
        }


def decode_escaped_string(s: str) -> str:
    """Decode escaped strings from SSE"""
    if not s:
        return s
    return s.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')


# ============================================================================
# OLLAMA INTERFACE (for non-multi-agent approaches)
# ============================================================================

OLLAMA_URL = 'http://localhost:11434'

def call_ollama(model: str, prompt: str, timeout: int = 120) -> Dict[str, Any]:
    """Call Ollama API to generate code"""
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "num_predict": 2048
                }
            },
            timeout=timeout
        )
        
        if response.status_code != 200:
            return {
                'success': False,
                'code': '',
                'generation_time': 0,
                'tokens_input': 0,
                'tokens_output': 0,
                'error': f"Ollama HTTP {response.status_code}"
            }
        
        result = response.json()
        generation_time = time.time() - start_time
        
        # Extract code from markdown
        text = result.get('response', '')
        code = extract_code_from_markdown(text)
        
        return {
            'success': bool(code),
            'code': code,
            'generation_time': generation_time,
            'tokens_input': result.get('prompt_eval_count', 0),
            'tokens_output': result.get('eval_count', 0)
        }
    
    except Exception as e:
        return {
            'success': False,
            'code': '',
            'generation_time': 0,
            'tokens_input': 0,
            'tokens_output': 0,
            'error': str(e)
        }


def extract_code_from_markdown(text: str) -> str:
    """Extract Python code from markdown blocks"""
    # Try to find code between ```python and ```
    pattern = r'```(?:python)?\s*(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    if matches:
        return matches[0].strip()
    
    # If no markdown blocks, return as-is if it looks like Python
    if 'import' in text and 'result' in text:
        return text.strip()
    
    return ''


# ============================================================================
# CODE EXECUTION
# ============================================================================

def execute_cadquery_code(code: str, output_stl: Path) -> Dict[str, Any]:
    """Execute CadQuery code and export STL"""
    
    # Create temporary Python file
    temp_file = RESULTS_DIR / 'temp_exec.py'
    
    wrapped_code = f"""
{code}

# Export STL
import cadquery as cq
if 'result' in locals() and result is not None:
    cq.exporters.export(result, '{output_stl}')
else:
    raise ValueError("No 'result' variable found in code")
"""
    
    temp_file.write_text(wrapped_code)
    
    try:
        start_time = time.time()
        
        result = subprocess.run(
            ['python3', str(temp_file)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        execution_time = time.time() - start_time
        
        if result.returncode == 0 and output_stl.exists():
            stl_size = output_stl.stat().st_size / 1024  # KB
            return {
                'success': True,
                'execution_time': execution_time,
                'stl_size_kb': stl_size,
                'error': None
            }
        else:
            return {
                'success': False,
                'execution_time': execution_time,
                'stl_size_kb': 0,
                'error': result.stderr or 'Execution failed'
            }
    
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'execution_time': 60,
            'stl_size_kb': 0,
            'error': 'Execution timeout'
        }
    except Exception as e:
        return {
            'success': False,
            'execution_time': 0,
            'stl_size_kb': 0,
            'error': str(e)
        }
    finally:
        if temp_file.exists():
            temp_file.unlink()


# ============================================================================
# METRICS CALCULATION
# ============================================================================

class MetricsCalculator:
    """Calculate code quality and correctness metrics"""
    
    @staticmethod
    def calculate_code_metrics(code: str) -> Dict[str, Any]:
        """Calculate code-level metrics"""
        lines = [l for l in code.split('\n') if l.strip() and not l.strip().startswith('#')]
        
        # Count API method calls
        api_methods = re.findall(r'\.(\w+)\(', code)
        
        # Detect hallucinations (common non-existent methods)
        hallucinations = []
        invalid_methods = ['smoothEdges', 'blend', 'createBox', 'makeCylinder', 'createSphere']
        for method in api_methods:
            if method in invalid_methods:
                hallucinations.append(method)
        
        return {
            'lines_of_code': len(lines),
            'api_methods_count': len(api_methods),
            'hallucination_count': len(hallucinations),
            'hallucination_list': list(set(hallucinations))
        }
    
    @staticmethod
    def check_geometric_correctness(code: str, prompt: str) -> bool:
        """Check if code implements expected geometric features"""
        prompt_lower = prompt.lower()
        code_lower = code.lower()
        
        # Check for expected operations based on prompt keywords
        checks = {
            'circle': 'circle(' in code_lower,
            'cylinder': 'circle(' in code_lower and 'extrude(' in code_lower,
            'box': 'box(' in code_lower or 'rect(' in code_lower,
            'fillet': 'fillet(' in code_lower if 'fillet' in prompt_lower else True,
            'chamfer': 'chamfer(' in code_lower if 'chamfer' in prompt_lower else True,
            'hole': 'hole(' in code_lower or 'cutblind' in code_lower if 'hole' in prompt_lower else True,
        }
        
        # Return True if all applicable checks pass
        return all(checks.values())


# ============================================================================
# BENCHMARK RUNNER
# ============================================================================

@dataclass
class TestResult:
    """Single test result"""
    approach: str
    model: str
    test: str
    complexity: str
    success: bool
    first_try_success: bool
    generation_time: float
    execution_time: float
    total_time: float
    tokens_input: int
    tokens_output: int
    tokens_total: int
    lines_of_code: int
    api_methods_count: int
    hallucination_count: int
    hallucination_list: List[str]
    geometric_correct: bool
    stl_path: str
    code_path: str
    stl_size_kb: float
    error: str = None


class BenchmarkRunner:
    """Main benchmark orchestrator"""
    
    def __init__(self, prompts_file: Path):
        with open(prompts_file, 'r') as f:
            self.prompts_data = json.load(f)
        
        self.results: List[TestResult] = []
    
    def run_single_test(
        self,
        approach: str,
        model: str,
        test_case: Dict[str, Any]
    ) -> TestResult:
        """Run a single test case"""
        
        test_name = test_case['name']
        prompt_text = test_case['prompt']
        complexity = test_case['complexity']
        
        print(f"  → {approach} | {model} | {test_name}")
        
        # Build prompt based on approach
        if approach == 'multi-agent':
            # Use backend directly (it implements multi-agent)
            final_prompt = prompt_text
        elif approach == 'zero-shot':
            final_prompt = build_zero_shot_prompt(prompt_text)
        elif approach == 'one-shot':
            final_prompt = build_one_shot_prompt(prompt_text)
        elif approach == 'few-shot-2':
            final_prompt = build_few_shot_prompt(prompt_text, num_examples=2)
        elif approach == 'few-shot-3':
            final_prompt = build_few_shot_prompt(prompt_text, num_examples=3)
        elif approach == 'cot':
            final_prompt = build_cot_prompt(prompt_text)
        else:
            final_prompt = prompt_text
        
        # Generate code
        if approach == 'multi-agent':
            # Use backend (multi-agent system)
            gen_result = call_backend_sse(final_prompt)
        else:
            # Use Ollama with specific prompting strategy
            gen_result = call_ollama(model, final_prompt)
        
        if not gen_result['success']:
            return TestResult(
                approach=approach,
                model=model,
                test=test_name,
                complexity=complexity,
                success=False,
                first_try_success=False,
                generation_time=gen_result['generation_time'],
                execution_time=0,
                total_time=gen_result['generation_time'],
                tokens_input=gen_result.get('tokens_input', 0),
                tokens_output=gen_result.get('tokens_output', 0),
                tokens_total=gen_result.get('tokens_input', 0) + gen_result.get('tokens_output', 0),
                lines_of_code=0,
                api_methods_count=0,
                hallucination_count=0,
                hallucination_list=[],
                geometric_correct=False,
                stl_path='',
                code_path='',
                stl_size_kb=0,
                error=gen_result.get('error', 'Code generation failed')
            )
        
        code = gen_result['code']
        
        # Calculate code metrics
        metrics = MetricsCalculator.calculate_code_metrics(code)
        geometric_correct = MetricsCalculator.check_geometric_correctness(code, prompt_text)
        
        # Save code
        approach_dir = RESULTS_DIR / approach / model.replace(':', '-')
        approach_dir.mkdir(parents=True, exist_ok=True)
        
        code_path = approach_dir / f"{test_name}.py"
        code_path.write_text(code, encoding='utf-8')
        
        # Execute code
        stl_path = approach_dir / f"{test_name}.stl"
        exec_result = execute_cadquery_code(code, stl_path)
        
        total_time = gen_result['generation_time'] + exec_result['execution_time']
        
        return TestResult(
            approach=approach,
            model=model,
            test=test_name,
            complexity=complexity,
            success=exec_result['success'],
            first_try_success=exec_result['success'],
            generation_time=gen_result['generation_time'],
            execution_time=exec_result['execution_time'],
            total_time=total_time,
            tokens_input=gen_result.get('tokens_input', 0),
            tokens_output=gen_result.get('tokens_output', 0),
            tokens_total=gen_result.get('tokens_input', 0) + gen_result.get('tokens_output', 0),
            lines_of_code=metrics['lines_of_code'],
            api_methods_count=metrics['api_methods_count'],
            hallucination_count=metrics['hallucination_count'],
            hallucination_list=metrics['hallucination_list'],
            geometric_correct=geometric_correct,
            stl_path=str(stl_path) if exec_result['success'] else '',
            code_path=str(code_path),
            stl_size_kb=exec_result['stl_size_kb'],
            error=exec_result.get('error')
        )
    
    def run_benchmark(self):
        """Run full benchmark"""
        
        # Check backend availability
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=5)
            print(f"✅ Backend available at {BACKEND_URL}")
        except:
            print(f"⚠️  Backend not available at {BACKEND_URL}")
            print("   Starting backend is recommended for multi-agent approach")
        
        # Check Ollama availability
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
            print(f"✅ Ollama available at {OLLAMA_URL}")
        except:
            print(f"⚠️  Ollama not available at {OLLAMA_URL}")
            print("   Please start Ollama for non-multi-agent approaches")
        
        # Select test cases based on TEST_SUITE
        all_tests = self.prompts_data['prompts']
        
        # Get test suite definition from JSON if available
        if TEST_SUITE in self.prompts_data.get('test_suites', {}):
            suite_def = self.prompts_data['test_suites'][TEST_SUITE]
            suite_names = suite_def['prompts']
            tests = [t for t in all_tests if t['name'] in suite_names and t.get('enabled', True)]
        elif TEST_SUITE == 'simple_only':
            tests = [t for t in all_tests if t['complexity'] == 'simple' and t.get('enabled', True)]
        elif TEST_SUITE == 'medium_only':
            tests = [t for t in all_tests if t['complexity'] == 'medium' and t.get('enabled', True)]
        elif TEST_SUITE == 'complex_only':
            tests = [t for t in all_tests if t['complexity'] == 'complex' and t.get('enabled', True)]
        elif TEST_SUITE == 'simple_medium':
            tests = [t for t in all_tests if t['complexity'] in ['simple', 'medium'] and t.get('enabled', True)]
        else:  # full_benchmark or unknown
            tests = [t for t in all_tests if t.get('enabled', True)]
        
        total_tests = len(APPROACHES) * len(MODELS) * len(tests)
        current_test = 0
        
        print(f"\n{'='*60}")
        print(f"BENCHMARK: {TEST_SUITE}")
        print(f"Tests: {len(tests)} | Approaches: {len(APPROACHES)} | Models: {len(MODELS)}")
        print(f"Total: {total_tests} tests")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        
        for approach in APPROACHES:
            print(f"\n📊 Approach: {approach}")
            
            # Skip multi-agent if not using backend
            if approach == 'multi-agent':
                try:
                    requests.get(f"{BACKEND_URL}/", timeout=2)
                except:
                    print(f"   ⚠️  Skipping (backend not available)")
                    continue
            
            for model in MODELS:
                print(f"\n  🤖 Model: {model}")
                
                for test_case in tests:
                    current_test += 1
                    progress = (current_test / total_tests) * 100
                    
                    print(f"  [{current_test}/{total_tests}] ({progress:.1f}%)", end=' ')
                    
                    result = self.run_single_test(approach, model, test_case)
                    self.results.append(result)
                    
                    status = "✅" if result.success else "❌"
                    print(f"{status} ({result.total_time:.1f}s)")
        
        total_time = time.time() - start_time
        
        print(f"\n{'='*60}")
        print(f"✅ Benchmark complete!")
        print(f"Total time: {total_time/60:.1f} minutes")
        print(f"{'='*60}\n")
        
        # Generate reports
        self.generate_reports(total_time)
    
    def generate_reports(self, total_time: float):
        """Generate summary reports"""
        
        # Save detailed JSON
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        json_path = RESULTS_DIR / f"benchmark_detailed_{timestamp}.json"
        
        results_dict = [asdict(r) for r in self.results]
        with open(json_path, 'w') as f:
            json.dump({
                'config': {
                    'test_suite': TEST_SUITE,
                    'models': MODELS,
                    'approaches': APPROACHES,
                    'total_tests': len(self.results),
                    'total_time': total_time
                },
                'results': results_dict
            }, f, indent=2)
        
        print(f"📄 Detailed results: {json_path}")
        
        # Save CSV summary
        csv_path = RESULTS_DIR / f"benchmark_summary_{timestamp}.csv"
        
        with open(csv_path, 'w') as f:
            f.write("approach,model,test,complexity,success,first_try,gen_time,exec_time,total_time,tokens_in,tokens_out,loc,halluc,geo_correct\n")
            for r in self.results:
                f.write(f"{r.approach},{r.model},{r.test},{r.complexity},{r.success},{r.first_try_success},"
                       f"{r.generation_time:.2f},{r.execution_time:.2f},{r.total_time:.2f},"
                       f"{r.tokens_input},{r.tokens_output},{r.lines_of_code},"
                       f"{r.hallucination_count},{r.geometric_correct}\n")
        
        print(f"📊 CSV summary: {csv_path}")
        
        # Print summary tables
        print("\n" + "="*80)
        print("📊 RESULTS BY APPROACH & MODEL")
        print("="*80)
        
        # Group by approach and model
        summary = {}
        for r in self.results:
            key = (r.approach, r.model)
            if key not in summary:
                summary[key] = {
                    'total': 0,
                    'success': 0,
                    'first_try': 0,
                    'time': 0,
                    'tokens': 0,
                    'loc': 0,
                    'halluc': 0
                }
            
            s = summary[key]
            s['total'] += 1
            s['success'] += 1 if r.success else 0
            s['first_try'] += 1 if r.first_try_success else 0
            s['time'] += r.total_time
            s['tokens'] += r.tokens_total
            s['loc'] += r.lines_of_code
            s['halluc'] += r.hallucination_count
        
        # Print table
        print(f"{'Approach':<15} {'Model':<20} {'Success':>8} {'1st-Try':>8} {'Time(s)':>8} {'Tokens':>8} {'LoC':>6} {'Halluc':>7}")
        print("-" * 80)
        
        for (approach, model), stats in sorted(summary.items()):
            success_rate = (stats['success'] / stats['total']) * 100
            first_try_rate = (stats['first_try'] / stats['total']) * 100
            avg_time = stats['time'] / stats['total']
            avg_tokens = stats['tokens'] / stats['total'] if stats['tokens'] > 0 else 0
            avg_loc = stats['loc'] / stats['total']
            
            print(f"{approach:<15} {model:<20} {success_rate:>7.1f}% {first_try_rate:>7.1f}% "
                  f"{avg_time:>8.1f} {avg_tokens:>8.0f} {avg_loc:>6.0f} {stats['halluc']:>7}")
        
        # Print by complexity
        print("\n" + "="*80)
        print("📊 RESULTS BY COMPLEXITY")
        print("="*80)
        
        complexity_stats = {}
        for r in self.results:
            comp = r.complexity
            if comp not in complexity_stats:
                complexity_stats[comp] = {'total': 0, 'success': 0, 'time': 0}
            
            complexity_stats[comp]['total'] += 1
            complexity_stats[comp]['success'] += 1 if r.success else 0
            complexity_stats[comp]['time'] += r.total_time
        
        print(f"{'Complexity':<15} {'Success Rate':>15} {'Avg Time(s)':>15}")
        print("-" * 45)
        
        for comp, stats in sorted(complexity_stats.items()):
            success_rate = (stats['success'] / stats['total']) * 100
            avg_time = stats['time'] / stats['total']
            print(f"{comp:<15} {success_rate:>14.1f}% {avg_time:>15.1f}")
        
        # Best performers
        print("\n" + "="*80)
        print("🏆 TOP PERFORMERS")
        print("="*80)
        
        # Sort by success rate
        approach_success = {}
        for (approach, model), stats in summary.items():
            success_rate = (stats['success'] / stats['total']) * 100
            approach_success[f"{approach} + {model}"] = success_rate
        
        print("\n🥇 Best Success Rates:")
        for combo, rate in sorted(approach_success.items(), key=lambda x: x[1], reverse=True)[:3]:
            print(f"   {combo}: {rate:.1f}%")
        
        # Fastest successful tests
        successful_tests = [r for r in self.results if r.success]
        if successful_tests:
            print("\n⚡ Fastest Successful Tests:")
            for r in sorted(successful_tests, key=lambda x: x.total_time)[:5]:
                print(f"   {r.approach} + {r.model} on {r.test}: {r.total_time:.1f}s")
        
        print(f"\n{'='*80}")
        print(f"Total benchmark time: {total_time/60:.1f} minutes")
        print(f"{'='*80}\n")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main benchmark execution"""
    
    prompts_file = Path('./prompts.json')
    
    if not prompts_file.exists():
        print(f"❌ Error: {prompts_file} not found!")
        print("   Please create prompts.json first")
        return
    
    runner = BenchmarkRunner(prompts_file)
    runner.run_benchmark()


if __name__ == '__main__':
    main()