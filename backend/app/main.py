import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from app.core.config import settings
from app.api.endpoints_clones import router as clones_router
from app.api.endpoints_llm import router as llm_router
from app.api.endpoints_timeline import router as timeline_router
from app.api.endpoints_render import router as render_router
from app.api.endpoints_social import router as social_router
from app.api.endpoints_radar import router as radar_router
from app.api.endpoints_connections import router as connections_router
from app.api.endpoints_express import router as express_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Estúdio Open Source de Clones Digitais e Vídeos com IA em PT-BR"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas da API
app.include_router(clones_router, prefix=f"{settings.API_PREFIX}/clones", tags=["Clones"])
app.include_router(llm_router, prefix=f"{settings.API_PREFIX}/llm", tags=["LLM & Roteiros"])
app.include_router(timeline_router, prefix=f"{settings.API_PREFIX}/timeline", tags=["Timeline & B-Roll"])
app.include_router(render_router, prefix=f"{settings.API_PREFIX}/render", tags=["Renderização"])
app.include_router(social_router, prefix=f"{settings.API_PREFIX}/social", tags=["Social & Distribuição"])
app.include_router(radar_router, prefix=f"{settings.API_PREFIX}/radar", tags=["Radar & Tendências"])
app.include_router(connections_router, prefix=f"{settings.API_PREFIX}/connections", tags=["Conexões & APIs"])
app.include_router(express_router, prefix=f"{settings.API_PREFIX}/express", tags=["Piloto Automático"])

# Montar pastas estáticas para uploads e vídeos gerados
app.mount("/uploads", StaticFiles(directory=str(settings.UPLOADS_DIR)), name="uploads")
app.mount("/outputs", StaticFiles(directory=str(settings.OUTPUTS_DIR)), name="outputs")

# Caminho para os arquivos do frontend estático
FRONTEND_DIST_DIR = settings.BASE_DIR.parent / "frontend" / "dist"

if FRONTEND_DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST_DIR / "assets")), name="frontend_assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        index_file = FRONTEND_DIST_DIR / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return HTMLResponse("<h1>CloneStudio PT-BR Backend Ativo!</h1>")
else:
    # Servidor integrado com interface HTML/Tailwind embutida de alta performance
    @app.get("/", response_class=HTMLResponse)
    async def serve_embedded_ui():
        ui_file = settings.BASE_DIR / "app" / "static" / "index.html"
        if ui_file.exists():
            return FileResponse(ui_file)
        return HTMLResponse("<h1>CloneStudio PT-BR API Online</h1><p>Acesse <a href='/docs'>/docs</a> para ver a documentação da API.</p>")

@app.get("/health")
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME, "version": settings.VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
