import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from dotenv import load_dotenv

# v3 Messaging API用
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient, BroadcastRequest, TextMessage

# 環境変数読み込み
load_dotenv()
ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# LINE設定
configuration = Configuration(access_token=ACCESS_TOKEN)

app = Flask(__name__)
scheduler = BackgroundScheduler()

def send_reminder():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    message = f'⏰シフト提出の期限が近づいています！忘れずに提出してください！\nhttps://im3c-cws.company.works-hi.com/self-workflow/cws/mbl/MblActLogin'
    with ApiClient(configuration) as api_client:
        line_bot = MessagingApi(api_client)
        try:
            line_bot.broadcast(
                BroadcastRequest(messages=[TextMessage(text=message)])
            )
            print(f"[{now}] Broadcast sent.")
        except Exception as e:
            print(f"Broadcast failed: {e}")

# 5日と20日 23:00, 23:30, 23:45 に送信
for day in [5, 20, 6]:
    scheduler.add_job(send_reminder, 'cron', day=day, hour=11, minute=0)
    scheduler.add_job(send_reminder, 'cron', day=day, hour=12, minute=0)
    scheduler.add_job(send_reminder, 'cron', day=day, hour=13, minute=0)
    scheduler.add_job(send_reminder, 'cron', day=day, hour=14, minute=0)
    scheduler.add_job(send_reminder, 'cron', day=day, hour=14, minute=15)
    scheduler.add_job(send_reminder, 'cron', day=day, hour=14, minute=30)
    scheduler.add_job(send_reminder, 'cron', day=day, hour=14, minute=45)
    scheduler.add_job(send_reminder, 'cron', day=day, hour=14, minute=50)
    scheduler.add_job(send_reminder, 'cron', day=day, hour=14, minute=55)

scheduler.start()

@app.route("/", methods=["GET", "HEAD"])
def index():
    return "OK"

if __name__ == "__main__":
    send_reminder()  
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))