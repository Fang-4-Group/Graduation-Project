# For Windows Developers

If you are using Windows, you will need to enable the Windows Subsystem for Linux (WSL) feature. Here’s a step-by-step guide:

## 1. Install WSL

```bash
# Follow the instructions here: https://learn.microsoft.com/zh-tw/windows/wsl/install
wsl --install
```

## 2. Set up Docker Desktop
[Official guide](https://learn.microsoft.com/zh-tw/windows/wsl/tutorials/wsl-containers) to configure Docker Desktop.

## 3. Clone the Project
Clone this project into the path `\\wsl.localhost\Ubuntu\home\${username}`, as shown below:
![image](https://github.com/Fang-4-Group/Graduation-Project/assets/104518723/5a5d7e10-d845-4882-b568-522d0c36502d)

## 4. Open the Project
Open the project from the WSL file system, preferably using Visual Studio Code:
![image](https://github.com/Fang-4-Group/Graduation-Project/assets/104518723/127b6a3f-5bc0-47d5-9ca8-6ec60f0e1ac2)

## 5. Settings in the vscode
- open setting of vscode
- search `security.allowedUNCHosts`
- click Add item, and fill in `wsl.localhost`
