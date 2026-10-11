import os
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Mock Database Store (Keeps the demo lightning fast and stateful)
FEEDBACK_DB = [
    {"text": "The onboarding flow is incredibly confusing and slow.", "sentiment": "🔴 NEGATIVE"},
    {"text": "Love the new dark mode interface!", "sentiment": "🟢 POSITIVE"}
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

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form.get('feedback')
    sentiment = "🟡 NEUTRAL"
    if any(word in text.lower() for word in ['slow', 'bad', 'confusing', 'terrible']):
        sentiment = "🔴 NEGATIVE"
    elif any(word in text.lower() for word in ['great', 'love', 'amazing', 'good']):
        sentiment = "🟢 POSITIVE"
       
    FEEDBACK_DB.insert(0, {"text": text, "sentiment": sentiment})
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
