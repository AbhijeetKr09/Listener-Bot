
from nltk.sentiment import SentimentIntensityAnalyzer
import os
from datetime import datetime
import re


conversation_data = []
class ConversationAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def analyze_conversation(self, username, conversation_data):
        self.sentiment_scores = [self.sia.polarity_scores(message['text'])['compound'] for message in conversation_data]
        average_sentiment_score = sum(self.sentiment_scores) / len(self.sentiment_scores) if self.sentiment_scores else 0

        sentiment_label = self.get_sentiment_label(average_sentiment_score)
        report = self.generate_report(average_sentiment_score, sentiment_label)
        self.save_report(username, report, average_sentiment_score)

        return report

    def get_sentiment_label(self, sentiment_score):
        if sentiment_score > 0.05:
            return "positive"
        elif sentiment_score < -0.05:
            return "negative"
        else:
            return "neutral"
    @staticmethod
    def generate_report(average_sentiment_score, sentiment_label):
        if sentiment_label == "positive":
            report = f"Your recent conversations show a positive sentiment."
        elif sentiment_label == "negative":
            report = f"Your recent conversations show a negative sentiment."
        else:
            report = f"Your recent conversations show a neutral sentiment."

        report += f"\nAverage Sentiment Score: {average_sentiment_score:.2f}"
        return report

    @staticmethod
    def save_report(username, report, sentiment_score):
        if not os.path.exists('reports'):
            os.makedirs('reports')

        report_filename = f'reports/{username}.txt'

        with open(report_filename, 'a') as file:
            now = datetime.now()
            date_string = now.strftime("%Y-%m-%d %H:%M:%S")
            report_with_score = f"\n\nReport generated on {date_string}:\n{report}\nAverage Sentiment Score: {sentiment_score:.2f}"
            file.write(report_with_score)

    def get_scores_for_date(self, username, target_date):
        scores = []
        reports_path = 'reports'
        for filename in os.listdir(reports_path):
            if filename.startswith(username) and filename.endswith('.txt'):
                with open(os.path.join(reports_path, filename), 'r') as file:
                    content = file.read()
                    report_date_str = re.search(r'Report generated on (\d{4}-\d{2}-\d{2})', content)
                    if report_date_str:
                        report_date = datetime.strptime(report_date_str.group(1), "%Y-%m-%d")
                        if report_date.date() == target_date.date():
                            sentiment_score = float(re.search(r'Average Sentiment Score: (\d+\.\d+)', content).group(1))
                            scores.append(sentiment_score)
        return scores
    
    def get_daily_report(self, username, target_date):
        scores = self.get_scores_for_date(username, target_date)
        if not scores:
            return "No conversations recorded for the day."

        average_score = sum(scores) / len(scores)
        sentiment_label = self.get_sentiment_label(average_score)
        report = self.generate_report(average_score, sentiment_label)

        overall_sentiment = "positive" if average_score > 0 else "negative" if average_score < 0 else "neutral"

        if overall_sentiment == sentiment_label:
            # More positivity or neutrality
            percent_difference = abs(average_score) * 100
            message = f"Your conversations today show a {percent_difference:.2f}% higher level."
        else:
            # More negativity
            percent_difference = abs(average_score) * 100
            message = f"Your conversations today show a {percent_difference:.2f}% tilt towards negativity."

        overall_report = f"{message}\n\n{report}\nAverage Sentiment Score: {average_score:.2f}"
        return overall_report
    
class Domestic_violence_Analyzer:

    def detect_domestic_violence(self, conversation_data):
        domestic_violence_keywords = ["abuse", "violence", "hurt", "fear", "control", "isolate", "threaten"]
        
        user_text = [message['text'] for message in conversation_data]
        
        user_text = " ".join(user_text)
        
        sentiment_score = self.sia.polarity_scores(user_text)['compound']
        
        keywords_present = any(keyword in user_text.lower() for keyword in domestic_violence_keywords)
        
        involves_domestic_violence = sentiment_score < -0.05 or keywords_present
        
        if involves_domestic_violence:
            response = "It seems like there may be concerns related to domestic violence in your recent conversation. Would you like to connect with someone who can provide assistance? Remember, talking to someone can be helpful. If you answer 'yes,' I can provide contact information for experts who can guide you."
        else:
            response = None
        
        return involves_domestic_violence, response