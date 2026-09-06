import json
import uuid
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from app.core.config import settings

router = APIRouter()

class CloneProfile(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    video_path: Optional[str] = None
    voice_sample_path: Optional[str] = None
    created_at: str
    tags: List[str] = []

def get_profiles_db_path() -> Path:
    return settings.CLONES_DIR / "profiles.json"

def load_profiles() -> List[dict]:
    db = get_profiles_db_path()
    if not db.exists():
        return []
    try:
        with open(db, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_profiles(profiles: List[dict]):
    db = get_profiles_db_path()
    with open(db, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)

@router.get("/list", response_model=List[dict])
async def list_clones():
    """Lista todos os clones salvos."""
    return load_profiles()

@router.post("/create")
async def create_clone(
    name: str = Form(...),
    description: str = Form(""),
    tags: str = Form(""),
    video: Optional[UploadFile] = File(None),
    voice_sample: Optional[UploadFile] = File(None)
):
    """Cria um novo perfil de clone com vídeo de referência e amostra de voz."""
    clone_id = str(uuid.uuid4())[:8]
    clone_folder = settings.CLONES_DIR / clone_id
    clone_folder.mkdir(parents=True, exist_ok=True)

    video_path_str = None
    if video:
        v_dest = clone_folder / f"reference_{video.filename}"
        with open(v_dest, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        video_path_str = str(v_dest)

    voice_path_str = None
    if voice_sample:
        a_dest = clone_folder / f"voice_{voice_sample.filename}"
        with open(a_dest, "wb") as buffer:
            shutil.copyfileobj(voice_sample.file, buffer)
        voice_path_str = str(a_dest)

    parsed_tags = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    new_profile = {
        "id": clone_id,
        "name": name,
        "description": description,
        "video_path": video_path_str,
        "voice_sample_path": voice_path_str,
        "created_at": str(Path(__file__).stat().st_mtime),
        "tags": parsed_tags
    }

    profiles = load_profiles()
    profiles.append(new_profile)
    save_profiles(profiles)

    return {"status": "success", "profile": new_profile}

@router.delete("/{clone_id}")
async def delete_clone(clone_id: str):
    """Deleta um perfil de clone e seus arquivos associados."""
    profiles = load_profiles()
    filtered = [p for p in profiles if p.get("id") != clone_id]
    if len(filtered) == len(profiles):
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    clone_folder = settings.CLONES_DIR / clone_id
    if clone_folder.exists():
        shutil.rmtree(clone_folder, ignore_errors=True)

    save_profiles(filtered)
    return {"status": "success", "deleted_id": clone_id}
