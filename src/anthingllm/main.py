from fastapi import APIRouter, FastAPI, Request

app = FastAPI()

router = APIRouter(prefix="/linebot")


@router.post("/callback")
async def line_webhook(request: Request):
    return 0
