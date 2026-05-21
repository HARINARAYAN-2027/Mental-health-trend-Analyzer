import re

class MentalHealthEngine:
    """Local Machine Learning Text Analysis Engine for sentiment and risk assessment"""

    def analyze_sentiment(self, text):
        """Analyze text for sentiment, emotion, and risk level with frontend metadata color patches"""
        text_lower = text.lower()

        # 1. Base Token Keyword Lexicon Selection
        positive_words = {'happy', 'good', 'great', 'excellent', 'love', 'wonderful', 'amazing', 'perfect', 'energized', 'grateful', 'loved'}
        negative_words = {'sad', 'bad', 'terrible', 'hate', 'awful', 'depressed', 'anxious', 'angry', 'stressed', 'overwhelmed', 'lost', 'hopeless', 'lonely', 'stuck', 'stress'}

        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)

        # 2. Mathematical Sentiment Scoring and Percentage Normalization
        if pos_count > neg_count:
            sentiment = "Positive"
            raw_confidence = min(0.95, 0.60 + (pos_count * 0.10))
        elif neg_count > pos_count:
            sentiment = "Negative"
            raw_confidence = min(0.95, 0.65 + (neg_count * 0.08))
        else:
            sentiment = "Neutral"
            raw_confidence = 0.70

        # JavaScript Binding Fix: Convert decimal score (e.g. 0.90) into actual UI Percentage (e.g. 90.0)
        confidence_percentage = round(raw_confidence * 100, 1)

        # 3. Priority Emotion Extraction Routing
        emotion_keywords = {
            'suicide': 'Severe Distress',
            'hopeless': 'Depression Trigger',
            'anxious': 'Anxiety',
            'stressed': 'Stress',
            'stress': 'Stress',
            'overwhelmed': 'Stress',
            'sad': 'Sadness',
            'angry': 'Anger',
            'happy': 'Joy',
            'loved': 'Joy',
            'good': 'Joy',
            'calm': 'Calmness'
        }
        
        emotion = "Neutral"
        for keyword, emo in emotion_keywords.items():
            if keyword in text_lower:
                emotion = emo
                break

        # 4. Critical Risk Status Mapping Engine
        risk_keywords = {'suicide', 'self-harm', 'dangerous', 'severe', 'hopeless'}
        
        if any(word in text_lower for word in risk_keywords):
            risk_level = "High Risk"
        elif neg_count >= 2 or 'stressed' in text_lower or 'overwhelmed' in text_lower:
            risk_level = "Moderate Risk"
        else:
            risk_level = "Low Risk"

        # 5. UI Metadata Color Management (Crucial for frontend api.js cards)
        # Sentiment Colors
        if sentiment == "Positive":
            sentiment_color = "#10b981"  # Emerald Green
        elif sentiment == "Negative":
            sentiment_color = "#ef4444"  # Coral Red
        else:
            sentiment_color = "#3b82f6"  # Cobalt Blue

        # Risk Status Colors
        if risk_level == "High Risk":
            risk_color = "#ef4444"      # Red Alert
        elif risk_level == "Moderate Risk":
            risk_color = "#f59e0b"    # Amber/Orange Warning
        else:
            risk_color = "#10b981"     # Stable Green Shield

        return {
            'original_text': text,
            'sentiment': sentiment,
            'emotion': emotion,
            'risk_level': risk_level,
            'confidence': confidence_percentage,  # Now returns 90.0% instead of 0.9%
            'sentiment_color': sentiment_color,
            'risk_color': risk_color,
            'text': text
        }