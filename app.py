# app.py
from flask import Flask, request
import importlib.util
import sys
import os
import telegram

# ------------------------
# استيراد الإعدادات من ملف config.py
# يجب أن يحتوي config.py على: TOKEN = "xxx", CHANNEL_ID = "xxx", وغيرها
import config

TOKEN = config.TOKEN
WEBHOOK_PATH = f"/{TOKEN}"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# ------------------------
# وظيفة لاستدعاء bot.py
def run_bot(update):
    spec = importlib.util.spec_from_file_location("bot", os.path.join(os.path.dirname(__file__), "bot.py"))
    bot_module = importlib.util.module_from_spec(spec)
    sys.modules["bot"] = bot_module
    spec.loader.exec_module(bot_module)

    # إذا bot.py يحتوي دالة main أو أي دالة استقبال، نفذها هنا
    if hasattr(bot_module, "main"):
        bot_module.main(update)
    else:
        # إذا bot.py يعمل مباشرة مع التحديثات، يمكن تجاهل هذا الجزء
        pass

# ------------------------
# استقبال التحديثات من Telegram
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    run_bot(update)
    return "ok"

# ------------------------
if __name__ == "__main__":
    app.run()
