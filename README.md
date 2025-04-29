# AndroidTVControllerForPc

#### This code implements a GUI-based Android TV remote control application using PyQt5. It allows users to connect to Android TVs via ADB (Android Debug Bridge) over IP, send text, and control the TV using navigation buttons.
---
### Any Android TV that supports ADB (Android Debug Bridge) over IP should be compatible with this app. (tested on Xiaomi Mi Box)
---
## In-app images:

![image](https://github.com/user-attachments/assets/6faf6767-30d3-4788-ab92-2af522152d15)

![image](https://github.com/user-attachments/assets/7089aee1-f789-43fc-b678-2814cc2dc57f)

---
# How to add or edit languages


You can add and edit languages in translations.json (C:\Users\YOURUSER\Documents\AndroidTVController) with Notepad or any text editor. 
Simply copy this structure, modify just the right texts and the language name.

    "English": {
        "status_disconnected": "● Disconnected",
        "status_connected": "● Connected",
        "text_input_placeholder": "Text to send",
        "send": "Send",
        "connect_to_ip": "Connect to IP",
        "connect": "Connect",
        "disconnect_device": "Disconnect device",
        "previous_connections": "Previous connections:",
        "no_previous_connections": "No previous connections.",
        "language": "Language:",
        "close_settings": "Close settings",
        "connection_success": "Connection successful",
        "connection_error": "Connection error",
        "disconnected": "Disconnected"
    }

like this:

	"Português": {
        "status_disconnected": "● Off-line",
        "status_connected": "● Conectado",
        "text_input_placeholder": "Texto para enviar",
        "send": "Enviar",
        "connect_to_ip": "Conecte-se ao IP",
        "connect": "Conectar",
        "disconnect_device": "Desconectar dispositivo",
        "previous_connections": "Conexões anteriores:",
        "no_previous_connections": "Nenhuma conexão anterior.",
        "language": "Linguagem:",
        "close_settings": "Fechar configurações",
        "connection_success": "Conexão bem-sucedida",
        "connection_error": "Erro de conexão",
        "disconnected": "Desconectado"
    }

then paste your new language after the last language like this 

![image](https://github.com/user-attachments/assets/730c8b3b-cad5-4dad-96c3-701742bc99b5)

and don't forge the ","

![image](https://github.com/user-attachments/assets/6deda782-503e-46de-a7cf-0834261efb09)


if you change text in the left section
![image](https://github.com/user-attachments/assets/442c1f10-b489-4d77-bf99-60c5c420fb39)
it would look like this in the app
![image](https://github.com/user-attachments/assets/535d5abb-1995-448d-adca-2085dfab2268)

If something breaks really badly, just erase translations.json, and it should create it again when you open the app.
