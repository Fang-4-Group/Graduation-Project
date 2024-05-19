import json
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.v3.webhook import WebhookHandler

import services

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
        )  # noqa

    body = json.loads(body_str)
    events = body["events"]

    for event in events:
        event_type = event.get("type")
        print(f"Processing event type: {event_type}")
        if event_type == "message":

            if (
                event["source"]["type"] == "group"
                and event["message"]["type"] == "text"
            ):
                group_id = await services.group_chat(event)  # Use the function
                print("-" * 40)
                await services.output_group_msg(group_id)
            elif (
                event["source"]["type"] == "user"
                and event["message"]["type"] == "text"  # noqa  # noqa
            ):
                await services.user_chat(event)
            else:
                print("The message is not in form of text.")

            return JSONResponse(status_code=200, content={"message": "OK"})
        else:
            print(f"Unhandled event type: {event_type}")


@router.post("/webhook")
async def webhook(request: Request):
    req_data = await request.json()
    payload = req_data["originalDetectIntentRequest"]["payload"]
    user_id = payload["data"]["source"]["userId"]
    print(f"User ID: {user_id}")
    try:
        profile = services.line_bot_api.get_profile(user_id)
        print(f"Profile: {profile}")
    except LineBotApiError as error:
        print(f"Error: {error}")

    dialog_res = req_data["queryResult"]["fulfillmentText"]
    response_data = {
        "fulfillmentText": f"{dialog_res} ( 我有經過 FastAPI Server )",
        "source": "webhookdata",
    }
    return JSONResponse(content=response_data, status_code=200)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    services.line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text)
    )


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
