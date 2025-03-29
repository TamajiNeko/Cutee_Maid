import requests
import json
import sys
import os

from dotenv import load_dotenv

if len(sys.argv):
    user_input = sys.argv[1]
    user_id = sys.argv[2]
    channel_id = sys.argv[3]

    chat_history = {}

    file_path = os.path.join("history", f"{channel_id}.json")

    def load_history():
        global chat_history
        try:
            os.makedirs("history", exist_ok=True)
            
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    chat_history = json.load(f)
            else:
                chat_history = {}
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(chat_history, f, indent=2)
            return chat_history
        except json.JSONDecodeError:
            chat_history = {}
            return chat_history

    def save_history():
        os.makedirs("history", exist_ok=True)
        with open(file_path, 'w', encoding="utf-8") as f:
            json.dump(chat_history, f, indent=2, ensure_ascii=False)

    def user_history(user_id, text):
        global chat_history
        
        if not chat_history:
            chat_history = load_history()
        
        if user_id not in chat_history:
            chat_history[user_id] = []
        
        messages = chat_history[user_id][-100:]
        messages.append({"role": "user", "content": text})
        
        
        chat_history[user_id].extend([
            {"role": "user", "content": text},
            {"role": "assistant", "content": ai_response}
        ])
        
        save_history()
        
        return ai_response
    
    API_URL = "YOUR API"

    with open("prompt.txt", "r", encoding="utf-8") as file:
        SYSTEM_PROMPT = file.read()

    base_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    chat_history = load_history()

    messages = base_messages.copy()
    messages.extend(chat_history.get(user_id, [])[-50:])
    messages.append({"role": "user", "content": user_input})

    response = requests.post(
        API_URL,
        json={
            "model": "openchat-3.6-8b-20240522",
            "messages": messages,
            "temperature": 1,
        }
    )

    if response.status_code == 200:
        ai_response = response.json()["choices"][0]["message"]["content"]
        chat_history = load_history()
        user_history(user_id,user_input)
        print(ai_response)