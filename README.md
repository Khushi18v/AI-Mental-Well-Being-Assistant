# AI Mental Well-Being Assistant
An AI-driven application designed to support mental health by providing journaling, sentiment analysis, relaxation exercises, and personalized feedback to help users manage emotional well-being.

# Features
Journaling: Safely write and store emotional entries with sentiment analysis and AI reflections.

Relaxation Tools: Guided breathing and mindfulness exercises.

Personalized Recommendations: Daily well-being tips and suggestions.

Safety Panel: Emergency resources and grounding techniques.

# Installation
Install Python
Python 3.10 or higher

Set Up Virtual Environment python -m venv venv
Activate:

Windows

venv\Scripts\activate

macOS / Linux

source venv/bin/activate

Install Dependencies pip install -r requirements.txt

Set OpenAI API Key

Create a .env file and add:

OPENAI_API_KEY=your_api_key_here

Run the Application streamlit run app.py
Open in browser


Project Structure /app.py - Main application /agents.py - AI agents for emotional support /sentiment.py - Sentiment analysis module /storage.py - Local JSON storage /tools_ui.py - UI modules /data/journal.json - Journal entries

# Technologies Used
Python 3.10+

Streamlit – User Interface

OpenAI API – AI-driven responses

TextBlob – Sentiment analysis
