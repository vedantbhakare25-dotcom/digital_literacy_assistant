# Quiz examples for interactive learning
# Each example has suspicious phrases that users need to identify

QUIZ_EXAMPLES = [
    {
        "id": 1,
        "text": "CONGRATULATIONS! You've been selected to receive $5,000 cash prize! Click here NOW to claim within 24 hours or forfeit your winnings forever!",
        "suspicious_phrases": [
            {
                "phrase": "CONGRATULATIONS!",
                "reason": "Excessive enthusiasm with ALL CAPS to grab attention - common in scam messages"
            },
            {
                "phrase": "$5,000 cash prize",
                "reason": "Unsolicited prize claim - you didn't enter any contest"
            },
            {
                "phrase": "Click here NOW",
                "reason": "Urgent call to action pressuring immediate response"
            },
            {
                "phrase": "within 24 hours",
                "reason": "Artificial deadline to prevent verification and create FOMO"
            },
            {
                "phrase": "forfeit your winnings forever",
                "reason": "Fear-based pressure tactic threatening loss"
            }
        ],
        "category": "Lottery Scam",
        "risk_score": 95
    },
    {
        "id": 2,
        "text": "Your Amazon account has been compromised. Verify your identity immediately at amazon-security-check.com or your account will be permanently suspended.",
        "suspicious_phrases": [
            {
                "phrase": "has been compromised",
                "reason": "Creates fear and urgency without providing specific details"
            },
            {
                "phrase": "immediately",
                "reason": "Pressures instant action to prevent careful thinking"
            },
            {
                "phrase": "amazon-security-check.com",
                "reason": "Suspicious domain - real Amazon uses amazon.com, not third-party domains"
            },
            {
                "phrase": "permanently suspended",
                "reason": "Threat of severe consequences to induce panic"
            }
        ],
        "category": "Phishing Attack",
        "risk_score": 90
    },
    {
        "id": 3,
        "text": "Investment opportunity! Make $10,000 per week working from home. No experience needed. Limited spots available - join now!",
        "suspicious_phrases": [
            {
                "phrase": "$10,000 per week",
                "reason": "Unrealistic income promise - too good to be true"
            },
            {
                "phrase": "No experience needed",
                "reason": "High pay with no requirements is a major red flag"
            },
            {
                "phrase": "Limited spots available",
                "reason": "Artificial scarcity to pressure quick decisions"
            },
            {
                "phrase": "join now",
                "reason": "Urgent call to action without providing real details"
            }
        ],
        "category": "Financial Scam",
        "risk_score": 85
    },
    {
        "id": 4,
        "text": "IRS NOTICE: You owe $3,247 in back taxes. Pay immediately via gift cards to avoid arrest. Call 1-800-FAKE-IRS.",
        "suspicious_phrases": [
            {
                "phrase": "IRS NOTICE:",
                "reason": "Government impersonation - IRS doesn't contact via random messages"
            },
            {
                "phrase": "Pay immediately",
                "reason": "Urgent payment demand without proper documentation"
            },
            {
                "phrase": "via gift cards",
                "reason": "MAJOR RED FLAG - legitimate organizations NEVER request gift card payments"
            },
            {
                "phrase": "avoid arrest",
                "reason": "Threatening consequences to create fear and panic"
            }
        ],
        "category": "Government Impersonation",
        "risk_score": 98
    },
    {
        "id": 5,
        "text": "Hi! I'm a Nigerian prince with $10 million. I need your help transferring funds. You'll receive 20% commission. Send your bank details for verification.",
        "suspicious_phrases": [
            {
                "phrase": "Nigerian prince",
                "reason": "Classic internet scam trope - notorious advance-fee fraud"
            },
            {
                "phrase": "$10 million",
                "reason": "Absurdly large amount offered to strangers"
            },
            {
                "phrase": "20% commission",
                "reason": "Unrealistic reward for doing nothing"
            },
            {
                "phrase": "Send your bank details",
                "reason": "Request for sensitive financial information - NEVER share this"
            }
        ],
        "category": "Advance-Fee Fraud",
        "risk_score": 92
    }
]

# Spot the Difference examples - Suspicious vs Legitimate versions
COMPARISON_EXAMPLES = [
    {
        "id": 1,
        "category": "Banking Security Alert",
        "suspicious": "URGENT!!! Your bank account will be LOCKED in 2 hours! Click this link immediately to verify: bit.ly/bank123",
        "legitimate": "We noticed unusual activity on your account ending in 4567. For your security, please log into your account at www.yourbank.com or call us at 1-800-123-4567. - YourBank Security Team",
        "differences": [
            {
                "point": "Tone",
                "suspicious_detail": "ALL CAPS, excessive punctuation (!!!)",
                "legitimate_detail": "Professional, calm tone"
            },
            {
                "point": "Urgency",
                "suspicious_detail": "Extreme urgency (2 hours), threatens account lockout",
                "legitimate_detail": "Informational, provides options without pressure"
            },
            {
                "point": "Links",
                "suspicious_detail": "Shortened link (bit.ly) - hides real destination",
                "legitimate_detail": "Full official website URL (www.yourbank.com)"
            },
            {
                "point": "Contact Method",
                "suspicious_detail": "Forces you to click suspicious link",
                "legitimate_detail": "Provides official phone number and website"
            },
            {
                "point": "Identification",
                "suspicious_detail": "Generic 'your bank account'",
                "legitimate_detail": "Specific account number (last 4 digits)"
            }
        ]
    },
    {
        "id": 2,
        "category": "Prize/Lottery Notification",
        "suspicious": "WINNER ALERT! You've won $50,000! Claim now before midnight or lose forever! No purchase necessary! Click here!",
        "legitimate": "Thank you for participating in our Annual Customer Appreciation Sweepstakes. You have been selected as a finalist. To verify your entry and eligibility, please contact our customer service at 1-800-555-0199 within 30 days. Please reference your confirmation number: #ABC123456. - CompanyName Promotions Department",
        "differences": [
            {
                "point": "Notification Style",
                "suspicious_detail": "Declares you a winner without any context",
                "legitimate_detail": "References specific contest you entered"
            },
            {
                "point": "Deadline Pressure",
                "suspicious_detail": "Extreme urgency (midnight), threatens loss",
                "legitimate_detail": "Reasonable timeframe (30 days) for response"
            },
            {
                "point": "Call to Action",
                "suspicious_detail": "Suspicious 'click here' link",
                "legitimate_detail": "Official phone number to call"
            },
            {
                "point": "Verification",
                "suspicious_detail": "No way to verify legitimacy",
                "legitimate_detail": "Provides confirmation number and company name"
            },
            {
                "point": "Language",
                "suspicious_detail": "Excessive excitement, multiple exclamation points",
                "legitimate_detail": "Professional, formal communication"
            }
        ]
    },
    {
        "id": 3,
        "category": "Job Opportunity",
        "suspicious": "Make $5000/week from home! No experience! No interview! Just send $99 for training materials and start today!",
        "legitimate": "We're hiring for a Remote Customer Service position. Starting salary: $45,000-$55,000/year. Requirements: 2+ years customer service experience, reliable internet. Apply at www.company.com/careers or email careers@company.com with your resume. - HR Department, Company Name",
        "differences": [
            {
                "point": "Compensation",
                "suspicious_detail": "Unrealistic pay ($5000/week = $260k/year)",
                "legitimate_detail": "Realistic salary range for the role"
            },
            {
                "point": "Requirements",
                "suspicious_detail": "'No experience needed' for high-paying job",
                "legitimate_detail": "Clear qualifications and experience required"
            },
            {
                "point": "Upfront Payment",
                "suspicious_detail": "Asks for $99 for 'training materials' - RED FLAG",
                "legitimate_detail": "No payment required - legitimate employers never charge fees"
            },
            {
                "point": "Hiring Process",
                "suspicious_detail": "No interview, start immediately",
                "legitimate_detail": "Standard application process mentioned"
            },
            {
                "point": "Company Info",
                "suspicious_detail": "No company name or verifiable contact",
                "legitimate_detail": "Company name, official email, and website provided"
            }
        ]
    }
]
