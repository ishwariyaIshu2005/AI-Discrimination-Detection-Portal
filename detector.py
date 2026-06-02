from textblob import TextBlob

# -----------------------------------
# Tamil + English Warning Keywords
# -----------------------------------

warning_words = [

    # English
    "hate",
    "inferior",
    "worthless",
    "stupid",
    "caste",
    "community",
    "untouchable",
    "discrimination",
    "racist",

    # Tamil
    "வெறுப்பு",
    "வெறுக்கிறேன்",
    "சாதி",
    "தாழ்ந்த",
    "ஒதுக்க",
    "அவமதிப்பு",
    "பாகுபாடு",
    "இழிவான"
]

# -----------------------------------
# Main Detection Function
# -----------------------------------

def analyze_text(text):

    text_lower = text.lower()

    score = 0

    detected_words = []

    # Keyword Detection
    for word in warning_words:

        if word.lower() in text_lower:

            score += 25
            detected_words.append(word)

    # Sentiment Analysis
    try:

        sentiment = TextBlob(text).sentiment.polarity

    except:

        sentiment = 0

    # Negative sentiment adds risk
    if sentiment < 0:

        score += 25

    # Maximum 100
    score = min(score, 100)

    # Risk Classification
    if score >= 75:

        result = "🔴 High Risk"

    elif score >= 40:

        result = "🟠 Medium Risk"

    else:

        result = "🟢 Low Risk"

    # Alert Message
    if score >= 75:

        alert = """
⚠ WARNING

Potential discriminatory or harmful content detected.

Immediate review recommended.
"""

    elif score >= 40:

        alert = """
⚠ CAUTION

Some risky language detected.

Further review suggested.
"""

    else:

        alert = """
✅ SAFE CONTENT

No major warning signs detected.
"""

    return {

        "result": result,

        "severity": score,

        "words": detected_words,

        "sentiment": sentiment,

        "alert": alert
    }