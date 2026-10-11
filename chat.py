from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models import Notification
import re

chat = Blueprint('chat', __name__)

# Strict safety guardrails
# These patterns trigger a mandatory refusal to answer
UNSAFE_PATTERNS = [
    r'\bdiagnose',
    r'\bprescription',
    r'\bprescribe',
    r'\bmedication',
    r'\bdrug',
    r'\bpill',
    r'\bsymptom',
    r'\bpain',
    r'\bache',
    r'\btreatment',
    r'\bcure',
    r'\bdoctor',
    r'\bpatient',
    r'\bdisease',
    r'\billness',
    r'\binfection',
    r'\bdose',
    r'\bdosage'
]

SYSTEM_MESSAGE = """
I am the Pharmacy Assistant Chatbot.
I can help you with:
- Store hours and locations
- General services provided
- How to register or login
- Contact information

I CANNOT:
- Diagnose medical conditions
- Prescribe medications
- Recommend medical treatments
"""

def is_safe(message):
    """Check if message contains unsafe keywords"""
    message_lower = message.lower()
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, message_lower):
            return False
    return True

def get_response(message):
    """Simple rule-based response generation (mock AI)"""
    msg = message.lower()
    
    if not is_safe(msg):
        return {
            "text": "I apologize, but I cannot answer medical questions, diagnose conditions, or give advice on medications. Please consult a licensed pharmacist or doctor for medical assistance.",
            "suggest_escalation": True,
            "suggested_actions": ["Contact Pharmacist", "Store Hours"]
        }
    
    # Safe topics
    response_text = ""
    suggested_actions = []
    
    if 'hour' in msg or 'open' in msg or 'time' in msg:
        response_text = "We are open Monday to Friday from 8:00 AM to 10:00 PM, and Weekends from 10:00 AM to 8:00 PM."
        suggested_actions = ["Locations", "Services", "Contact Us"]
    elif 'location' in msg or 'address' in msg or 'where' in msg:
        response_text = "We have branches across the city. Please check the Dashboard for the nearest branch location."
        suggested_actions = ["Store Hours", "Contact Us"]
    elif 'register' in msg or 'sign up' in msg:
        response_text = "You can register for an account by clicking the 'Register' button on the login page."
        suggested_actions = ["Login Help", "Store Hours"]
    elif 'service' in msg:
        response_text = "We offer prescription dispensing, health consultations, and vaccination services."
        suggested_actions = ["Store Hours", "Locations", "Register"]
    elif 'hello' in msg or 'hi' in msg:
        response_text = "Hello! How can I help you today?"
        suggested_actions = ["Store Hours", "Services", "Locations", "Contact Pharmacist"]
    elif 'thank' in msg:
        response_text = "You're welcome! Let me know if you need anything else."
        suggested_actions = ["Store Hours", "Services"]
    elif 'contact pharmacist' in msg or 'pharmacist' in msg:
        response_text = "I can certainly help you connect with a pharmacist. Please click the button below to send a request."
        return {"text": response_text, "suggest_escalation": True, "suggested_actions": ["Store Hours", "Services"]}
    else:
        response_text = "I can help with store hours, locations, and general inquiries. For medical advice, please speak to a pharmacist."
        return {"text": response_text, "suggest_escalation": True, "suggested_actions": ["Store Hours", "Services", "Contact Pharmacist"]}
        
    return {"text": response_text, "suggest_escalation": False, "suggested_actions": suggested_actions}

@chat.route('/api/chat/message', methods=['POST'])
def chat_message():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
        
    response_data = get_response(user_message)
    
    return jsonify({
        'response': response_data['text'],
        'suggest_escalation': response_data.get('suggest_escalation', False),
        'suggested_actions': response_data.get('suggested_actions', []),
        'safe': is_safe(user_message)
    })

@chat.route('/api/chat/escalate', methods=['POST'])
def escalate_chat():
    from app.notifications import create_pharmacist_notification
    data = request.get_json()
    message = data.get('message')
    contact = data.get('contact')
    
    if not message or not contact:
        return jsonify({'error': 'Missing information'}), 400
        
    success = create_pharmacist_notification(message, contact)
    
    if success:
        return jsonify({'message': 'Your request has been sent to a pharmacist. They will contact you shortly.'})
    else:
        return jsonify({'error': 'Failed to notify pharmacist'}), 500

@chat.route('/api/chat/replies', methods=['GET'])
@login_required
def check_replies():
    """Check for pharmacist replies to user inquiries"""
    # Find unread reply notifications
    notifications = Notification.query.filter_by(
        user_id=current_user.id,
        type='pharmacist_reply',
        is_read=False
    ).all()
    
    replies = []
    for note in notifications:
        replies.append({
            'message': note.message,
            'timestamp': note.created_at.strftime('%H:%M')
        })
        note.is_read = True
    
    if replies:
        db.session.commit()
        
    return jsonify({'replies': replies})
