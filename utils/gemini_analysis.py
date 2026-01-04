import google.generativeai as genai
import json

def analyze_text(text):
    """
    Analyzes text using Gemini AI for scams, misinformation, and manipulation.
    Returns a structured analysis with scores and explanations.
    """
    
    # Create the prompt for Gemini with better scoring instructions
    prompt = f"""
You are a digital literacy expert. Analyze the following text for potential scams, misinformation, and manipulation tactics.

IMPORTANT SCORING GUIDELINES:
- Be realistic and context-aware. Not all urgency or emotional language is malicious.
- Legitimate marketing uses urgency, discounts, and emotional appeals - this is NORMAL.
- Only flag phrases that are genuinely deceptive or manipulative, not standard business communication.
- Consider the CONTEXT and SOURCE when scoring:
  * Known legitimate brands (Nike, Amazon, banks) using official domains = LOW RISK
  * Unknown senders requesting money/personal info = HIGH RISK
  * Unrealistic promises from unknown sources = HIGH RISK
  
SCORING SCALE (be strict about these thresholds):
- 0-20: Safe - Normal communication, standard marketing, legitimate business
- 21-40: Low Risk - Some caution needed, verify sender but likely legitimate
- 41-60: Medium Risk - Multiple red flags, proceed with caution, verify carefully
- 61-80: High Risk - Strong scam indicators, likely fraudulent
- 81-100: Critical Risk - Definite scam, do not engage

PHRASE FLAGGING RULES:
- Only flag phrases that are ACTUALLY suspicious in context
- Don't flag normal business language like "limited time", "sale", "discount" from legitimate sources
- DO flag: unrealistic promises, requests for money from strangers, suspicious URLs, authority impersonation
- Consider the SEVERITY: not everything is a red flag, some things are just "be aware"

TEXT TO ANALYZE:
{text}

Provide a detailed analysis in the following JSON format:

{{
    "overall_confidence_score": <number 0-100, be realistic - most legitimate marketing should score 10-25>,
    "overall_assessment": "<brief summary of the text's trustworthiness>",
    "category_scores": {{
        "phishing": <0-100, only high if suspicious URLs or credential requests>,
        "financial_scam": <0-100, only high if unrealistic money promises or requests from strangers>,
        "misinformation": <0-100, only high if verifiable false claims>,
        "emotional_manipulation": <0-100, standard marketing emotion is LOW, extreme manipulation is HIGH>,
        "urgency_tactics": <0-100, normal business deadlines are LOW (20-30), extreme pressure is HIGH>
    }},
    "red_flags": [
        {{
            "flag": "<red flag description>",
            "severity": "<low/medium/high - be accurate, not everything is HIGH>",
            "explanation": "<why this is concerning, consider context>"
        }}
    ],
    "suspicious_phrases": [
        {{
            "phrase": "<exact phrase from text - ONLY include genuinely suspicious phrases>",
            "reason": "<why it's suspicious IN THIS CONTEXT>"
        }}
    ],
    "recommendation": "<what the user should do>",
    "is_safe": <true/false>
}}

EXAMPLES FOR CALIBRATION:

Example 1 (LEGITIMATE MARKETING - should score ~15):
Text: "LIMITED TIME SALE! 50% off all shoes - Today Only! Shop now: www.nike.com"
- Score: 15 (low risk, normal marketing)
- Urgency_tactics: 30 (normal business urgency)
- Emotional_manipulation: 25 (standard marketing)
- Suspicious phrases: NONE or maybe just note "verify URL matches nike.com"

Example 2 (ACTUAL SCAM - should score ~95):
Text: "URGENT! You won $50,000! Send $500 via Western Union to claim your prize!"
- Score: 95 (critical risk)
- Urgency_tactics: 95
- Financial_scam: 98
- Suspicious phrases: "You won $50,000", "Send $500", "Western Union"

Example 3 (ROMANCE SCAM - should score ~70-85):
Text: "I love you. I need $800 for plane ticket via Western Union. I'll pay you back."
- Score: 75-85 (high risk, not 98)
- Financial_scam: 90
- Emotional_manipulation: 70
- Flag "I need $800" and "Western Union" as HIGH severity
- Flag "I love you" as MEDIUM severity (context matters - fast relationship + money request)
- DON'T flag normal conversational phrases like "I have wonderful news"

Be thorough and accurate. If the text seems safe, reflect that in low scores. Don't over-flag legitimate communication.
"""
    
    try:
        # Call Gemini API
model = genai.GenerativeModel('gemini-1.5-flash') # Ya 'gemini-pro'
response = model.generate_content(prompt)
        # Extract and parse the JSON response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse JSON
        analysis = json.loads(response_text)
        
        return {
            "success": True,
            "data": analysis
        }
        
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": "Failed to parse AI response",
            "raw_response": response_text if 'response_text' in locals() else "No response"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_severity_color(severity):
    """Returns color for severity levels"""
    colors = {
        "low": "🟢",
        "medium": "🟡",
        "high": "🔴"
    }
    return colors.get(severity.lower(), "⚪")


def get_score_color(score):
    """Returns color emoji based on confidence score"""
    if score <= 20:
        return "🟢"  # Safe
    elif score <= 40:
        return "🟡"  # Low risk
    elif score <= 60:
        return "🟠"  # Medium risk
    elif score <= 80:
        return "🔴"  # High risk
    else:
        return "🔴"  # Critical risk


def get_category_icon(category):
    """Returns icon for each category"""
    icons = {
        "phishing": "🎣",
        "financial_scam": "💰",
        "misinformation": "🗞️",
        "emotional_manipulation": "🧠",
        "urgency_tactics": "⚠️"
    }
    return icons.get(category, "❓")


def create_annotated_text_html(original_text, suspicious_phrases):
    """
    Creates HTML-annotated version of text with highlighted suspicious parts.
    Returns HTML string with proper escaping.
    """
    if not suspicious_phrases:
        return f"""
        <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #444; font-size: 16px; line-height: 1.8;'>
            {original_text}
        </div>
        """
    
    import html
    
    # Escape the entire text first
    escaped_text = html.escape(original_text)
    
    # Track replacements to make
    replacements = []
    
    # Find all phrase positions in ORIGINAL text (not escaped)
    for phrase_data in suspicious_phrases:
        phrase = phrase_data["phrase"]
        reason = html.escape(phrase_data["reason"])
        
        # Find phrase in original text (case-insensitive)
        start_pos = original_text.lower().find(phrase.lower())
        if start_pos != -1:
            end_pos = start_pos + len(phrase)
            original_phrase_text = original_text[start_pos:end_pos]
            
            replacements.append({
                "original": original_phrase_text,
                "escaped": html.escape(original_phrase_text),
                "reason": reason
            })
    
    # Now replace in the escaped text
    highlighted_text = escaped_text
    for replacement in replacements:
        # Create the highlighted span
        highlighted_span = f"""<span style='background-color: #ff4444; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; cursor: help;' title='{replacement["reason"]}'>{replacement["escaped"]}</span>"""
        
        # Replace first occurrence
        highlighted_text = highlighted_text.replace(replacement["escaped"], highlighted_span, 1)
    
    # Wrap in container
    html_content = f"""
    <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #444; font-size: 16px; line-height: 1.8; color: #ffffff;'>
        {highlighted_text}
    </div>
    """
    
    return html_content 
