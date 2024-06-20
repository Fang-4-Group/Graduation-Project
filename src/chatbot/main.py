import json
import os

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.webhook import WebhookHandler

from src.chatbot.message_templates import create_houses_carousel
from src.chatbot.services import group_chat, output_group_msg, user_chat

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

    # body = json.loads(body_str)
    # events = body["events"]

    # for event in events:
    #     event_type = event.get("type")
    #     print(f"Processing event type: {event_type}")
    #     if event_type == "message":

    #         if (
    #             event["source"]["type"] == "group"
    #             and event["message"]["type"] == "text"
    #         ):
    #             group_id = await group_chat(event)
    #             print("-" * 40)
    #             await output_group_msg(group_id)
    #         elif (
    #             event["source"]["type"] == "user"
    #             and event["message"]["type"] == "text"  # noqa
    #         ):
    #             await user_chat(event)
    #         else:
    #             print("The message is not in form of text.")

    #         return JSONResponse(status_code=200, content={"message": "OK"})
    #     else:
    #         print(f"Unhandled event type: {event_type}")


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    body = json.loads("temp")
    print(body)
    if event.source.type == "group":
        group_id = group_chat(event)
        print("-" * 40)
        output_group_msg(group_id)
    elif event.source.type == "user":
        user_chat(event)
    else:
        print("The message is not in form of text.")


@handler.add(MessageEvent, message=TextMessage)
def house_recommendation(event):
    user_message = event.message.text

    if user_message == "@推薦":
        your_ip = "192.168.56.1"  # Replace it with your IP address
        user_id = 2
        url = f"http://{your_ip}:7877/get_pref_house_lst/{user_id}"
        try:
            response = requests.get(url)
            data_list = response.json()
            carousel_message = create_houses_carousel(data_list["data"])
            line_bot_api.reply_message(event.reply_token, carousel_message)
        except requests.HTTPError as http_err:
            error_message = f"API Request Failed: {http_err}"
            print(error_message)
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=error_message)
            )


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
