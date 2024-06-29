# Chatbot Setup

## Prerequisites

Before setting up the chatbot, complete the following prerequisites:
- Create a [LINE Developers Account](https://account.line.biz/login?redirectUri=https%3A%2F%2Fdevelopers.line.biz%2Fconsole%2Fchannel%2Fnew%3Ftype%3Dline-login) and request role access.
- Download [ngrok](https://ngrok.com/download), a tool that will expose your local development server to the Internet.
- Add the official LINE account as a friend using the QR code below:
  ![QR code](https://github.com/Fang-4-Group/Graduation-Project/assets/82760846/c369e78a-5553-424e-8ac5-8b0042772d66)

## Configuration

Configure environment settings before running the chatbot service:

```powershell
# Copy the example.env, rename it to .env, and set the required environment variables:
# These values are found in the LINE Developers Console.
CHANNEL_SECRET=[YOUR_CHANNEL_SECRET]
CHANNEL_ACCESS_TOKEN=[YOUR_CHANNEL_ACCESS_TOKEN]

HOUSE_RECOMMEND_API = [YOUR_IP_ADDR]

MONGO_URI=mongodb://mongodb:27017
MONGO_DB_NAME=Graduation-Project
MONGO_COLLECTION=group-chat-record
```

Run the chatbot using the following command in the project root:

```bash
# Accessing the container's shell
docker exec -it graduation-project /bin/bash

# Starting the API service with Uvicorn on localhost
uvicorn src.chatbot.main:app --host 0.0.0.0 --port 8080 --reload
```

## ngrok Setup

Expose your local server to the Internet using ngrok:

```powershell
# Execute ngrok
ngrok authtoken [YOUR_AUTH_TOKEN]  # Authenticate your ngrok session
ngrok http 8080  # Expose local port 8080 to the Internet
```

Update the generated ngrok URL in LINE Developers Settings (e.g., https://xxxxxx.ngrok-free.app/linebot/callback) to update the webhook URL for real-time communication.

Now you can try to add the official account to a group and send some messages to the group.

## Expected Result

If everything is set up correctly, every message you send will be saved to MongoDB and will be retrieved and printed to console.

![Test Success](https://github.com/Fang-4-Group/Graduation-Project/assets/82760846/1675bee8-4d68-473c-bb01-e80ae1474632)
