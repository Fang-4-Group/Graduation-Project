# isort: skip_file
from typing import List

import httpx

# flake8: noqa
from fastapi import APIRouter, FastAPI, File, HTTPException, Request, UploadFile

app = FastAPI()

router = APIRouter(prefix="/anythingllm")

API_KEY = "236B76T-B694TWM-G78QPR0-GMFCJQW"

url_first = "http://localhost:3001/api/"


@router.post("/workspace/new")
async def create_new_workspace(request: Request):
    url = f"{url_first}v1/workspace/new"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"name": (await request.json()).get("name")}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code)
    return response.json()


@router.post("/document/upload")
async def upload_document(file: UploadFile = File(...)):
    url = f"{url_first}v1/document/upload"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "multipart/form-data",
    }
    files = {"file": (file.filename, await file.read(), file.content_type)}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, files=files)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code)
    return response.json()


@router.post("/workspace/{workspace_slug}/update-embeddings")
async def update_embeddings(workspace_slug: str, adds: List[str]):
    url = f"{url_first}v1/workspace/{workspace_slug}/update-embeddings"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"adds": adds}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code)
    return response.json()


@router.post("/workspace/{workspace_slug}/chat")
async def chat(workspace_slug: str, message: str):
    url = f"{url_first}v1/workspace/{workspace_slug}/chat"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"message": message, "mode": "chat"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code)
    return response.json()
