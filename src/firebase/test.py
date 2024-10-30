import firebase_admin
from firebase_admin import credentials, storage

# 1. 初始化 Firebase Admin SDK
cred = credentials.Certificate(
    "src/firebase/fang5-group-firebase-adminsdk-d81ae-4daed4fca8.json"
)
firebase_admin.initialize_app(cred, {"storageBucket": "fang5-group.appspot.com"})

# 2. 設置要上傳的文件路徑和在 Firebase Storage 中的名稱
file_name = "src/firebase/Test123.docx"
blob_name = "uploads/my_document.docx"  # Firebase Storage 中的檔案路徑

# 3. 獲取儲存桶（bucket）並上傳文件
bucket = storage.bucket()
blob = bucket.blob(blob_name)
blob.upload_from_filename(file_name)

# 4. 設置該文件的公開訪問權限
blob.make_public()

# 5. 獲取文件的公開 URL
url = blob.public_url

print(f"File uploaded successfully. URL: {url}")
