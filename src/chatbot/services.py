# flake8:noqa
import os
from datetime import datetime
from io import BytesIO
from xml.dom.minidom import Document

import requests
import speech_recognition as sr
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from linebot import LineBotApi
from linebot.models import TextSendMessage
from pydub import AudioSegment

import src.chatbot.models as models
from src.chatbot.database import save_group_msg_to_db
from src.chatbot.message_templates import create_houses_carousel

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


async def voice_recognition(msg_id):
    result_content = ""
    try:
        message_content = line_bot_api.get_message_content(msg_id)
        m4a_audio_bytes_io = BytesIO()
        for chunk in message_content.iter_content():
            m4a_audio_bytes_io.write(chunk)
        m4a_audio_bytes_io.seek(0)

        request_audio = AudioSegment.from_file(m4a_audio_bytes_io, format="M4A")
        wav_audio_bytes_io = request_audio.export(format="wav")
        r = sr.Recognizer()
        with sr.AudioFile(wav_audio_bytes_io) as source:
            recognizer_audio = r.record(source)
        result_content = await run_in_threadpool(
            lambda: r.recognize_google(recognizer_audio, language="zh-TW")
        )
    except Exception as e:
        result_content = f"Failed to recognize audio. {e}"

    return result_content


async def handle_async_audio(event):
    try:
        msg_id = event.message.id
        recognized_text = await voice_recognition(msg_id)

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=recognized_text)
        )

    except Exception as e:
        print(f"Errors occurred when handling async audio: {e}")


async def build_consensus_document(input_text):
    doc = Document()
    doc.add_heading("青銀共居協議書", 0).alignment = 1  # Large title, centered

    sections = input_text.strip().split("**")
    for section in sections:
        if section.strip():
            heading, *content = section.split("\n")
            doc.add_heading(heading.strip(), level=2)
            for line in content:
                if line.strip().startswith("*"):
                    line_content = line.strip().lstrip("*").strip()
                    doc.add_paragraph(line_content, style="ListBullet")
                elif line.strip().startswith("+"):
                    line_content = line.strip().lstrip("+").strip()
                    doc.add_paragraph(line_content, style="ListBullet2")

    file_path = "src/chatbot/contract.docx"
    doc.save(file_path)

    return FileResponse(path=file_path, filename="Rental_Contract.docx")
