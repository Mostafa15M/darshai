from flask import Flask, render_template, request, jsonify
import requests
import uuid
import hashlib
import time

app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

# 1. أداة إنشاء الصور (Flux AI)
@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    try:
        prompt = request.json.get('prompt', 'Messi rides a donkey')
        url = "https://mu-devs.vercel.app/generate"
        headers = {"content-type": "application/json", "user-agent": "Mozilla/5.0"}
        data = {"prompt": prompt, "model": "flux"}
        response = requests.post(url, headers=headers, json=data, timeout=30).json()
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. أداة تحسين النصوص (Humanize AI)
@app.route('/api/humanize', methods=['POST'])
def humanize():
    try:
        text = request.json.get('text', '')
        uid = uuid.uuid4().hex
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Origin": "https://humanize.im",
            "uniqueid": uid
        }
        resp = requests.post("https://api.humanize.im/api/v1/chat/humanizedChat", 
                             headers=headers, json={"prompt": text}, timeout=20).json()
        return jsonify(resp)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. محرك البحث الذكي (Grok/GPT)
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        message = request.json.get('message', '')
        url = "https://grok.free/wp-admin/admin-ajax.php?action=yescale_chat"
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": message}],
            "max_tokens": 1000,
            "temperature": 0.7,
            "stream": False
        }
        res = requests.post(url, json=data, timeout=20).json()
        return jsonify({"content": res['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
