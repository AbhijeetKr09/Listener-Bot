# Listener Bot Project

## Overview

Welcome to the Listener Bot project! This project is designed to create an interactive chatbot using the Telegram API, capable of engaging in conversations, providing sentiment analysis, and detecting potential domestic violence concerns. The bot utilizes various modules to achieve these functionalities.

## Modules

### ChatApp

The `ChatApp` module serves as the main interaction point between the Telegram API and the underlying conversation analysis and response generation modules.

- **Real-time Interaction:** Handles incoming messages, records user data, and generates appropriate responses.

### ConversationAnalyzer

The `ConversationAnalyzer` module focuses on sentiment analysis and daily reporting.

- **Sentiment Analysis:** Utilizes the `SentimentIntensityAnalyzer` for sentiment analysis on user conversations.

- **Daily Reporting:** Provides daily sentiment reports based on historical data.

### Domestic_violence_Analyzer

The `Domestic_violence_Analyzer` module within conversation analyzer identifies potential domestic violence concerns in user conversations.

- **Domestic Violence Detection:** Analyzes user text for keywords and sentiment to identify potential domestic violence concerns. If detected, it provides a supportive response.

### ResponseGenerator

The `ResponseGenerator` module is responsible for generating responses based on user prompts.

- **Response Generation:** Uses OpenAI's GPT-3 engine to generate context-aware responses.

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `data.env` (e.g., BOT_TOKEN, NLU_API, OPENAI_API, etc.).
3. Run the main file: `python main_v2.py`

**Note:** Ensure you have the necessary dependencies installed and environment variables configured before running the project.

