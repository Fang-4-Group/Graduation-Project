import os
from datetime import datetime

import requests
from linebot import LineBotApi

import src.chatbot.models as models
from src.chatbot.database import save_group_msg_to_db
from src.chatbot.message_templates.buttom_template import create_check_button
from src.chatbot.message_templates.carousel_template import (  # noqa
    create_houses_carousel,
)

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))


def save_group_msg(user_id, group_id, msg):
    profile = line_bot_api.get_group_member_profile(group_id, user_id)
    user_name = profile.display_name

    #  Contruct msg data structure
    msg_detail = models.MsgDetail(
        UserId=user_id, UserName=user_name, MsgText=msg, Time=datetime.now()
    )

    # Save msg to DB
    try:
        result = save_group_msg_to_db(group_id, msg_detail)
    except Exception as e:
        result = f"Exception: {e}"
    return result


def house_recommendation():
    your_ip = os.getenv("HOUSE_RECOMMEND_API")
    user_id = 2
    url = f"http://{your_ip}:7877/get_pref_house_lst/{user_id}"
    try:
        response = requests.get(url)
        data_list = response.json()
        carousel_message = create_houses_carousel(data_list["data"])
        result = carousel_message
    except requests.HTTPError as http_err:
        error_message = f"API Request Failed: {http_err}"
        result = error_message
    return result


def summary_checklist():
    buttom_message = create_check_button()
    return buttom_message
