import os
import json  # 🟢 FIXED: Required to safely parse inner stringified Lambda payloads
import requests  
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Mock Database Store 
FEEDBACK_DB = [
    {"text": "Love the new dark mode interface! Incredibly smooth.", "sentiment": "🟢 POSITIVE"},
    {"text": "The onboarding flow is incredibly confusing and slow.", "sentiment": "🔴 NEGATIVE"},
    {"text": "Standard quarterly security patch and platform maintenance run.", "sentiment": "🟡 NEUTRAL"},
    {"text": "This application deployment is amazing and blazing fast!", "sentiment": "🟢 POSITIVE"},
    {"text": "Terrible performance bottlenecks under high container load conditions.", "sentiment": "🔴 NEGATIVE"},
    {"text": "The new analytics dashboard charts render fine.", "sentiment": "🟡 NEUTRAL"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Customer Feedback Portal</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; background: #f4f6f9; }
        .card { background: white; padding: 15px; margin: 10px 0; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; float: right; }
        .btn { background: #0066cc; color: white; padding: 10px; border: none; border-radius: 4px; cursor: pointer; }
        textarea { width: 100%; height: 60px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <h2>📋 Customer Feedback Board</h2>
   
    <form method="POST" action="/submit">
        <textarea name="feedback" placeholder="Enter product feedback here..." required></textarea>
        <button type="submit" class="btn">Submit Feedback</button>
    </form>

    <h3>Recent Submissions</h3>
    {% for item in submissions %}
    <div class="card">
        {% if ai_enabled %}
            <span class="badge">{{ item.sentiment }}</span>
        {% endif %}
        <p>{{ item.text }}</p>
    </div>
    {% endfor %}
</body>
</html>
"""

# ==============================================================================
# 🎛️ SYSTEM CORE ENTRY ROUTER (Consolidated Boundary)
# ==============================================================================
@app.route('/')
def index():
    # A. DAY 2 NATIVE IN-BAND LANDING (Direct out-of-band Lambda data store check)
    ai_endpoint = os.environ.get('AI_ENDPOINT_URL') 
    if ai_endpoint:
        try:
            # Query Lambda function URL synchronously to read the live toggle state
            response = requests.get(ai_endpoint, timeout=2)
            if response.status_code == 200:
                # 🟢 FIXED: Safely unpacks the inner serialized string to clear type mismatches
                lambda_payload = response.json()
                inner_body = json.loads(lambda_payload.get('body', '{}'))
                
                if inner_body.get('maintenance_mode') == 'true':
                    return """
                    <body style="font-family:sans-serif; text-align:center; padding-top:100px; background:#f4f6f9;">
                        <h1>⚠️ 🛠️ DOWN FOR SCHEDULED MAINTENANCE</h1>
                        <p>The Platform team is performing system optimizations. We will be back online shortly.</p>
                    </body>
                    """, 503
        except Exception:
            pass 

    # B. DAY 2 BACKUP LOCAL FALLBACK ENGINE
    if os.environ.get('MAINTENANCE_MODE') == 'true':
        return """
        <body style="font-family:sans-serif; text-align:center; padding-top:100px; background:#f4f6f9;">
            <h1>⚠️ 🛠️ DOWN FOR SCHEDULED MAINTENANCE</h1>
            <p>The Platform team is performing system optimizations. We will be back online shortly.</p>
        </body>
        """, 503

    # C. DAY 1 ADD-ON LOGIC VIEW ACTIVATION
    ai_enabled = os.environ.get('AI_ENABLED') == 'true'
    return render_template_string(HTML_TEMPLATE, submissions=FEEDBACK_DB, ai_enabled=ai_enabled)

# ==============================================================================
# 🚀 RESTORED SUBMISSION HANDSHAKE ROUTE
# ==============================================================================
@app.route('/submit', methods=['POST'])
def submit():
    text = request.form.get('feedback')
    sentiment = "🟡 NEUTRAL" 
    
    ai_enabled = os.environ.get('AI_ENABLED') == 'true'
    ai_endpoint = os.environ.get('AI_ENDPOINT_URL') 

    if ai_enabled and ai_endpoint:
        try:
            response = requests.post(ai_endpoint, json={"text": text}, timeout=4)
            if response.status_code == 200:
                # 🟢 FIXED: Handle parsing safely whether it returns flat body data or proxy data
                lambda_payload = response.json()
                if 'body' in lambda_payload:
                    data = json.loads(lambda_payload['body'])
                else:
                    data = lambda_payload
                
                if "sentiment" in data:
                    sentiment = data.get("sentiment", "🟡 NEUTRAL")
        except Exception as e:
            print(f"AI Engine Handshake Failed: {str(e)}")
            
    else:
        if any(word in text.lower() for word in ['slow', 'bad', 'confusing', 'terrible']):
            sentiment = "🔴 NEGATIVE"
        elif any(word in text.lower() for word in ['great', 'love', 'amazing', 'good']):
            sentiment = "🟢 POSITIVE"
       
    FEEDBACK_DB.insert(0, {"text": text, "sentiment": sentiment})
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
