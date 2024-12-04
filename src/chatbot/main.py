import asyncio
import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import (  # noqa
    AudioMessage,
    MessageEvent,
    PostbackEvent,
    TextMessage,
    TextSendMessage,
)
from linebot.webhook import WebhookHandler

from src.chatbot.services import (  # noqa
    build_consensus_document,
    call_llm_api,
    generate_summarized_checklist,
    group_chat_records_to_file,
    handle_async_audio,
    house_recommendation,
    normal_chat,
    save_group_chat_records,
)

from .logconfig import setup_logging

load_dotenv()
setup_logging()

app = FastAPI()
router = APIRouter(prefix="/linebot")

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")


@router.post("/callback")
async def line_webhook(request: Request):
    logging.info(f"CHANNEL_ACCESS_TOKEN: {os.getenv('CHANNEL_ACCESS_TOKEN')}")
    logging.info(f"CHANNEL_SECRET: {os.getenv('CHANNEL_SECRET')}")

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
        else:
            result = normal_chat(user_id, user_message)
            response = result["textResponse"]
            line_bot_api.reply_message(event.reply_token, TextMessage(text=response))

    elif source_type == "group":  # group chat
        group_id = event.source.group_id
        group_message = event.message.text
        logging.info(f"Group ID: {group_id}")

        # Save group chat record to DB and output to file
        save_result = save_group_chat_records(user_id, group_id, msg)
        logging.info(f"Save group msg: {save_result}")
        group_chat_records_to_file(group_id)

        # Update chat records to RAG and summarize
        if group_message == "@check":
            result = generate_summarized_checklist(group_id)
            response = result["textResponse"]
            print("CHECK RESPONSE: ", response)
            url = build_consensus_document(response, group_id)
            line_bot_api.reply_message(event.reply_token, TextMessage(text=url))


@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if data == "action=call_llm_api":
        result = call_llm_api()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=result)
        )  # noqa


@handler.add(MessageEvent, message=AudioMessage)
def audio_msg_handler(event):
    asyncio.create_task(handle_async_audio(event))


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
