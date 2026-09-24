# app.py
import os, base64, asyncio
from flask import Flask, render_template_string, request
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()
bot = Bot(os.getenv("BOT_TOKEN"))
CHAT_ID = int(os.getenv("CHAT_ID"))
app = Flask(__name__)

PAGE = """
<h1>Сделать фото (с вашего согласия)</h1>
<p>Нажав кнопку, вы соглашаетесь отправить своё фото.</p>
<video id="v" autoplay playsinline width="320"></video><br>
<button onclick="snap()">📸 Сделать фото и отправить</button>
<script>
navigator.mediaDevices.getUserMedia({video:true}).then(s=>{
  document.getElementById('v').srcObject=s;
});
async function snap(){
  const v=document.getElementById('v');
  const c=document.createElement('canvas');
  c.width=v.videoWidth; c.height=v.videoHeight;
  c.getContext('2d').drawImage(v,0,0);
  const data=c.toDataURL('image/jpeg',0.9).split(',')[1];
  await fetch('/upload',{method:'POST',body:data});
  alert('Отправлено');
}
</script>
"""

@app.route("/")
def index(): return render_template_string(PAGE)

@app.route("/upload", methods=["POST"])
def upload():
    img = base64.b64decode(request.get_data())
    asyncio.run(bot.send_photo(CHAT_ID, img))
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
