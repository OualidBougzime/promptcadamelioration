import re, math, os, logging
import builtins as py_builtins
from typing import Dict, Any, List, Optional
from templates import CodeTemplates

log = logging.getLogger("cadamx.agents")


class AnalystAgent:
    """Detects application type and extracts parameters"""

    APPLICATION_KEYWORDS = {
        'splint': ['splint', 'orthosis', 'orthèse', 'brace', 'hand', 'wrist', 'forearm', 'finger'],
        'stent': ['stent', 'vascular', 'serpentine', 'expandable', 'coronary', 'renal', 'artery'],  # Added medical stent keywords
        'facade_pyramid': ['pyramid facade', 'hexagonal pyramid', 'triangle pyramid', 'pyramidal'],  # Removed generic 'hub'
        'honeycomb': ['honeycomb panel', 'alveolar', 'hexagonal cells', 'hex panel', 'cellular panel'],  # More specific
        'louvre_wall': ['louvre', 'louver', 'slat', 'diagonal', 'pavilion', 'lattice wall'],
        'sine_wave_fins': ['sine', 'wave', 'fins', 'undulating', 'ribbed', 'zahner'],
        'gripper': ['gripper', 'surgical gripper', 'medical gripper'],  # Very restricted - no generic 'arm', 'clamp', 'holder'
        'heatsink': ['heatsink', 'heat sink', 'cooling fins', 'thermal dissipator', 'radiator'],  # More specific
        'origami': ['origami', 'miura', 'folding', 'cylindre origami', 'pattern'],
        'lion': ['lion', 'animal', 'sculpture', 'procedural'],
        'lattice_sc': ['lattice sc', 'simple cubic', 'cubic lattice', 'lattice cubique'],
        'lattice_bcc': ['bcc', 'body centered cubic', 'body-centered', 'lattice bcc'],
        'lattice_fcc': ['fcc', 'face centered cubic', 'face-centered', 'lattice fcc'],
        'lattice_diamond': ['diamond lattice', 'diamond structure', 'tetrahedral lattice'],
        'lattice_octet': ['octet', 'octet truss', 'octahedral', 'lattice octet'],
    }
        
    async def analyze(self, prompt: str) -> Dict[str, Any]:
        """Analyzes and detects application type + parameters"""
        p = prompt.lower()

        app_type = self._detect_application_type(p)
        log.info(f"✅ Detected application type: {app_type.upper()}")

        if app_type == 'splint':
            return self._analyze_splint(prompt)
        elif app_type == 'stent':
            return self._analyze_stent(prompt)
        elif app_type == 'facade_pyramid':
            return self._analyze_facade_pyramid(prompt)
        elif app_type == 'honeycomb':
            return self._analyze_honeycomb(prompt)
        elif app_type == 'louvre_wall':
            return self._analyze_louvre_wall(prompt)
        elif app_type == 'sine_wave_fins':
            return self._analyze_sine_wave_fins(prompt)
        elif app_type == 'gripper':
            return self._analyze_gripper(prompt)
        elif app_type == 'heatsink':
            return self._analyze_heatsink(prompt)
        elif app_type == 'origami':
            return self._analyze_origami(prompt)
        elif app_type == 'lion':
            return self._analyze_lion(prompt)
        elif app_type == 'lattice_sc':
            return self._analyze_lattice_sc(prompt)
        elif app_type == 'lattice_bcc':
            return self._analyze_lattice_bcc(prompt)
        elif app_type == 'lattice_fcc':
            return self._analyze_lattice_fcc(prompt)
        elif app_type == 'lattice_diamond':
            return self._analyze_lattice_diamond(prompt)
        elif app_type == 'lattice_octet':
            return self._analyze_lattice_octet(prompt)
        elif app_type == 'unknown':
            return {
                "type": "unknown",
                "parameters": {},
                "raw_prompt": prompt
            }

    def _analyze_honeycomb(self, prompt: str) -> Dict[str, Any]:
        """Analysis for honeycomb panel (hexagonal honeycomb panel)"""
        params = {
            # Panel
            'panel_width': self._find_number(prompt, r'(?:panel\s+)?width\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 300.0),
            'panel_height': self._find_number(prompt, r'(?:panel\s+)?height\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 380.0),
            'panel_thickness': self._find_number(prompt, r'(?:panel\s+)?thickness\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 40.0),

            # Hexagonal cells
            'cell_size': self._find_number(prompt, r'cell\s+size\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 12.0),
            'wall_thickness': self._find_number(prompt, r'wall\s+thickness\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 2.2),
            'cell_depth': self._find_number(prompt, r'cell\s+depth\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 40.0),

            # Options
            'corner_fillet': self._find_number(prompt, r'corner\s+fillet\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 0.0),
            'full_depth': 'full depth' in prompt.lower() or 'through' in prompt.lower(),
        }
        
        log.info(f"✅ HONEYCOMB: {params['panel_width']}×{params['panel_height']}mm, cell={params['cell_size']}mm")
        
        return {
            "type": "honeycomb",
            "parameters": params,
            "raw_prompt": prompt
        }

    def _analyze_origami(self, prompt: str) -> Dict[str, Any]:
        """Analysis for origami cylinder"""
        params = {
            'outer_diameter': self._find_number(prompt, r'diameter\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 40.0),
            'height': self._find_number(prompt, r'height\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 100.0),
            'relief': self._find_number(prompt, r'relief\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 1.8),
            'n_cols': int(self._find_number(prompt, r'(\d+)\s*columns?', 18)),
            'n_rows': int(self._find_number(prompt, r'(\d+)\s*rows?', 14)),
            'twist': self._find_number(prompt, r'twist\s*:?\s*(\d+(?:\.\d+)?)', 0.5),
        }
        
        log.info(f"✅ ORIGAMI: diameter={params['outer_diameter']}mm, height={params['height']}mm")
        
        return {
            "type": "origami",
            "parameters": params,
            "raw_prompt": prompt
        }

    def _analyze_lion(self, prompt: str) -> Dict[str, Any]:
        """Analysis for procedural lion"""
        params = {
            'scale': self._find_number(prompt, r'scale\s*:?\s*(\d+(?:\.\d+)?)', 1.0),
            'quality': int(self._find_number(prompt, r'quality\s*:?\s*(\d+)', 200)),
            'iso_level': self._find_number(prompt, r'iso\s*level\s*:?\s*(\d+(?:\.\d+)?)', 0.36),
        }
        
        log.info(f"✅ LION: scale={params['scale']}, quality={params['quality']}")
        
        return {
            "type": "lion",
            "parameters": params,
            "raw_prompt": prompt
        }

    def _analyze_lattice_sc(self, prompt: str) -> Dict[str, Any]:
        """Analysis for simple cubic lattice"""
        params = {
            'block_x': self._find_number(prompt, r'width\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'block_y': self._find_number(prompt, r'depth\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'block_z': self._find_number(prompt, r'height\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'cell_size': self._find_number(prompt, r'cell\s*size\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 15.0),
            'strut_radius': self._find_number(prompt, r'strut\s*radius\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 1.2),
            'node_radius_factor': self._find_number(prompt, r'node\s*factor\s*:?\s*(\d+(?:\.\d+)?)', 1.55),
        }
        
        log.info(f"✅ LATTICE SC: {params['block_x']}×{params['block_y']}×{params['block_z']}mm")
        
        return {
            "type": "lattice_sc",
            "parameters": params,
            "raw_prompt": prompt
        }

    def _analyze_lattice_bcc(self, prompt: str) -> Dict[str, Any]:
        """Analysis for BCC lattice"""
        params = {
            'block_x': self._find_number(prompt, r'(?:width|block\s*x)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'block_y': self._find_number(prompt, r'(?:depth|block\s*y)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'block_z': self._find_number(prompt, r'(?:height|block\s*z)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'cell_size': self._find_number(prompt, r'cell\s*size\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 15.0),
            'strut_radius': self._find_number(prompt, r'strut\s*radius\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 1.2),
            'node_radius': self._find_number(prompt, r'node\s*radius\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 1.86),
        }
        
        log.info(f"✅ LATTICE BCC: {params['block_x']}×{params['block_y']}×{params['block_z']}mm")
        
        return {
            "type": "lattice_bcc",
            "parameters": params,
            "raw_prompt": prompt
        }

    def _analyze_lattice_fcc(self, prompt: str) -> Dict[str, Any]:
        """Analysis for FCC lattice"""
        params = {
            'block_x': self._find_number(prompt, r'(?:width|block\s*x)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'block_y': self._find_number(prompt, r'(?:depth|block\s*y)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'block_z': self._find_number(prompt, r'(?:height|block\s*z)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'cell_size': self._find_number(prompt, r'cell\s*size\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 15.0),
            'strut_radius': self._find_number(prompt, r'strut\s*radius\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 1.2),
            'node_radius': self._find_number(prompt, r'node\s*radius\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 1.86),
        }
        
        log.info(f"✅ LATTICE FCC: {params['block_x']}×{params['block_y']}×{params['block_z']}mm")
        
        return {
            "type": "lattice_fcc",
            "parameters": params,
            "raw_prompt": prompt
        }

    def _analyze_lattice_diamond(self, prompt: str) -> Dict[str, Any]:
        """Analysis for Diamond lattice"""
        params = {
            'block_x': self._find_number(prompt, r'(?:width|block\s*x)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'block_y': self._find_number(prompt, r'(?:depth|block\s*y)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'block_z': self._find_number(prompt, r'(?:height|block\s*z)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'cell_size': self._find_number(prompt, r'cell\s*size\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 15.0),
            'strut_radius': self._find_number(prompt, r'strut\s*radius\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 1.2),
            'node_radius': self._find_number(prompt, r'node\s*radius\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 1.86),
        }
        
        log.info(f"✅ LATTICE DIAMOND: {params['block_x']}×{params['block_y']}×{params['block_z']}mm")
        
        return {
            "type": "lattice_diamond",
            "parameters": params,
            "raw_prompt": prompt
        }

    def _analyze_lattice_octet(self, prompt: str) -> Dict[str, Any]:
        """Analysis for Octet truss lattice"""
        params = {
            'block_x': self._find_number(prompt, r'(?:width|block\s*x)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'block_y': self._find_number(prompt, r'(?:depth|block\s*y)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'block_z': self._find_number(prompt, r'(?:height|block\s*z)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 30.0),
            'cell_size': self._find_number(prompt, r'cell\s*size\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 15.0),
            'strut_radius': self._find_number(prompt, r'strut\s*radius\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 1.2),
            'node_radius': self._find_number(prompt, r'node\s*radius\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 1.86),
        }
        
        log.info(f"✅ LATTICE OCTET: {params['block_x']}×{params['block_y']}×{params['block_z']}mm")
        
        return {
            "type": "lattice_octet",  
            "parameters": params,
            "raw_prompt": prompt
        }
    
    def _detect_application_type(self, prompt: str) -> str:
        """Detects application type based on keywords with stricter detection"""
        scores = {app: 0 for app in self.APPLICATION_KEYWORDS}

        for app_type, keywords in self.APPLICATION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in prompt:
                    scores[app_type] += 1

        # Strict detection rules (by priority order)

        # 1. HEATSINK - Very specific
        if 'heatsink' in prompt or 'heat sink' in prompt:
            return 'heatsink'

        # 2. LOUVRE WALL - BEFORE GRIPPER!
        if 'louvre' in prompt or 'louver' in prompt or 'pavilion' in prompt:
            return 'louvre_wall'

        # 3. GRIPPER - Requires exact word "gripper"
        if 'gripper' in prompt:
            return 'gripper'

        # 4. STENT - Requires "stent" keyword (medical context inferred)
        if 'stent' in prompt:
            return 'stent'

        # 5. HONEYCOMB PANEL - Requires "honeycomb" + context
        if ('honeycomb panel' in prompt or 'alveolar' in prompt or
            'hexagonal cells' in prompt or 'cellular panel' in prompt or
            ('honeycomb' in prompt and ('panel' in prompt or 'cell' in prompt))):
            return 'honeycomb'

        # 6. PYRAMID FACADE - Requires explicit "pyramid"
        if 'pyramid facade' in prompt or 'hexagonal pyramid' in prompt or 'pyramidal' in prompt:
            return 'facade_pyramid'

        # 7. SINE WAVE FINS - Requires combination "sine" or "wave" + "fins"
        if (('sine' in prompt or 'wave' in prompt) and 'fin' in prompt) or 'zahner' in prompt:
            return 'sine_wave_fins'

        # 8. ORIGAMI
        if 'origami' in prompt or 'miura' in prompt:
            return 'origami'

        # 9. LION  
        if 'lion' in prompt or 'procedural' in prompt:
            return 'lion'

        # 10. LATTICES SPECIFIQUES - AVANT lattice générique
        if 'octet' in prompt or 'octet truss' in prompt:
            return 'lattice_octet'

        if 'diamond lattice' in prompt or 'diamond structure' in prompt:
            return 'lattice_diamond'

        if 'bcc' in prompt or 'body centered' in prompt or 'body-centered' in prompt:
            return 'lattice_bcc'

        if 'fcc' in prompt or 'face centered' in prompt or 'face-centered' in prompt:
            return 'lattice_fcc'

        if 'simple cubic' in prompt or 'lattice sc' in prompt:
            return 'lattice_sc'

        # 9. Score-based detection with higher threshold
        detected = max(scores, key=scores.get)

        # Requires at least 2 matches to consider a valid template
        if scores[detected] < 2:
            log.info("🧠 No strong template match (score < 2) → routing to Chain-of-Thought")
            return 'unknown'

        log.info(f"✅ Template detected via scoring: {detected} (score: {scores[detected]})")
        return detected

    def _analyze_heatsink(self, prompt: str) -> Dict[str, Any]:
        """Analysis for heatsink (thermal dissipator)"""
        params = {
            # Plate
            'plate_w': self._find_number(prompt, r'plate.*?width\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 40.0),
            'plate_h': self._find_number(prompt, r'plate.*?height\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 40.0),
            'plate_t': self._find_number(prompt, r'plate.*?thickness\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 3.0),

            # Tube/pipe
            'tube_od': self._find_number(prompt, r'tube.*?(?:outer\s+)?diameter\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 42.0),
            'tube_len': self._find_number(prompt, r'tube.*?length\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 10.0),

            # Bars/fins
            'bar_len': self._find_number(prompt, r'(?:bar|fin).*?length\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 22.0),
            'bar_angle': self._find_number(prompt, r'(?:bar|fin).*?angle\s*:?\s*(\d+(?:\.\d+)?)\s*(?:deg|°)', 20.0),

            # Holes
            'hole_d': self._find_number(prompt, r'hole.*?diameter\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 3.3),
            'hole_pitch': self._find_number(prompt, r'hole.*?pitch\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 32.0),
        }
        
        log.info(f"✅ HEATSINK: plate {params['plate_w']}×{params['plate_h']}mm, bars {params['bar_len']}mm @ {params['bar_angle']}°")
        
        return {
            "type": "heatsink",
            "parameters": params,
            "raw_prompt": prompt
        }

    def _analyze_louvre_wall(self, prompt: str) -> Dict[str, Any]:
        """Analysis for louvre wall (pavilion with diagonal slats)"""
        params = {
            # Triangle
            'width': self._find_number(prompt, r'width\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 280.0),
            'height': self._find_number(prompt, r'height\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 260.0),
            'thickness': self._find_number(prompt, r'thickness\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 40.0),
            'corner_fillet': self._find_number(prompt, r'(?:corner|fillet)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 3.0),

            # Louvres (layer 1)
            'angle_deg': self._find_number(prompt, r'(?:angle|slat angle)\s*:?\s*(\d+(?:\.\d+)?)\s*(?:deg|°)', 35.0),
            'pitch': self._find_number(prompt, r'(?:pitch|spacing)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 12.0),
            'slat_width': self._find_number(prompt, r'slat\s+width\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 8.0),
            'slat_depth': self._find_number(prompt, r'slat\s+depth\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 12.0),
            'end_radius': self._find_number(prompt, r'(?:end|edge)\s+radius\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 3.0),
            'layer1_z': self._find_number(prompt, r'layer\s+1\s+z\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 6.0),

            # Layer 2 (optional)
            'layer2_enabled': 'layer 2' in prompt.lower() or 'crossed' in prompt.lower() or 'double' in prompt.lower(),
            'layer2_angle': self._find_number(prompt, r'layer\s+2\s+angle\s*:?\s*(\d+(?:\.\d+)?)\s*(?:deg|°)', 55.0),
            'layer2_z_offset': self._find_number(prompt, r'layer\s+2\s+z\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 0.0),

            # Options
            'boolean_mode': 'intersect' if 'intersect' in prompt.lower() else 'union',
            'same_layer': 'same layer' in prompt.lower() or 'same z' in prompt.lower(),
            'full_depth': 'full depth' in prompt.lower() or 'through' in prompt.lower(),
        }
        
        log.info(f"✅ LOUVRE WALL: {params['width']}×{params['height']}mm, angle={params['angle_deg']}°")
        
        return {
            "type": "louvre_wall",
            "parameters": params,
            "raw_prompt": prompt
        }

    def _analyze_sine_wave_fins(self, prompt: str) -> Dict[str, Any]:
        """Analysis for sine wave fins (wavy facade with fins)"""
        params = {
            # Panel
            'panel_length': self._find_number(prompt, r'(?:panel\s+)?(?:length|width)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 420.0),
            'panel_height': self._find_number(prompt, r'(?:panel\s+)?height\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 180.0),
            'depth': self._find_number(prompt, r'depth\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 140.0),

            # Fins
            'n_fins': int(self._find_number(prompt, r'(\d+)\s+(?:fins|ribs|blades)', 34)),
            'fin_thickness': self._find_number(prompt, r'fin\s+thickness\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 3.0),

            # Sinusoid
            'amplitude': self._find_number(prompt, r'amplitude\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 40.0),
            'period_ratio': self._find_number(prompt, r'period\s+ratio\s*:?\s*(\d+(?:\.\d+)?)', 0.9),

            # Base
            'base_thickness': self._find_number(prompt, r'base\s+thickness\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 6.0),
        }
        
        log.info(f"✅ SINE WAVE FINS: {params['panel_length']}×{params['panel_height']}mm, {params['n_fins']} fins")
        
        return {
            "type": "sine_wave_fins",
            "parameters": params,
            "raw_prompt": prompt
        }
    
    def _analyze_facade_pyramid(self, prompt: str) -> Dict[str, Any]:
        """Analysis for facade with pyramids (OLD VERSION)"""
        p = prompt.lower()
        
        params = {
            'hex_radius': self._find_number(prompt, r'radius\s+(\d+(?:\.\d+)?)\s*mm', 60.0),
            'w_frame': self._find_number(prompt, r'frame.*?width\s+(\d+(?:\.\d+)?)\s*mm', 8.0),
            'h_frame': self._find_number(prompt, r'frame.*?height\s+(\d+(?:\.\d+)?)\s*mm', 10.0),
            'tri_height': self._find_number(prompt, r'triangle.*?height\s+(\d+(?:\.\d+)?)\s*mm', 55.0),
            'tri_thickness': self._find_number(prompt, r'(?:triangle|plate).*?thickness\s+(\d+(?:\.\d+)?)\s*mm', 2.4),
            'w_bar': self._find_number(prompt, r'bar.*?width\s+(\d+(?:\.\d+)?)\s*mm', 8.0),
        }
        
        log.info(f"✅ FACADE PYRAMID: hex radius={params['hex_radius']}mm, triangle height={params['tri_height']}mm")
        
        return {
            "type": "facade_pyramid",
            "parameters": params,
            "raw_prompt": prompt
        }
    
    def _analyze_facade_parametric(self, prompt: str) -> Dict[str, Any]:
        """Analysis for parametric facade (NEW VERSION)"""
        p = prompt.lower()

        # Pattern type
        pattern_type = 'wavy'
        patterns = ['wavy', 'hexagonal', 'triangular', 'fins', 'louvers', 'diamond', 'scales']
        for pt in patterns:
            if pt in p:
                pattern_type = pt
                break
        
        params = {
            'pattern_type': pattern_type,
            'width': self._find_number(prompt, r'width\s*:?\s*(\d+(?:\.\d+)?)\s*(?:m|mm)', 20000.0),
            'height': self._find_number(prompt, r'height\s*:?\s*(\d+(?:\.\d+)?)\s*(?:m|mm)', 10000.0),
            'depth': self._find_number(prompt, r'(?:depth|relief)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 500.0),
            'element_size': self._find_number(prompt, r'element\s+size\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 200.0),
            'spacing': self._find_number(prompt, r'spacing\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 50.0),
            'amplitude': self._find_number(prompt, r'amplitude\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 300.0),
            'frequency': self._find_number(prompt, r'frequency\s*:?\s*(\d+(?:\.\d+)?)', 3.0),
        }
        
        log.info(f"✅ FACADE PARAMETRIC: {pattern_type.upper()}, {params['width']}×{params['height']}mm")
        
        return {
            "type": "facade_parametric",
            "parameters": params,
            "raw_prompt": prompt
        }
    
    def _analyze_splint(self, prompt: str) -> Dict[str, Any]:
        """Analysis for splint/orthosis"""
        p = prompt.lower()
        sections = self._extract_sections(prompt)
        
        splint_type = self._extract_splint_type(p)
        curvatures = self._extract_curvatures(prompt)
        
        features = {
            'holes': self._extract_holes(p),
            'slots': self._extract_slots(p),
            'fillets': self._extract_fillets(p)
        }
        
        thickness = self._find_number(prompt, r'(?:wall\s+)?thickness\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 3.5)
        edge_radius = self._find_number(prompt, r'(?:edge|edges)\s*:?\s*(\d+(?:\.\d+)?)\s*mm\s+radius', 2.0)
        total_length_explicit = self._find_number(prompt, r'total\s+(?:assembled\s+)?length\s*:?\s*(\d+(?:\.\d+)?)\s*mm', None)
        
        log.info(f"✅ SPLINT ({splint_type}): {len(sections)} sections")
        
        return {
            "type": "splint",
            "splint_type": splint_type,
            "sections": sections,
            "features": features,
            "thickness": thickness,
            "edge_radius": edge_radius,
            "total_length_explicit": total_length_explicit,
            "curvatures": curvatures,
            "raw_prompt": prompt
        }
    
    def _extract_splint_type(self, text: str) -> str:
        match = re.search(r'\b(resting|dynamic|static|functional)\s+(?:hand\s+)?splint', text)
        return match.group(1) if match else 'resting'
    
    def _extract_curvatures(self, prompt: str) -> Dict[str, float]:
        curvatures = {}
        lines = prompt.split('\n')
        current_section = None
        
        for line in lines:
            line_lower = line.lower()
            
            if 'forearm' in line_lower:
                current_section = 'forearm'
            elif 'palm' in line_lower:
                current_section = 'palm'
            elif 'finger' in line_lower:
                current_section = 'finger'
            
            if current_section and 'curv' in line_lower:
                curve_match = re.search(r'(\d+(?:\.\d+)?)\s*mm', line)
                if curve_match:
                    curvatures[current_section] = float(curve_match.group(1))
        
        return curvatures
    
    def _extract_fillets(self, text: str) -> Optional[Dict[str, Any]]:
        has_smooth = 'smooth' in text or 'curved' in text or 'rounded' in text or 'fillet' in text
        
        if not has_smooth:
            return None
        
        radius_match = re.search(r'(?:smooth|filleted?)\s+(?:transitions?|edges?)\s*:?\s*(\d+(?:\.\d+)?)\s*mm', text, re.I)
        radius = float(radius_match.group(1)) if radius_match else 8.0
        
        return {
            'enabled': True,
            'radius': radius
        }
    
    def _extract_sections(self, prompt: str) -> List[Dict[str, Any]]:
        sections = []
        lines = prompt.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            
            if re.search(r'\bpalm\s+(?:platform|section|support)\b', line_lower):
                length = self._find_number(line, r'length\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 80.0)
                width_match = re.search(r'(?:constant\s+)?(\d+(?:\.\d+)?)\s*mm', line, re.I)
                width = float(width_match.group(1)) if width_match else 75.0
                
                sections.append({
                    'name': 'palm',
                    'length': length,
                    'width': width,
                    'width_start': width,
                    'width_end': width,
                    'angle': 20.0
                })
                continue
            
            if re.search(r'\bforearm\s+(?:support|section)\b', line_lower):
                length = self._find_number(line, r'length\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 150.0)
                
                taper_match = re.search(r'tapers?\s+from\s+(\d+(?:\.\d+)?)\s*mm.*?to\s+(\d+(?:\.\d+)?)\s*mm', line, re.I)
                if taper_match:
                    width_start = float(taper_match.group(1))
                    width_end = float(taper_match.group(2))
                else:
                    width_start = 70.0
                    width_end = 60.0
                
                sections.append({
                    'name': 'forearm',
                    'length': length,
                    'width_start': width_start,
                    'width_end': width_end,
                    'angle': 0.0
                })
                continue
            
            if re.search(r'\bfinger\s+(?:support|section)\b', line_lower):
                length = self._find_number(line, r'length\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 40.0)
                width_match = re.search(r'(\d+(?:\.\d+)?)\s*mm', line, re.I)
                width = float(width_match.group(1)) if width_match else 65.0
                
                sections.append({
                    'name': 'finger',
                    'length': length,
                    'width': width,
                    'width_start': width,
                    'width_end': width,
                    'angle': 0.0
                })
        
        if not sections:
            sections = [{'name': 'main', 'length': 270.0, 'width_start': 70.0, 'width_end': 60.0, 'angle': 0.0}]
        
        order = {'forearm': 0, 'palm': 1, 'finger': 2}
        sections.sort(key=lambda s: order.get(s['name'], 99))
        
        return sections
    
    def _extract_holes(self, text: str) -> Optional[Dict[str, Any]]:
        if 'hole' not in text and 'ventilation' not in text and 'perforation' not in text:
            return None
        
        diameter_match = re.search(r'(\d+(?:\.\d+)?)\s*mm\s+diameter', text, re.I)
        diameter = float(diameter_match.group(1)) if diameter_match else 6.0
        
        grid_match = re.search(r'(\d+)\s*[x×]\s*(\d+)', text, re.I)
        if grid_match:
            grid_x, grid_y = int(grid_match.group(1)), int(grid_match.group(2))
        else:
            grid_x, grid_y = 10, 3
        
        return {'diameter': diameter, 'grid_x': grid_x, 'grid_y': grid_y}
    
    def _extract_slots(self, text: str) -> Optional[Dict[str, Any]]:
        if 'slot' not in text and 'strap' not in text:
            return None
        
        width_match = re.search(r'(\d+(?:\.\d+)?)\s*mm\s+wide', text, re.I)
        width = float(width_match.group(1)) if width_match else 25.0
        
        depth_match = re.search(r'(\d+(?:\.\d+)?)\s*mm\s+deep', text, re.I)
        depth = float(depth_match.group(1)) if depth_match else 3.0
        
        positions = []
        pos_matches = re.findall(r'(\d+(?:\.\d+)?)\s*mm', text)
        if len(pos_matches) >= 3:
            positions = [float(p) for p in pos_matches[-3:]]
        else:
            positions = [50.0, 150.0, 220.0]
        
        return {'width': width, 'depth': depth, 'length': 20.0, 'positions': positions}
    
    def _find_number(self, text: str, pattern: str, default: float) -> float:
        match = re.search(pattern, text, re.I)
        return float(match.group(1)) if match else default
    
    def _analyze_stent(self, prompt: str) -> Dict[str, Any]:
        p = prompt.lower()
        
        params = {
            'outer_radius': self._find_number(prompt, r'radius\s+(\d+(?:\.\d+)?)\s*mm', 8.0),
            'length': self._find_number(prompt, r'length\s+(\d+(?:\.\d+)?)\s*mm', 40.0),
            'n_peaks': int(self._find_number(prompt, r'(\d+)\s+peaks?', 8)),
            'n_rings': int(self._find_number(prompt, r'(\d+)\s+rings?', 6)),
            'amplitude': self._find_number(prompt, r'amplitude\s+(\d+(?:\.\d+)?)\s*mm', 3.0),
            'ring_spacing': self._find_number(prompt, r'spacing\s+(\d+(?:\.\d+)?)\s*mm', 6.0),
            'strut_width': self._find_number(prompt, r'strut.*?width\s+(\d+(?:\.\d+)?)\s*mm', 0.6),
            'strut_depth': self._find_number(prompt, r'strut.*?depth\s+(\d+(?:\.\d+)?)\s*mm', 0.4),
        }
        
        return {"type": "stent", "parameters": params, "raw_prompt": prompt}
    
    def _analyze_gripper(self, prompt: str) -> Dict[str, Any]:
        params = {
            'arm_length': self._find_number(prompt, r'arm.*?length\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 25.0),
            'arm_width': self._find_number(prompt, r'arm.*?width\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 8.0),
            'center_diameter': self._find_number(prompt, r'center.*?diameter\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 6.0),
            'thickness': self._find_number(prompt, r'thickness\s*:?\s*(\d+(?:\.\d+)?)\s*mm', 1.5),
            'n_arms': int(self._find_number(prompt, r'(\d+)[- ]arm', 4)),  # 🔥 EXTRACTION DU NOMBRE DE BRAS
        }
        
        log.info(f"✅ GRIPPER: {params['n_arms']} arms, length={params['arm_length']}mm")
        
        return {"type": "gripper", "parameters": params, "raw_prompt": prompt}


class GeneratorAgent:
    def __init__(self):
        self.templates = CodeTemplates()
    
    async def generate(self, analysis: Dict[str, Any]) -> tuple[str, str]:
        app_type = analysis.get('type', 'splint')
        
        log.info(f"🎯 GeneratorAgent: Generating code for type='{app_type}'")
        
        if app_type == 'splint':
            code = self.templates.generate_splint(analysis)
            file_type = 'splint'
        elif app_type == 'stent':
            code = self.templates.generate_stent(analysis)
            file_type = 'stent'
        elif app_type == 'facade_pyramid':
            code = self.templates.generate_facade_pyramid(analysis)
            file_type = 'facade'
        elif app_type == 'honeycomb':  # 🔥 NOUVEAU
            code = self.templates.generate_honeycomb(analysis)
            file_type = 'facade'
        elif app_type == 'louvre_wall':
            code = self.templates.generate_louvre_wall(analysis)
            file_type = 'facade'
        elif app_type == 'sine_wave_fins':
            code = self.templates.generate_sine_wave_fins(analysis)
            file_type = 'facade'
        elif app_type == 'gripper':
            code = self.templates.generate_gripper(analysis)
            file_type = 'gripper'
        elif app_type == 'heatsink':
            code = self.templates.generate_heatsink(analysis)
            file_type = 'heatsink'
        elif app_type == 'origami':
            code = self.templates.generate_origami_cylinder(analysis)
            file_type = 'origami'
        elif app_type == 'lion':
            code = self.templates.generate_lion(analysis)
            file_type = 'lion'
        elif app_type == 'lattice_sc':
            code = self.templates.generate_lattice_sc(analysis)
            file_type = 'lattice'
        elif app_type == 'lattice_bcc':
            code = self.templates.generate_lattice_bcc(analysis)
            file_type = 'lattice'
        elif app_type == 'lattice_fcc':
            code = self.templates.generate_lattice_fcc(analysis)
            file_type = 'lattice'
        elif app_type == 'lattice_diamond':
            code = self.templates.generate_lattice_diamond(analysis)
            file_type = 'lattice'
        elif app_type == 'lattice_octet':
            code = self.templates.generate_lattice_octet(analysis)
            file_type = 'lattice'
        else:
            log.warning(f"⚠️ Unknown app_type '{app_type}', defaulting to splint")
            code = self.templates.generate_splint(analysis)
            file_type = 'splint'
        
        log.info(f"✅ Generated code for file_type='{file_type}'")
        return code, file_type


class ValidatorAgent:
    def __init__(self):
        try:
            import cadquery as cq
            self.cq_ok = True
        except Exception:
            self.cq_ok = False

    def _safe_builtins(self):
        allowed = [
            "abs", "min", "max", "range", "len", "float", "int", "pow", "sum",
            "zip", "enumerate", "print", "list", "dict", "set", "tuple", "round",
            "__import__", "Exception", "BaseException", "ValueError", "any",
            "str", "open", "bytes", "bool", "isinstance", "type", "iter",
            "next", "hasattr", "getattr", "setattr", "dir", "format",
            "ord", "chr", "hex", "bin", "oct", "sorted", "reversed",
            "map", "filter", "all", "repr", "hash", "id", "callable"
        ]
        return {k: getattr(py_builtins, k) for k in allowed}

    async def validate_and_execute(self, code: str, app_type: str = "model") -> Dict[str, Any]:
        try:
            compile(code, "<cad>", "exec")
        except SyntaxError as e:
            return {"success": False, "errors": [f"Syntax: {e.msg}"]}

        import numpy as np
        from pathlib import Path
        import time

        # No-op function for show_object (used by CQ-Editor)
        def show_object(obj, name=None, options=None):
            """Dummy function - show_object is only for CQ-Editor"""
            pass

        ns = {
            "__builtins__": self._safe_builtins(),
            "math": math,
            "np": np,
            "numpy": np,
            "struct": __import__('struct'),
            "Path": Path,
            "show_object": show_object,
            "__file__": str(Path(__file__).parent / "temp_exec.py"),
        }

        try:
            exec(compile(code, "<cad>", "exec"), ns)

            backend_dir = Path(__file__).parent
            output_dir = backend_dir / "output"

            time.sleep(0.1)

            # ALWAYS search for the most recent .stl file (not just generated_*.stl)
            # This fixes the bug where an old file was returned instead of the new one
            stl_files = sorted(output_dir.glob("*.stl"), key=lambda p: p.stat().st_mtime, reverse=True)
            stl_path = str(stl_files[0].absolute()) if stl_files else None
            
        except Exception as e:
            log.error(f"Execution failed: {e}", exc_info=True)
            # Include exception type in error message so ErrorHandlerAgent can categorize it
            error_type = type(e).__name__
            return {"success": False, "errors": [f"Execution: {error_type}: {e}"]}

        if stl_path and os.path.exists(stl_path):
            mesh = self._create_mesh_from_stl(stl_path)
        else:
            mesh = self._create_mesh()

        return {
            "success": True,
            "mesh": mesh,
            "analysis": {"dimensions": {}, "features": {}, "validation": {}},
            "stl_path": stl_path,
            "step_path": None,
        }

    def _create_mesh_from_stl(self, stl_path: str) -> Dict[str, Any]:
        try:
            import struct

            # First, check if this is ASCII or binary STL
            with open(stl_path, 'rb') as f:
                header = f.read(80)
                # ASCII STL files start with "solid" (but binary can too, so check more carefully)
                is_ascii = header.startswith(b'solid') and b'\n' in header[:80]

            if is_ascii:
                # Parse ASCII STL format
                log.info(f"Reading ASCII STL file: {stl_path}")
                vertices = []
                faces = []

                with open(stl_path, 'r') as f:
                    lines = f.readlines()
                    i = 0
                    while i < len(lines):
                        line = lines[i].strip()
                        if line.startswith('facet normal'):
                            # Read the 3 vertices for this facet
                            # Skip "outer loop" line
                            i += 2

                            facet_verts = []
                            for _ in range(3):
                                vertex_line = lines[i].strip()
                                if vertex_line.startswith('vertex'):
                                    coords = vertex_line.split()[1:4]
                                    facet_verts.extend([float(coords[0]), float(coords[1]), float(coords[2])])
                                i += 1

                            base_idx = len(vertices) // 3
                            vertices.extend(facet_verts)
                            faces.extend([base_idx, base_idx+1, base_idx+2])

                            # Skip "endloop" and "endfacet"
                            i += 2
                        else:
                            i += 1

                num_triangles = len(faces) // 3
                log.info(f"Loaded ASCII STL: {num_triangles} triangles")

            else:
                # Parse binary STL format
                log.info(f"Reading binary STL file: {stl_path}")
                with open(stl_path, 'rb') as f:
                    f.read(80)
                    num_triangles = struct.unpack('<I', f.read(4))[0]

                    vertices = []
                    faces = []

                    for i in range(num_triangles):
                        f.read(12)
                        v1 = struct.unpack('<3f', f.read(12))
                        v2 = struct.unpack('<3f', f.read(12))
                        v3 = struct.unpack('<3f', f.read(12))

                        base_idx = len(vertices) // 3
                        vertices.extend(v1)
                        vertices.extend(v2)
                        vertices.extend(v3)

                        faces.extend([base_idx, base_idx+1, base_idx+2])
                        f.read(2)

            # Decimate if too many triangles
            if len(faces) // 3 > 10000:
                log.info(f"Decimating mesh from {len(faces)//3} to ~5000 triangles")
                step = (len(faces) // 3) // 5000
                vertices_decimated = []
                faces_decimated = []
                for i in range(0, len(faces), step*3):
                    if i+2 < len(faces):
                        base = len(vertices_decimated) // 3
                        for j in range(3):
                            idx = faces[i+j] * 3
                            vertices_decimated.extend(vertices[idx:idx+3])
                        faces_decimated.extend([base, base+1, base+2])

                vertices = vertices_decimated
                faces = faces_decimated

            return {"vertices": vertices, "faces": faces, "normals": []}

        except Exception as e:
            log.warning(f"Failed to load STL: {e}", exc_info=True)
            return self._create_mesh()
    
    def _create_mesh(self) -> Dict[str, Any]:
        vertices = []
        faces = []
        
        for i in range(10):
            for j in range(10):
                vertices.extend([(i-5)*10, j*10, math.sin(i*0.5)*math.cos(j*0.5)*5])
        
        for i in range(9):
            for j in range(9):
                v0, v1 = i*10+j, (i+1)*10+j
                v2, v3 = (i+1)*10+(j+1), i*10+(j+1)
                faces.extend([v0, v1, v2, v0, v2, v3])
        
        return {"vertices": vertices, "faces": faces, "normals": []}