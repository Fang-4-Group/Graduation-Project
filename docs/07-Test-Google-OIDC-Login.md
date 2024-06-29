# Test Google OIDC Login

## Prerequisites

- Navigate to the Google Cloud API Credentials page at [Google Cloud Console](https://console.cloud.google.com/apis/credentials?hl=en) and create a new project.
- Follow the instructions on this page to register a client: [Google OAuth 2.0 Integration Guide](https://growingdna.com/google-oauth-2-0-for-3rd-party-login/). Please set two redirect URIs: `http://localhost:7877/google-oidc/auth` and `http://localhost:7877/google-oidc/login`.
- After registering, add yourself as a test user and download the OAuth client JSON file. Rename this file to `client.json` and place it under the `services/google_oidc` directory.

## Steps to Test

1. Update your `.env` file.

```plaintext
# Google OIDC Login Settings
GOOGLE_CLIENT_ID = [YOUR_GOOGLE_CLIENT_ID]
GOOGLE_CLIENT_SECRET = [YOUR_GOOGLE_CLIENT_SECRET]
GOOGLE_REDIRECT_URI = 'http://localhost:7877/google-oidc/auth'
```

2. Start the test environment:

```bash
# Accessing the container's shell
docker exec -it graduation-project /bin/bash
uvicorn src.main:app --host localhost --port 7877 --reload
```

3. Visit [http://localhost:7877/google-oidc/](http://localhost:7877/google-oidc/) to see the test results.

## Expected Results
![homepage](https://github.com/Fang-4-Group/Graduation-Project/assets/82760846/3ed378a0-625e-4371-bdc1-d1d98c930b87)
![login](https://github.com/Fang-4-Group/Graduation-Project/assets/82760846/04228ea1-6fe4-4115-9751-814f1780f49e)
![login-successful](https://github.com/Fang-4-Group/Graduation-Project/assets/82760846/ab909842-d764-4e53-b1ab-9fad6f1050cb)
