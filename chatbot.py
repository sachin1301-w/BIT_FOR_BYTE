"""
AI Chatbot using OpenAI GPT (can work with any LLM)
For demo: uses rule-based responses if no API key
"""

import os
import json

# Try to use OpenAI, fallback to rule-based
try:
    import openai
    HAS_OPENAI = True
    openai.api_key = os.getenv('OPENAI_API_KEY')
except:
    HAS_OPENAI = False

# Rule-based responses for demo without API key
DEMO_RESPONSES = {
    'cibil': "Your CIBIL score is crucial! Aim for 750+ for best approval chances. Pay bills on time, keep credit utilization below 30%, and avoid multiple loan applications.",
    'rejected': "Common rejection reasons: Low CIBIL score, high loan-to-income ratio, insufficient assets. Check your prediction details for personalized recommendations.",
    'improve': "To improve approval chances: 1) Increase your CIBIL score, 2) Reduce loan amount, 3) Add a co-applicant, 4) Increase asset values, 5) Extend loan term.",
    'documents': "Required documents: PAN card, Aadhaar, salary slips (3 months), bank statements (6 months), property papers (if any), employment proof.",
    'income': "Include all sources: salary, rental income, business income, investments. Higher income improves approval chances significantly.",
    'assets': "Assets act as security. Include residential property, commercial property, vehicles, gold, investments. Accurate valuation helps.",
    'eligibility': "Use our Calculator tool for quick eligibility check. Generally, EMI shouldn't exceed 40% of monthly income.",
    'approval': "Approval depends on: CIBIL score (35%), Income vs Loan (30%), Assets (20%), Employment (10%), Dependents (5%).",
}

def get_chatbot_response(user_message, user_context=None):
    """
    Get chatbot response - uses OpenAI if available, else rule-based
    """
    user_message_lower = user_message.lower()
    
    # Try OpenAI first
    if HAS_OPENAI and openai.api_key:
        try:
            context = f"User: {user_context.get('username', 'User')}\n"
            if user_context and user_context.get('last_prediction'):
                context += f"Last Prediction: {user_context['last_prediction']}\n"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful loan advisor assistant. Provide clear, concise advice about loan applications, credit scores, and financial planning. Keep responses under 100 words."},
                    {"role": "user", "content": context + "\n" + user_message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI error: {e}")
            # Fall through to rule-based
    
    # Rule-based fallback
    for keyword, response in DEMO_RESPONSES.items():
        if keyword in user_message_lower:
            return response
    
    # Default response
    return ("I can help with: CIBIL scores, loan rejections, approval tips, required documents, income calculation, "
            "asset evaluation, and eligibility checks. What would you like to know?")

def get_loan_advice(prediction_data):
    """Generate specific advice based on prediction data"""
    advice = []
    
    if prediction_data['cibil_score'] < 700:
        advice.append("🎯 Priority: Improve your CIBIL score to 750+ for better approval chances.")
    
    loan_to_income = prediction_data['loan_amount'] / prediction_data['income_annum']
    if loan_to_income > 4:
        advice.append("💡 Your loan amount is high relative to income. Consider reducing it or increasing income sources.")
    
    total_assets = (prediction_data.get('residential_assets_value', 0) + 
                   prediction_data.get('commercial_assets_value', 0) + 
                   prediction_data.get('luxury_assets_value', 0))
    if total_assets < prediction_data['loan_amount'] * 0.3:
        advice.append("🏠 Building assets will strengthen your application. Consider increasing asset documentation.")
    
    if not advice:
        advice.append("✅ Your profile looks strong! Keep maintaining good financial habits.")
    
    return advice
