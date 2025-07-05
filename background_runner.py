import time
from main import run_assistant

def background_loop():
    while True:
        print("🔁 Checking Gmail + Updating messages.json")
        run_assistant()
        time.sleep(600)  

if __name__ == "__main__":
    background_loop()
