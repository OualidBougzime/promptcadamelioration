# PromptToSTL

Generate 3D models (STL/STEP) from natural language descriptions. The system uses a multi-agent architecture with local LLMs (Ollama) to transform text into executable CAD code.

## Features

### Optimized Templates (8 types)
Ultra-fast generation (~2s) for common types:
- **Medical**: splints (orthoses), cardiovascular stents
- **Mechanical**: heat sinks, robotic grippers
- **Architecture**: parametric facades, honeycomb structures
- **Structures**: lattices, parametric geometries

### Universal Generation (Chain-of-Thought)
For everything not in templates (~20s):
- Gears, screws, nuts
- Supports, brackets, adapters
- Housings, enclosures
- Connectors, joints
- **Any describable shape**

## Architecture

### 12 Specialized Agents

**Base Agents** (3)
- `AnalystAgent`: Detects type and extracts parameters
- `GeneratorAgent`: Generates code from templates
- `ValidatorAgent`: Executes and validates code

**Multi-Agent Agents** (6)
- `OrchestratorAgent`: Coordinates entire pipeline + intelligent routing
- `DesignExpertAgent`: Validates business rules (Qwen2.5-Coder 7B)
- `ConstraintValidatorAgent`: Checks manufacturing constraints
- `SyntaxValidatorAgent`: Validates Python syntax before execution
- `ErrorHandlerAgent`: Categorizes and handles errors
- `SelfHealingAgent`: Automatically corrects code (DeepSeek-Coder 6.7B)

**Chain-of-Thought Agents** (3)
- `ArchitectAgent`: Analyzes and reasons about design (Qwen2.5 14B)
- `PlannerAgent`: Creates construction plan (Qwen2.5-Coder 14B)
- `CodeSynthesizerAgent`: Generates final code (DeepSeek-Coder 33B)

### Intelligent Routing

```
User prompt
    ↓
Analyst Agent detects type
    ↓
    ├─ Known type → Template (2s, local)
    └─ Unknown type → Chain-of-Thought (20s, local)
```

## Installation

> 📚 **Detailed Guides Available**:
> - **[INSTALL_OLLAMA.md](INSTALL_OLLAMA.md)** - Complete Ollama installation guide (recommended for beginners)
> - **[verify_ollama.sh](verify_ollama.sh)** - Automatic installation verification script
> - **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Troubleshooting common errors
> - **[TEST_LLM.md](TEST_LLM.md)** - Tests and use cases

### Prerequisites
- Python 3.10+
- Ollama
- 16-32 GB RAM (depending on models)

### 1. Install Ollama

**Quick guide** - Download from [ollama.ai](https://ollama.ai)

**Complete guide** - See [INSTALL_OLLAMA.md](INSTALL_OLLAMA.md) for detailed instructions

### 2. Download Models

**Standard configuration (32GB RAM)**:
```bash
ollama pull qwen2.5-coder:7b
ollama pull deepseek-coder:6.7b
ollama pull qwen2.5:14b
ollama pull qwen2.5-coder:14b
ollama pull deepseek-coder:33b
```

**Lightweight configuration (16GB RAM)**:
```bash
ollama pull qwen2.5-coder:7b
ollama pull deepseek-coder:6.7b
ollama pull qwen2.5:7b
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configuration

Copy `.env.example` to `.env` and adjust if needed:

```bash
# Ollama
OLLAMA_BASE_URL=http://localhost:11434

# Models for multi-agent agents
DESIGN_EXPERT_MODEL=qwen2.5-coder:7b
CODE_LLM_MODEL=deepseek-coder:6.7b

# Models for Chain-of-Thought
COT_ARCHITECT_MODEL=qwen2.5:14b
COT_PLANNER_MODEL=qwen2.5-coder:14b
COT_SYNTHESIZER_MODEL=deepseek-coder:33b
```

### 5. Launch the Application

```bash
# Terminal 1: Ollama
ollama serve

# Terminal 2: Backend
cd backend
python main.py

# Terminal 3: Frontend (optional)
cd frontend
python -m http.server 3000
```

The API will be available at `http://localhost:8000`

## Usage

### REST API

**Main endpoint**: `POST /api/generate`

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "create a gear with 20 teeth"}'
```

**Response** (Server-Sent Events):
```json
{"type": "status", "message": "Analyzing...", "progress": 10}
{"type": "code", "code": "import cadquery as cq\n...", "progress": 70}
{"type": "complete", "mesh": {...}, "stl_path": "output/gear.stl"}
```

**Download files**:
- STL: `GET /api/export/stl`
- STEP: `GET /api/export/step`

### Web Interface

Open `http://localhost:3000` in your browser.

### Examples

```python
# Medical orthosis (template)
{
  "prompt": "create a wrist splint 270mm long, 70mm wide, 3.5mm thick"
}

# Gear (Chain-of-Thought)
{
  "prompt": "create a gear with 20 teeth, 50mm diameter, 10mm thick"
}

# Custom support (Chain-of-Thought)
{
  "prompt": "create a camera mount bracket for 1/4 inch screw"
}

# Simple shape (Chain-of-Thought)
{
  "prompt": "create a cube 50mm"
}
```

### 🚀 Batch Runner - Automatic Execution

Automatically execute multiple CAD prompts with logs and result saving:

```bash
# Simple method (recommended)
./run_batch.sh

# Or directly with Python
python3 batch_runner.py

# With custom prompts file
python3 batch_runner.py my_prompts.json
```

**Features**:
- ✅ Sequential execution of all prompts
- 📝 Complete logs for each prompt
- 💾 Save generated Python code
- 📊 JSON report with results and metrics
- ⏱️ Execution time measurement

**Customization**: Edit `prompts.json` to add your own prompts:

```json
{
  "prompts": [
    {
      "id": 1,
      "name": "My Object",
      "enabled": true,
      "prompt": "Create a custom object..."
    }
  ]
}
```

**Results**: All files are saved in `batch_results/`:
- `batch_run_*.log` - Complete execution logs
- `batch_results_*.json` - Structured results with all details
- `prompt_*_code.py` - Generated Python code for each prompt
- STL files in `backend/output/`

See [BATCH_README.md](BATCH_README.md) for complete documentation.

## Performance

| Type | Time | Cost | Mode |
|------|------|------|------|
| Template | 1-2s | $0 | Local |
| CoT Simple | 12-15s | $0 | Local |
| CoT Medium | 18-22s | $0 | Local |
| CoT Complex | 25-35s | $0 | Local |

*Times with 14B/33B models on CPU. 2-3x faster with GPU.*

## Advantages

- ✅ **100% Free** - No API fees, open-source models
- ✅ **100% Local** - No internet connection required (after setup)
- ✅ **100% Private** - Your data stays on your machine
- ✅ **Unlimited** - No quotas, no rate limiting
- ✅ **Flexible** - Generates any 3D shape

## Technologies

- **Backend**: FastAPI, Python 3.10+
- **CAD**: CadQuery 2.4
- **LLMs**: Ollama (Qwen2.5, DeepSeek-Coder)
- **Export**: STL, STEP

## Documentation

### Architecture and System
- [COT_SYSTEM.md](COT_SYSTEM.md) - Chain-of-Thought system documentation
- [MULTI_AGENT_SYSTEM.md](MULTI_AGENT_SYSTEM.md) - Detailed multi-agent architecture

### Installation and Configuration
- [INSTALL_OLLAMA.md](INSTALL_OLLAMA.md) - Complete Ollama installation guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common troubleshooting
- [TEST_LLM.md](TEST_LLM.md) - Tests and LLM system validation

## Troubleshooting

**Ollama not accessible**
```bash
# Check that Ollama is running
ollama serve

# Test
curl http://localhost:11434/api/tags
```

**Model not found**
```bash
ollama pull qwen2.5:14b
```

**Insufficient memory**

Use 7B models in `.env`:
```bash
COT_ARCHITECT_MODEL=qwen2.5:7b
COT_PLANNER_MODEL=qwen2.5-coder:7b
COT_SYNTHESIZER_MODEL=deepseek-coder:6.7b
```

**Generation too slow**

- Use a GPU (2-3x faster)
- Switch to 7B models
- Close other applications

## Contributing

Contributions are welcome!

1. Fork the repo
2. Create your branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Authors

- Initial development and multi-agent architecture

## Acknowledgments

- [CadQuery](https://github.com/CadQuery/cadquery) for the CAD engine
- [Ollama](https://ollama.ai) for local LLM infrastructure
- [Qwen](https://github.com/QwenLM/Qwen) and [DeepSeek](https://github.com/deepseek-ai/DeepSeek-Coder) for open-source models
