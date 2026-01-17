import json
from models import db

# Badge definitions
BADGES = {
    'first_prediction': {'name': 'First Steps', 'icon': '🎯', 'description': 'Made your first prediction', 'points': 10},
    'verified_user': {'name': 'Verified User', 'icon': '✅', 'description': 'Verified your account', 'points': 20},
    'prediction_master': {'name': 'Prediction Master', 'icon': '🏆', 'description': 'Made 10 predictions', 'points': 50},
    'approved_once': {'name': 'First Approval', 'icon': '💰', 'description': 'Got your first loan approved', 'points': 30},
    'high_score': {'name': 'Credit Champion', 'icon': '⭐', 'description': 'CIBIL score above 750', 'points': 40},
    'calculator_user': {'name': 'Calculator Pro', 'icon': '🧮', 'description': 'Used the calculator', 'points': 15},
    'export_expert': {'name': 'Data Export Expert', 'icon': '📊', 'description': 'Exported your data', 'points': 25},
    'week_streak': {'name': 'Weekly Warrior', 'icon': '🔥', 'description': 'Used the app 7 days in a row', 'points': 100},
}

def award_badge(user, badge_key):
    """Award a badge to a user if they don't already have it"""
    try:
        current_badges = json.loads(user.badges)
    except:
        current_badges = []
    
    if badge_key not in current_badges and badge_key in BADGES:
        current_badges.append(badge_key)
        user.badges = json.dumps(current_badges)
        user.points += BADGES[badge_key]['points']
        db.session.commit()
        return BADGES[badge_key]
    return None

def get_user_badges(user):
    """Get all badges earned by a user"""
    try:
        badge_keys = json.loads(user.badges)
    except:
        badge_keys = []
    
    return [{'key': key, **BADGES[key]} for key in badge_keys if key in BADGES]

def check_and_award_badges(user, predictions=None):
    """Check conditions and award applicable badges"""
    new_badges = []
    
    # First prediction
    if predictions and len(predictions) == 1:
        badge = award_badge(user, 'first_prediction')
        if badge:
            new_badges.append(badge)
    
    # Prediction master
    if predictions and len(predictions) >= 10:
        badge = award_badge(user, 'prediction_master')
        if badge:
            new_badges.append(badge)
    
    # Verified user
    if user.is_verified:
        badge = award_badge(user, 'verified_user')
        if badge:
            new_badges.append(badge)
    
    return new_badges
