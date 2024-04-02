import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.v3.webhook import WebhookHandler

app = FastAPI()

# get environment variables
load_dotenv()
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))
if line_bot_api is None or handler is None:
    print("Make sure you have the right environment variables.")


@app.post("/callback")
async def line_webhook(request: Request):
    body = await request.body()
    signature = request.headers["X-Line-Signature"]

    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        return JSONResponse(  # noqa
            status_code=400, content={"message": "Invalid signature"}  # noqa
        )  # noqa
    return JSONResponse(status_code=200, content={"message": "OK"})


# webhook endpoint for dialogflow
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
