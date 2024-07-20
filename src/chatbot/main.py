import os

import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import (  # noqa
    MessageEvent,
    PostbackEvent,
    TextMessage,
    TextSendMessage,
)
from linebot.webhook import WebhookHandler

from src.chatbot.services import (  # noqa
    call_llm_api,
    house_recommendation,
    save_group_msg,
    summary_checklist,
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
        group_message = event.message.text
        print("Group ID: ", group_id)
        result = save_group_msg(user_id, group_id, msg)
        print("MongoDB insert result: ", result)

        if group_message == "@check":
            result = summary_checklist()
            line_bot_api.reply_message(event.reply_token, result)


@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if data == "action=call_llm_api":
        result = call_llm_api()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=result)
        )  # noqa


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
