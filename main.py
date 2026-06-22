import os
import requests
import time

TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}"
REPLY = "Привет! Я сейчас в больнице, отвечу примерно через пару недель. Спасибо за понимание 🙏"

offset = None
print("Автоответчик запущен.")

while True:
    try:
        r = requests.get(f"{API}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=40).json()
        for upd in r.get("result", []):
            offset = upd["update_id"] + 1
            msg = upd.get("business_message")
            if not msg:
                continue
            if msg.get("from", {}).get("is_bot"):
                continue
            requests.post(f"{API}/sendMessage", json={
                "business_connection_id": msg["business_connection_id"],
                "chat_id": msg["chat"]["id"],
                "text": REPLY
            })
    except Exception as e:
        print("Ошибка:", e)
        time.sleep(3)
