from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# 1. محرك توليد الصور (Flux)
@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
            
        url = "https://mu-devs.vercel.app/generate"
        payload = {"prompt": prompt, "model": "flux"}
        
        # إرسال الطلب من السيرفر لتخطي حماية المتصفح
        response = requests.post(url, json=payload, timeout=60)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. محرك الشات (GPT-4o)
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_msg = request.json.get('message', '')
        url = "https://grok.free/wp-admin/admin-ajax.php?action=yescale_chat"
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": user_msg}],
            "stream": False
        }
        response = requests.post(url, json=payload, timeout=30)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
