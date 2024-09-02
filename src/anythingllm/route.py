# isort: skip_file
# flake8: noqa
import os  # To handle file path operations

import requests
from dotenv import load_dotenv

"""
create_workspace(api_key, workspace_name)
    workspac_name
    return class.workspace

upload_document(api_key, file_path)
    file_path
    return class.doc

update_raw_text(api_key, raw_text, title)
    raw_text, title
    return class.doc

update_embeddings(api_key, slug, file_path=None, action=None, doc_id=None, title=None)
    slug=workspace.getslug()
    filepath
    action
    doc_id=doc.get_doc_id()
    title

    return response.json

send_chat_message(api_key, slug_id, message, mode)
    slug=workspace.getslug()
    message
    mode

    return response.json

update_topN(api_key, slug_id, topN):
    topN

    return response.json

"""


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
    def __init__(self, doc_id, filename):
        self.doc_id = doc_id
        self.filename = filename

    def get_doc_id(self):
        return self.doc_id

    def get_filename(self):
        return self.filename

    def __repr__(self):
        return f"Doc(id={self.doc_id}, filename={self.filename})"


def create_workspace(api_key, workspace_name):
    api_url = f"{base_url}workspace/new"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    data = {"name": workspace_name}

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            response_data = response.json()
            workspace_name = response_data["workspace"]["name"]
            slug = response_data["workspace"]["slug"]
            return Workspace(workspace_name, slug)
        except (KeyError, ValueError) as e:
            # print(f"Unexpected response format: {e}")
            return None
    else:
        # print(f"Failed to create workspace: {response.status_code}, {response.text}")
        return None


def upload_document(api_key, file_path):
    api_url = f"{base_url}document/upload"
    headers = {"Authorization": f"Bearer {api_key}", "accept": "application/json"}

    try:
        with open(file_path, "rb") as file:
            files = {
                "file": (file_path, file, "text/plain")  # Adjust MIME type if necessary
            }

            response = requests.post(api_url, headers=headers, files=files)

        if response.status_code == 200:
            try:
                response_data = response.json()
                doc_id = response_data["documents"][0]["id"]
                filename = os.path.basename(
                    file_path
                )  # Extract the filename from the file path
                return Doc(doc_id, filename)
            except (KeyError, IndexError, ValueError) as e:
                # print(f"Unexpected response format: {e}")
                return None
        else:
            # print(f"Failed to upload document: {response.status_code}, {response.text}")
            return None

    except FileNotFoundError:
        # print(f"File not found: {file_path}")
        return None


def update_raw_text(api_key, raw_text, title):
    api_url = f"{base_url}document/raw-text"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json",
    }

    data = {
        "textContent": raw_text,
        "metadata": {
            "title": title,
            "keyOne": "valueOne",
            "keyTwo": "valueTwo",
            "etc": "etc",
        },
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            response_data = response.json()
            doc_id = response_data["documents"][0]["id"]
            title = response_data["documents"][0]["title"]
            # print(f"Success to upload raw text: {title}, {raw_text},{doc_id}")
            return Doc(doc_id, title)
        except (KeyError, IndexError, ValueError) as e:
            # print(f"Unexpected response format: {e}")
            return None
    else:
        # print(f"Failed to upload document: {response.status_code}, {response.text}")
        return None


def update_embeddings(
    api_key, slug, file_path=None, action=None, doc_id=None, title=None
):
    api_url = f"{base_url}workspace/{slug}/update-embeddings"
    if file_path:
        filename_with_extension = os.path.basename(file_path)
        document_path = f"custom-documents/{filename_with_extension}-{doc_id}.json"
        print("file")
        print(filename_with_extension)
        print(doc_id)
        print(document_path)

    if title:
        print("raw")
        print(title)
        print(doc_id)
        document_path = f"custom-documents/{title}-{doc_id}.json"
        print(document_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json",
    }

    data = {
        "adds": [document_path] if action == "add" else [],
        "deletes": [document_path] if action == "delete" else [],
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"Embeddings updated successfully.{document_path}")
        return response.json()
    else:
        # print(f"Failed to update embeddings: {response.status_code}, {response.text}")
        return None


def send_chat_message(api_key, slug_id, message, mode="chat"):
    api_url = f"{base_url}workspace/{slug_id}/chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json",
    }

    data = {"message": message, "mode": mode}

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        # print("Chat message sent successfully.")
        return response.json()
    else:
        # print(f"Failed to send chat message: {response.status_code}, {response.text}")
        return None


def update_topN(api_key, slug_id, topN):
    api_url = f"{base_url}workspace/{slug_id}/update"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json",
    }

    data = {"topN": topN}

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        # print(f"topN update successfully. {topN}")
        return response.json()
    else:
        # print(f"Failed update topN: {response.status_code}, {response.text}")
        return None


# Define your API parameters
load_dotenv()
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")
default_path = os.getenv("DEFAULT_PATH")

chat_id = ""
workspace_name = "test_Workspace"
file_path = f"{default_path}{chat_id}"  # Path to the file you want to upload
message = "remote work?"
raw_text = "The shift to remote work has transformed the modern business landscape, offering both opportunities and challenges. With advancements in technology, employees can now work from virtually anywhere, leading to a more flexible and dynamic workforce. This change has enabled companies to tap into a global talent pool, reduce overhead costs, and offer employees a better work-life balance.However, remote work also presents significant challenges. Communication can become fragmented without the ease of face-to-face interactions, leading to potential misunderstandings and a slower decision-making process. Companies must invest in reliable communication tools and establish clear guidelines to maintain productivity and collaboration among remote teams.Moreover, the shift to remote work requires a change in management style. Leaders must trust their employees to manage their time effectively and focus on outcomes rather than hours worked. Building a strong company culture remotely is also challenging, as employees may feel disconnected from their colleagues and the organization’s mission.In conclusion, while remote work offers numerous advantages, it also demands a thoughtful approach to communication, management, and culture. Businesses that successfully navigate these challenges can benefit from a more flexible and diverse workforce, positioning themselves for long-term success in a rapidly changing world."
title = "remote_raw_text"
topN = 20

if __name__ == "__main__":
    # Step 1: Create a workspace
    workspace = create_workspace(api_key, workspace_name)

    if workspace:
        # print(f"Workspace created successfully: {workspace}")

        # Step 2: Upload a document
        doc = upload_document(api_key, file_path)
        doc_raw = update_raw_text(api_key, raw_text, title)
        print(workspace.get_slug())
        print(doc_raw.get_filename())
        print(doc_raw.get_doc_id())
        if doc and doc_raw:
            # Step 3: Update embeddings
            update_response = update_embeddings(
                api_key,
                workspace.get_slug(),
                file_path,
                action="add",
                doc_id=doc.get_doc_id(),
            )
            update_response_raw = update_embeddings(
                api_key,
                workspace.get_slug(),
                action="add",
                doc_id=doc_raw.get_doc_id(),
                title=doc_raw.get_filename(),
            )
            """ if update_response:
                print(f"Embeddings updated successfully for document: {document_path}")
            else:
                print("Failed to update embeddings.") """
            """ if update_response_raw:
                print(f"Embeddings updated successfully for document: {title},{doc_raw.get_filename()}")
            else:
                print("Failed to update embeddings.") """
            # Step 4: update topN
            update_topN(api_key, workspace.get_slug(), topN)
            # Step 5: Send a chat message
            chat_response = send_chat_message(
                api_key, workspace.get_slug(), message=message, mode="chat"
            )

            if chat_response:
                print(f"Chat message response: {chat_response}")
            else:
                print("Failed to send chat message.")
        else:
            print("Failed to upload document.")
    else:
        print("Failed to create workspace.")
