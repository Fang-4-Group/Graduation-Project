import json
import logging

# flake8:noqa
import os
from datetime import datetime
from io import BytesIO
from xml.dom.minidom import Document

import requests
import speech_recognition as sr
from docx import Document
from dotenv import load_dotenv
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from linebot import LineBotApi
from linebot.models import TextSendMessage
from pydub import AudioSegment

import src.chatbot.models as models
from src.chatbot.database import (
    get_group_chat_records_by_id,
    save_group_chat_records_to_db,
)
from src.chatbot.message_templates.buttom_template import create_check_button
from src.chatbot.message_templates.carousel_template import (  # noqa
    create_houses_carousel,
)

from .logconfig import setup_logging

setup_logging()
load_dotenv()

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))

json_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f'Bearer {os.getenv("API_KEY")}',
}
multipart_headers = {
    "Accept": "application/json",
    "Authorization": f'Bearer {os.getenv("API_KEY")}',
}


def save_group_chat_records(user_id, group_id, msg):
    profile = line_bot_api.get_group_member_profile(group_id, user_id)
    user_name = profile.display_name
    msg_detail = models.MsgDetail(
        UserId=user_id, UserName=user_name, MsgText=msg, Time=datetime.now()
    )
    try:
        result = save_group_chat_records_to_db(group_id, msg_detail)
    except Exception as e:
        result = f"Exception: {e}"
    return result


def group_chat_records_to_file(group_id):
    try:
        chat_record_list = get_group_chat_records_by_id(group_id)
        os.makedirs("./src/chatbot/group_chat_records/", exist_ok=True)
        with open(
            f"./src/chatbot/group_chat_records/{group_id}.json", "w"
        ) as file:  # noqa
            json.dump(chat_record_list, file, indent=4)
    except Exception as e:
        print(f"Failed to transfer chat records to file: {e}")


def __create_rag_workspace(group_id):
    url = f'{os.getenv("BASE_URL")}workspace/new'
    data = {"name": f"{group_id}'s workspace"}
    response = requests.post(url, headers=json_headers, json=data)
    response_data = response.json()
    slug_id = response_data.get("workspace", {}).get("slug")
    if slug_id is not None:
        return slug_id
    else:
        error = response_data.get("error", None)
        logging.error(f"Failed to create workspace: {error}")
        raise Exception(f"Failed to create workspace: {error}")


def __upload_group_chat_records_file(group_id):
    url = f'{os.getenv("BASE_URL")}document/upload'
    file_path = f"./src/chatbot/group_chat_records/{group_id}.json"
    with open(file_path, "rb") as file:
        files = {"file": (os.path.basename(file_path), file)}
        response = requests.post(url, files=files, headers=multipart_headers)
        response_data = response.json()
        print("RESPONSE DATA: ", response_data)
        doc_id = response_data["documents"][0]["id"]
        return doc_id


def __group_chat_summarize(slug_id):
    with open("llm-promting/prompt.txt", "r", encoding="utf-8") as file:
        prompt_message = file.read().strip()

    url = f'{os.getenv("BASE_URL")}workspace/{slug_id}/chat'
    data = {"message": prompt_message, "mode": "chat"}
    response = requests.post(url, json=data, headers=json_headers)
    return response.json()


def __update_rag_embeddings(slug_id, doc_id, file_name):
    url = f'{os.getenv("BASE_URL")}workspace/{slug_id}/update-embeddings'
    data = {
        "adds": [f"custom-documents/{file_name}-{doc_id}.json"],
        "deletes": [""],
    }  # noqa
    response = requests.post(url, json=data, headers=json_headers)
    return response.json()


def generate_summarized_checklist(group_id):
    slug_id = __create_rag_workspace(group_id)
    logging.info(f"Successfully created workspace. [slug id: {slug_id}]")

    # Update file to RAG
    doc_id = __upload_group_chat_records_file(group_id)
    logging.info(f"Successfully update file to rag. [doc_id: {doc_id}]")

    # Update embeddings
    embeddings_response = __update_rag_embeddings(slug_id, doc_id, group_id)
    logging.info(f"Successfully update embeddings. {embeddings_response}")

    # Summarize
    summarize_response = __group_chat_summarize(slug_id)
    logging.info(f"Successfully update embeddings. {summarize_response}")

    return summarize_response


def summary_checklist():
    buttom_message = create_check_button()
    return buttom_message


def call_llm_api():
    result = "call_llm_api()"
    return result


# Recommendation related services
def house_recommendation():
    your_ip = os.getenv("HOUSE_RECOMMEND_API")
    user_id = 2
    url = f"{your_ip}/get_recommendation/0/{user_id}"
    try:
        response = requests.get(url)
        data_list = response.json()
        carousel_message = create_houses_carousel(data_list)
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
    doc.add_heading("青銀共居協議書", 0).alignment = 1

    sections = input_text.strip().split("**")[1:-1]
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

    # TODO: change the file path to cloud storage path
    file_path = "src/chatbot/contract.docx"
    doc.save(file_path)

    return FileResponse(path=file_path, filename="Rental_Contract.docx")
