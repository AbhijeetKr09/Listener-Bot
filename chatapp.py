from response_generator import ResponseGenerator
from conversation_analyzer import ConversationAnalyzer, Domestic_violence_Analyzer
from datetime import datetime
import json
from datetime import datetime, timedelta, time

current_time = datetime.now()
end_of_day = datetime(current_time.year, current_time.month, current_time.day, 23, 59, 59)

class ChatApp:
    def __init__(self):
        self.response_generator = ResponseGenerator()
        self.conversation_analyzer = ConversationAnalyzer()
        self.dv_analyzer = Domestic_violence_Analyzer()
        self.sent_dv_response = False
    
    def is_eod(self, my_datetime):
        eod_time = datetime.combine(my_datetime.date(), time(23, 59, 59))
        
        return my_datetime == eod_time
    
    def chat(self, username, query_text):

        conversation_history = self.response_generator.load_conversation_history(username)
        if self.is_eod(current_time) and not self.sent_dv_response:
            involves_domestic_violence, response = self.dv_analyzer.detect_domestic_violence(self.conversation_data)
            if involves_domestic_violence:
                self.sent_dv_response = True
                return response

        prompt = query_text if len(query_text) < 20 else self.response_generator.create_prompt(query_text)
        response_text = self.response_generator.generate_response(prompt, conversation_history)

        if not self.is_eod(current_time) or len(query_text) >= 20:
            self.response_generator.store_complete_data(username, query_text, response_text)


        self.response_generator.store_data(username, query_text, response_text)
        
        return response_text

    def analyze_conversation(self, username):
        self.conversation_data = self.response_generator.load_complete_conversation_history(username)
        return self.conversation_analyzer.analyze_conversation(username, self.conversation_data)

    def get_daily_report(self, username, target_date):
        return self.conversation_analyzer.get_daily_report(username, target_date)
    
    def get_user(self, username, filename='complete_history.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        return data

if __name__ == "__main__":
    app = ChatApp()
