from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# 1. محرك توليد الصور (Pollinations AI - المجاني البديل لـ Muapi)
@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        if not prompt:
            return jsonify({"error": "الوصف مطلوب"}), 400
            
        # تحسين الوصف لضمان جودة سينمائية
        enhanced_prompt = f"{prompt}, cinematic lighting, 8k, highly detailed, professional photography"
        # تحويل النص لرابط متوافق مع الـ URL
        safe_prompt = requests.utils.quote(enhanced_prompt)
        
        # رابط الصورة المباشر
        image_url = f"https://pollinations.ai/p/{safe_prompt}?width=1024&height=1024&model=flux"
        
        return jsonify({"url": image_url})
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
