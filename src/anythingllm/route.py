# isort: skip_file
# flake8: noqa
import os  # To handle file path operations

import requests
from dotenv import load_dotenv


import requests

""" # testing setup
default_path = "C:/Users/User/Desktop/api_test.txt"
message = "how to install mod?"
# env
base_url = "http://localhost:3001/api/"
api_key = "17FYQX0-BZA4W8T-M7KH3AY-VW7035V" """

# Define your API parameters
load_dotenv()
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")
default_path = os.getenv("DEFAULT_PATH")

# test
message = "how to install mod?"


class Workspace:
    def __init__(self, name, slug):
        self.name = name
        self.slug = slug

    def get_name(self):
        return self.name

    def get_slug(self):
        return self.slug

    def __repr__(self):
        return f"Workspace(name={self.name}, slug={self.slug})"


class Doc:
    def __init__(self, doc_id):
        self.doc_id = doc_id

    def get_doc_id(self):
        return self.doc_id

    """ def get_filename(self):
        return self.filename """

    def __repr__(self):
        return f"Doc(id={self.doc_id}, filename={self.filename})"


def create_workspace(api_key, workspace_name):
    api_url = f"{base_url}workspace/new"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    data = {"name": workspace_name}

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            response_data = response.json()
            workspace_name = response_data["workspace"]["name"]
            slug = response_data["workspace"]["slug"]
            slug_id = slug
            print()
            print("Create new workspace(name,slug):", workspace_name, slug_id)
            return Workspace(workspace_name, slug)
        except (KeyError, ValueError) as e:
            print(f"Unexpected response format: {e}")
            return None
    else:
        print(f"Failed to create workspace: {response.status_code}, {response.text}")
        return None


def upload_document(api_key, file_path):
    api_url = f"{base_url}/workspace/document/upload"
    # 設定 headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        # "Content-Type": "multipart/form-data; boundary=<calculated when request is sent>",
        "User-Agent": "PostmanRuntime/7.42.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    # 設定要上傳的檔案
    files = {
        "file": (file_path, open(file_path, "rb")),
    }

    # 發送 POST 請求
    response = requests.post(api_url, headers=headers, files=files)
    print()
    print("upload_doc:", response)


def get_documents():
    api_url = f"{base_url}system/local-files"
    headers = {
        "User-Agent": "PostmanRuntime/7.42.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        try:
            # print("Response JSON:", response.json())
            items = response.json()["localFiles"]["items"]
            if items:
                custom_documents = items[0]["items"]
                if custom_documents:
                    doc_id = custom_documents[0]["name"]
                    print()
                    print("Get_documents:", doc_id)
                    return Doc(doc_id=doc_id)
        except ValueError:
            print("Failed to parse JSON. Response text:", response.text)
    else:
        print(f"Failed to fetch data: {response.status_code}, {response.reason}")
        print("Response Text:", response.text)


def update_embedding(api_key, slug_id, doc_id):
    api_url = f"{base_url}workspace/{slug_id}/update-embeddings"
    # 設定 headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "*/*",
    }

    data = {"adds": [f"custom-documents/{doc_id}"], "deletes": []}

    # 發送 POST 請求
    response = requests.post(api_url, headers=headers, json=data)
    print()
    print("update_embeddings:", response)


def creat_new_thread(slug_id):
    api_url = f"{base_url}workspace/{slug_id}/thread/new"
    # 設定 headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "*/*",
    }
    response = requests.post(api_url, headers=headers)
    response_data = response.json()
    thread_id = response_data.get("thread", {}).get("slug", None)
    print()
    print("creat_new_thread:", response, thread_id)
    return thread_id


def send_chat_message(api_key, slug_id, thread_id, message, mode="chat"):
    api_url = f"{base_url}v1/workspace/{slug_id}/thread/{thread_id}/chat"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    data = {"message": message, "mode": mode}

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        print("Chat message sent successfully.")
        return response.json()
    else:
        print("ERROR: ", response.text)
        print(f"Failed to send chat message: {response.status_code}")
        return None


if __name__ == "__main__":
    workspace = create_workspace(api_key=api_key, workspace_name="api_test")
    upload_document(api_key=api_key, file_path=default_path)
    doc = get_documents()
    update_embedding(api_key, workspace.get_slug(), doc.get_doc_id())
    thread_id = creat_new_thread(workspace.get_slug())
    ans = send_chat_message(
        api_key, workspace.get_slug(), thread_id=thread_id, message=message, mode="chat"
    )
    print(ans)

if __name__ == "__main__":
    workspace = create_workspace(api_key=api_key, workspace_name="api_test")
    upload_document(api_key=api_key, file_path=default_path)
    doc = get_documents()
    update_embedding(api_key, workspace.get_slug(), doc.get_doc_id())
    thread_id = creat_new_thread(workspace.get_slug())
    ans = send_chat_message(
        api_key, workspace.get_slug(), thread_id=thread_id, message=message, mode="chat"
    )
    print(ans)
