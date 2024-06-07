import logging
import os
from datetime import datetime
from io import BytesIO

import aiohttp
import models
import speech_recognition as sr
from linebot import LineBotApi, WebhookParser
from linebot.models import TextSendMessage
from pydub import AudioSegment

import database

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
parser = WebhookParser(os.getenv("CHANNEL_SECRET"))

# Build aiohttp session
session = aiohttp.ClientSession()
async_http_client = aiohttp.ClientSession()


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


async def recognize_audio(replay_token, line_message_id):
    """
    Recognize the speech from a Line app audio message.
    """
    try:
        message_content = await line_bot_api.get_message_content(
            line_message_id
        )  # noqa
        audio_bytes_io = BytesIO()
        async for chunk in message_content.iter_content():
            audio_bytes_io.write(chunk)
        audio_bytes_io.seek(0)

        audio_segment = AudioSegment.from_file(audio_bytes_io, format="m4a")
        wav_audio = audio_segment.export(format="wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_audio) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="zh-TW")

        await line_bot_api.reply_message(
            replay_token, TextSendMessage(text=text)
        )  # noqa
    except Exception as e:
        logging.error(f"Error in recognize_audio: {e}")
        await line_bot_api.reply_message(
            replay_token,
            TextSendMessage(text="Sorry, I couldn't understand the audio."),
        )
