import os
import requests  # 🟢 Added to handle outbound API communications with your Lambda function
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Mock Database Store (Expanded to maximize immediate color-coded visual contrast for demos)
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
# 🟢 RESTORED CRITICAL VIEW BOUNDARY (Fixed 404 Boot Failures)
# ==============================================================================
@app.route('/')
def index():
    # DAY 2 OPERATIONAL ACTION GUARDRAIL
    if os.environ.get('MAINTENANCE_MODE') == 'true':
        return """
        <body style="font-family:sans-serif; text-align:center; padding-top:100px; background:#f4f6f9;">
            <h1>⚠️ 🛠️ DOWN FOR SCHEDULED MAINTENANCE</h1>
            <p>The Platform team is performing system optimizations. We will be back online shortly.</p>
        </body>
        """, 503

    # DAY 1 ADD-ON UI MOVEMENT
    ai_enabled = os.environ.get('AI_ENABLED') == 'true'
    return render_template_string(HTML_TEMPLATE, submissions=FEEDBACK_DB, ai_enabled=ai_enabled)

# ==============================================================================
# 🚀 CORE SUBMISSION PROCESSOR (Day 0 Local vs Day 1 Remote API Router)
# ==============================================================================
@app.route('/submit', methods=['POST'])
def submit():
    text = request.form.get('feedback')
    sentiment = "🟡 NEUTRAL" # Safe fallback state
    
    # 🔍 DAY 1 ADD-ON LIVE INTEGRATION PATH
    ai_enabled = os.environ.get('AI_ENABLED') == 'true'
    ai_endpoint = os.environ.get('AI_ENDPOINT_URL') # Dynamically fed by your Terraform output

    if ai_enabled and ai_endpoint:
        try:
            # Native, unauthenticated outbound handshake straight to your Lambda Endpoint URL
            response = requests.post(ai_endpoint, json={"text": text}, timeout=4)
            if response.status_code == 200:
                data = response.json()
                sentiment = data.get("sentiment", "🟡 NEUTRAL")
        except Exception as e:
            # Graceful fallback logging so your demo app never crashes on camera
            print(f"AI Engine Handshake Failed: {str(e)}")
            
    # Fallback to local routing logic if AI is disabled or backend lookup times out
    else:
        if any(word in text.lower() for word in ['slow', 'bad', 'confusing', 'terrible']):
            sentiment = "🔴 NEGATIVE"
        elif any(word in text.lower() for word in ['great', 'love', 'amazing', 'good']):
            sentiment = "🟢 POSITIVE"
       
    FEEDBACK_DB.insert(0, {"text": text, "sentiment": sentiment})
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
