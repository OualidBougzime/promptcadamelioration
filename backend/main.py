import os
import json
import logging
import time
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel

from agents import AnalystAgent, GeneratorAgent, ValidatorAgent
from multi_agent_system import OrchestratorAgent

# ========== CONFIGURATION ==========
# Load environment variables from .env
load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("cadamx")

app = FastAPI(title="CadaMx API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agents (3 existing)
analyst = AnalystAgent()
generator = GeneratorAgent()
validator = ValidatorAgent()

# Orchestrator (coordinates 9 agents: 3 existing + 6 new)
orchestrator = OrchestratorAgent(analyst, generator, validator)

# Temporary storage of last generated files
_last_stl_path: Optional[str] = None
_last_step_path: Optional[str] = None
_last_app_type: Optional[str] = None


# ========== MODELS ==========
class GenerateRequest(BaseModel):
    prompt: str


# ========== HELPERS ==========
def escape_for_json(text: str) -> str:
    """
    Escapes a string for inclusion in JSON.
    Important for Python code that contains newlines, quotes, etc.
    """
    if not text:
        return text

    return (text
        .replace('\\', '\\\\')  # Backslash first
        .replace('\n', '\\n')   # Newlines
        .replace('\r', '\\r')   # Carriage returns
        .replace('\t', '\\t')   # Tabs
        .replace('"', '\\"')    # Double quotes
    )


async def send_sse_event(event_type: str, data: dict) -> str:
    """
    Formats an SSE event.
    Returns a string ready to be sent.
    """
    data['type'] = event_type
    json_str = json.dumps(data, ensure_ascii=False)
    return f"data: {json_str}\n\n"


# ========== ENDPOINTS ==========

@app.get("/")
async def root():
    """Health check"""
    return {"status": "ok", "service": "CadaMx API"}

@app.get("/api/export/grasshopper")
async def export_grasshopper():
    """Export as Grasshopper-compatible format with sections"""
    from pathlib import Path
    import json
    
    if not _last_stl_path or not os.path.exists(_last_stl_path):
        raise HTTPException(status_code=404, detail="No model available")
    
    # Read STL and convert to sectioned format
    import struct
    sections = []
    
    with open(_last_stl_path, 'rb') as f:
        f.read(80)  # header
        num_triangles = struct.unpack('<I', f.read(4))[0]
        
        # Group triangles by Z height (sections)
        z_sections = {}
        for i in range(num_triangles):
            f.read(12)  # normal
            v1 = struct.unpack('<3f', f.read(12))
            v2 = struct.unpack('<3f', f.read(12))
            v3 = struct.unpack('<3f', f.read(12))
            
            avg_z = (v1[2] + v2[2] + v3[2]) / 3
            section_key = int(avg_z / 10) * 10  # 10mm sections
            
            if section_key not in z_sections:
                z_sections[section_key] = []
            
            z_sections[section_key].append({
                "vertices": [v1, v2, v3],
                "normal": struct.unpack('<3f', f.read(12))
            })
            f.read(2)  # attribute
    
    # Convert to Grasshopper format
    gh_data = {
        "type": _last_app_type or "model",
        "sections": [],
        "metadata": {
            "total_triangles": num_triangles,
            "section_height": 10.0
        }
    }
    
    for z_height, triangles in sorted(z_sections.items()):
        gh_data["sections"].append({
            "z_position": z_height,
            "triangles": triangles[:1000]  # Limit for performance
        })
    
    response = json.dumps(gh_data, indent=2)
    
    return Response(
        content=response,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="{_last_app_type or "model"}_grasshopper.json"'
        }
    )


@app.post("/api/generate")
async def generate_endpoint(request: GenerateRequest):
    """
    Main generation endpoint with SSE streaming.

    Event flow:
    1. type: "status" - Progress updates
    2. type: "code" - Generated Python code (may be escaped)
    3. type: "complete" - Final result with mesh, analysis, etc.
    4. type: "error" - In case of error
    """
    
    global _last_stl_path, _last_step_path, _last_app_type
    
    async def event_stream():
        try:
            start_time = time.time()
            log.info(f"🚀 Starting multi-agent workflow for prompt: {request.prompt[:100]}...")

            # List to collect progress events
            progress_events = []

            # Callback to send progress events
            async def progress_callback(event_type: str, data: dict):
                if event_type == "code":
                    # Escape code for JSON
                    data["code"] = escape_for_json(data.get("code", ""))
                event = await send_sse_event(event_type, data)
                progress_events.append(event)

            # Execute orchestrated workflow with 9 agents
            result = await orchestrator.execute_workflow(
                request.prompt,
                progress_callback=progress_callback
            )

            # Calculate execution time
            execution_time = time.time() - start_time

            # Send all progress events
            for event in progress_events:
                yield event

            if result["success"]:
                # Success - store paths
                _last_stl_path = result.get("stl_path")
                _last_step_path = result.get("step_path")
                _last_app_type = result.get("app_type", "model")

                log.info(f"✅ Multi-agent generation successful! (⏱️  {execution_time:.2f}s)")
                if _last_stl_path:
                    log.info(f"  STL: {_last_stl_path}")
                if _last_step_path:
                    log.info(f"  STEP: {_last_step_path}")

                # Send final result
                response_data = {
                    "success": True,
                    "mesh": result.get("mesh"),
                    "analysis": result.get("analysis"),
                    "code": result.get("code"),  # Unescaped code for final result
                    "app_type": result.get("app_type"),
                    "progress": 100,
                    "execution_time": round(execution_time, 2)  # Add execution time in seconds
                }

                # Add paths if available
                if _last_stl_path:
                    response_data["stl_path"] = _last_stl_path
                if _last_step_path:
                    response_data["step_path"] = _last_step_path

                # Add multi-agent system metadata
                if "metadata" in result:
                    response_data["metadata"] = result["metadata"]

                yield await send_sse_event("complete", response_data)

            else:
                # Error - agents handled the error
                errors = result.get("errors", ["Unknown error"])
                log.error(f"❌ Multi-agent workflow failed: {errors} (⏱️  {execution_time:.2f}s)")

                yield await send_sse_event("error", {
                    "success": False,
                    "errors": errors,
                    "progress": 0,
                    "metadata": result.get("metadata", {}),
                    "execution_time": round(execution_time, 2)
                })

        except Exception as e:
            # General uncaught error
            log.error(f"❌ Orchestrator error: {e}", exc_info=True)
            yield await send_sse_event("error", {
                "success": False,
                "errors": [str(e)],
                "progress": 0
            })
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
            "Access-Control-Allow-Origin": "*",
        }
    )


@app.get("/api/export/stl")
async def export_stl():
    """Download the last generated STL file"""
    from pathlib import Path

    # Use the path of the last generated file
    if _last_stl_path and os.path.exists(_last_stl_path):
        stl_file = Path(_last_stl_path)
    else:
        # Fallback: search for most recent file
        output_dir = Path(__file__).parent / "output"
        stl_files = sorted(
            output_dir.glob("generated_*.stl"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        if stl_files:
            stl_file = stl_files[0]
        else:
            raise HTTPException(status_code=404, detail="No STL file available")

    # Determine filename based on type
    filename = f"{_last_app_type or 'model'}_generated.stl"
    
    return FileResponse(
        str(stl_file),
        media_type="application/octet-stream",
        filename=filename
    )


@app.get("/api/export/step")
async def export_step():
    """Download the last generated STEP file"""
    if not _last_step_path or not os.path.exists(_last_step_path):
        raise HTTPException(status_code=404, detail="No STEP file available")

    filename = f"{_last_app_type or 'model'}_generated.step"
    
    return FileResponse(
        _last_step_path,
        media_type="application/octet-stream",
        filename=filename
    )


# ========== MAIN ==========
if __name__ == "__main__":
    import uvicorn

    # Create output directory if needed
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    log.info("Starting CadaMx API server...")
    log.info("Output directory: " + str(output_dir))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )