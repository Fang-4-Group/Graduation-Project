# ENV setting
Go to anythingllm desktop to generate your own apiley, then paste it to the .env file

# New a workspace
Using the following function and parameter "workspace_name" to create new workspace. API will return the workspace class with workspace_name, slug.
```powershell
create_workspace(api_key, workspace_name):
...
...
  return Workspace(workspace_name, slug)
```
Using this function to get the slug_id of the workspace
```poewshell
workspace.get_slug()
```

# Upload a document(chat record) and get doc_id
Using the following function and parameter "file"(File path) to uplaod new chat record.
```powershell
def upload_document(api_key, file_path):
  return None
```
Using this function to get the doc_id store in DOC class. Using doc.get_doc_id() to get it. In order to update the embeding after this step.
```poweshell
def get_documents():
  return Doc(doc_id=doc_id)
```

# Update embedding
Using the following function to update embedding. You will need slug_id and doc_id we store before for the request.
```powershell
def update_embedding(api_key, slug_id, doc_id):
  return None
```
Using this two class function as input parameter of update_embedding(as slug_id and doc_id)
```powershell
workspace.get_slug()
doc.get_doc_id()
```

# Create new thread
Using the following function to create new thread for chattting. workspace.get_slug() to get slug_id.
```powershell
def creat_new_thread(slug_id):
  return thread_id
```
# Chat
Using the following function and parameter "slug_id, thread_id, message" to chat with llm.
```powershell
def send_chat_message(api_key, slug_id, thread_id, message, mode="chat"):
  return response.json()
```
message should use the llm-promting/promt.txt to chat with the llm.
