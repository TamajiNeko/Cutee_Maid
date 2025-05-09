import requests
import json
import sys
import os

if len(sys.argv): #Receive arguments send by main.py 
    user_input = sys.argv[1]
    user_id = sys.argv[2]
    user_name = sys.argv[3]
    channel_id = sys.argv[4]

    chat_history = {}

    file_path = os.path.join("history", f"{channel_id}.json") #History directory you can change it

    def load_history():
        global chat_history
        try:
            os.makedirs("history", exist_ok=True)
            
            if os.path.exists(file_path): #load history if exitsts else create new
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
        
        if not chat_history: #To make sure history exitsts
            chat_history = load_history()
        
        if user_id not in chat_history:
            chat_history[user_id] = []
        
        chat_history[user_id].extend([ #Add new message group(user message, AI response) to history for user
            {"role": "user", "content": text},
            {"role": "assistant", "content": ai_response}
        ])
        
        save_history()
        
        return ai_response
    
    API_URL = "YOUR API" #Enter your API URL

    with open("src/prompt.txt", "r", encoding="utf-8") as file: #Open prompt
        SYSTEM_PROMPT = file.read()

    base_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    chat_history = load_history()

    messages = base_messages.copy()
    messages.extend(chat_history.get(user_id, [])[-100:]) #Read last 100 message from user and add to messages group
    messages.append({"role": "user", "content": user_input}) #Add user input to messages group

    response = requests.post( #post messages group to AI
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