import asyncio
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import AudioMessage, MessageEvent, TextMessage
from linebot.webhook import WebhookHandler

from src.chatbot.services import (
    handle_async_audio,
    house_recommendation,
    save_group_msg,
)

app = FastAPI()

router = APIRouter(prefix="/linebot")

load_dotenv()
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))


@router.post("/callback")
async def line_webhook(request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")
    signature = request.headers.get("X-Line-Signature")
    try:
        handler.handle(body_str, signature)
    except InvalidSignatureError:
        return JSONResponse(
            status_code=400, content={"message": "Invalid signature"}  # noqa
        )

    return JSONResponse(status_code=200, content={"message": "OK"})


@handler.add(MessageEvent, message=TextMessage)
def text_msg_handler(event):
    user_message = event.message.text
    source_type = event.source.type
    user_id = event.source.user_id
    msg = event.message.text

    if source_type == "user":  # one-on-one chat
        if user_message == "@推薦":
            result = house_recommendation()
            line_bot_api.reply_message(event.reply_token, result)
    elif source_type == "group":  # group chat
        group_id = event.source.group_id
        print("Group ID: ", group_id)
        result = save_group_msg(user_id, group_id, msg)
        print("MongoDB insert result: ", result)


@handler.add(MessageEvent, message=AudioMessage)
def audio_msg_handler(event):
    asyncio.create_task(handle_async_audio(event))


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
