from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse

import json
import os
import sys
import shutil
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Tutor AIOS Dashboard")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "../..")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# ─────────────────────────────────────────
# Rotas de páginas
# ─────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/classroom", response_class=HTMLResponse)
async def classroom(request: Request):
    return templates.TemplateResponse("classroom.html", {"request": request})


@app.get("/progress", response_class=HTMLResponse)
async def progress(request: Request):
    return templates.TemplateResponse("progress.html", {"request": request})


@app.get("/memory", response_class=HTMLResponse)
async def memory(request: Request):
    return templates.TemplateResponse("memory.html", {"request": request})


@app.get("/agents", response_class=HTMLResponse)
async def agents(request: Request):
    return templates.TemplateResponse("agents.html", {"request": request})


@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


# ─────────────────────────────────────────
# Upload e ingestão de PDF
# ─────────────────────────────────────────

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...), course_id: str = Form(...)):
    try:

        # Normaliza course_id: espacos -> underscore, lowercase
        course_id = course_id.strip().lower().replace(" ", "_")

        # Diretório de PDFs
        sources_dir = os.path.join(PROJECT_DIR, "sources", "pdfs")
        os.makedirs(sources_dir, exist_ok=True)

        pdf_path = os.path.join(sources_dir, file.filename)

        with open(pdf_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Pipeline Tutor
        from aios.tutor_core.tutor_session import TutorSession

        session = TutorSession()

        chunks = session.ingest_pdf(pdf_path)
        curriculum = session.generate_curriculum(course_id)

        # ─────────────────────────────
        # Limpar markdown do LLM
        # ─────────────────────────────
        if isinstance(curriculum, str):
            curriculum = curriculum.replace("```json", "").replace("```", "").strip()
            curriculum = json.loads(curriculum)

        # ─────────────────────────────
        # Persistência do currículo
        # ─────────────────────────────
        progress_dir = os.path.join(PROJECT_DIR, "data", "progress")
        os.makedirs(progress_dir, exist_ok=True)

        course_file = os.path.join(progress_dir, f"{course_id}.json")

        course_data = {
            "course_id": course_id,
            "created_at": datetime.utcnow().isoformat(),
            "chunks": chunks,
            "curriculum": curriculum
        }

        with open(course_file, "w") as f:
            json.dump(course_data, f, indent=2)

        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "chunks": chunks,
            "curriculum": curriculum
        })

    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)


# ─────────────────────────────────────────
# WebSocket com ConversationEngine
# ─────────────────────────────────────────

class ConnectionManager:

    def __init__(self):
        self.active = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def send(self, message: str, ws: WebSocket):
        await ws.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):

    await manager.connect(websocket)

    from aios.tutor_core.conversation_engine import ConversationEngine

    engine = ConversationEngine(student_name="Rafael")

    topic_started = False

    try:

        while True:

            data = await websocket.receive_text()
            payload = json.loads(data)

            user_message = payload.get("message", "").strip()
            command = payload.get("command", "")

            if command == "simplify":
                response = engine.simplify()

            elif not topic_started:
                response = engine.start_topic(user_message)
                topic_started = True

            else:
                response = engine.respond(user_message)

            await manager.send(json.dumps({
                "role": "assistant",
                "content": response
            }), websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception as e:
        await manager.send(json.dumps({
            "role": "assistant",
            "content": f"Erro interno: {str(e)}"
        }), websocket)

        manager.disconnect(websocket)


# ─────────────────────────────────────────
# APIs de dados
# ─────────────────────────────────────────

@app.get("/api/progress")
async def get_progress():

    progress_dir = os.path.join(PROJECT_DIR, "data", "progress")

    courses = []

    if os.path.exists(progress_dir):

        for f in os.listdir(progress_dir):

            if f.endswith(".json"):

                with open(os.path.join(progress_dir, f)) as fp:
                    courses.append(json.load(fp))

    return {"courses": courses}


@app.get("/api/agents")
async def get_agents():

    return {
        "agents": [
            {"name": "TutorAgent", "role": "Conduz aulas", "status": "idle"},
            {"name": "CurriculumAgent", "role": "Gera curriculos", "status": "idle"},
            {"name": "ResearchAgent", "role": "Pesquisa conteudo", "status": "idle"},
        ]
    }


@app.get("/api/memory")
async def get_memory():

    memory_file = os.path.join(PROJECT_DIR, "memory", "MEMORY.md")

    content = ""

    if os.path.exists(memory_file):

        with open(memory_file) as f:
            content = f.read()

    return {"content": content}
