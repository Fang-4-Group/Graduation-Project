import os
from datetime import datetime

from linebot import LineBotApi

import database
import src.chatbot.models as models

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))


async def group_chat(event):
    message = event["message"]

    if "groupId" in event["source"]:
        group_id = event["source"]["groupId"]
        user_id = event["source"]["userId"]

        profile = line_bot_api.get_group_member_profile(group_id, user_id)
        user_name = profile.display_name

        msg_detail = models.MsgDetail(
            UserId=user_id,
            UserName=user_name,
            MsgText=message["text"],
            Time=datetime.now(),
        )

        try:
            await database.add_message_to_group(group_id, msg_detail)
            print(f"Insert message to {group_id} successfully.")
        except Exception as e:
            print(f"Exception: {e}")
    return group_id


async def user_chat(events):
    pass


async def output_group_msg(group_id):
    messages = await database.select_all_group_msg(group_id)
    for message in messages:
        print("FROM MONGO DB:", message)
