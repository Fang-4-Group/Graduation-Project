import json
import os
from datetime import datetime
from typing import Dict, List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.v3.webhook import WebhookHandler
from models import MsgDetail

app = FastAPI()

summary_queue: Dict[str, List[MsgDetail]] = {}

# Get environment variables
load_dotenv()
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))
if line_bot_api is None or handler is None:
    print("Make sure you fill in the right environment variables.")
    exit(1)


# Deal with messages
@app.post("/callback")
async def line_webhook(request: Request):
    body_bytes = await request.body()
    body = json.loads(body_bytes.decode("utf-8"))
    events = body["events"]
    signature = request.headers.get("X-Line-Signature")

    try:
        handler.handle(body_bytes.decode("utf-8"), signature)
    except InvalidSignatureError:
        return JSONResponse(  # noqa
            status_code=400, content={"message": "Invalid signature"}  # noqa
        )  # noqa

    for event in events:
        if (
            event["source"]["type"] == "group"
            and event["message"]["type"] == "text"  # noqa
        ):
            await group_chat(event)
            print("SUMMARY QUEUE:", summary_queue)
        elif (
            event["source"]["type"] == "user"
            and event["message"]["type"] == "text"  # noqa
        ):  # noqa
            await user_chat(event)
        else:
            print("The message is not in form of text.")

    return JSONResponse(status_code=200, content={"message": "OK"})


async def group_chat(event):
    message = event["message"]

    if "groupId" in event["source"]:
        group_id = event["source"]["groupId"]
        user_id = event["source"]["userId"]

        profile = line_bot_api.get_group_member_profile(group_id, user_id)
        user_name = profile.display_name

        # Append the message to the group's queue
        msg_detail = MsgDetail(
            MsgText=message["text"], UserName=user_name, Time=datetime.now()
        )

        if group_id not in summary_queue:
            summary_queue[group_id] = []
        summary_queue[group_id].append(msg_detail)


async def user_chat(events):
    pass


# Webhook endpoint for dialogflow
@app.post("/webhook")
async def webhook(request: Request):
    req_data = await request.json()
    # print out user info
    payload = req_data["originalDetectIntentRequest"]["payload"]
    user_id = payload["data"]["source"]["userId"]
    print(f"User ID: {user_id}")
    try:
        profile = line_bot_api.get_profile(user_id)
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
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text)
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
