import random
import nltk  # For natural language processing (you'll need to install it: pip install nltk)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)  # Download necessary NLTK data (do this once)
nltk.download('stopwords', quiet=True)


def preprocess_text(text):
    """Preprocesses text for better analysis."""
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [w for w in tokens if not w in stop_words and w.isalnum()]  # Remove stopwords and non-alphanumeric
    return filtered_tokens


def get_response(user_input):
    """Generates a more advanced chatbot response."""

    user_input = user_input.lower()
    preprocessed_input = preprocess_text(user_input)

    responses = {
        "greetings": ["Hello!", "Hi there!", "Hey!", "Greetings!"],
        "goodbye": ["Goodbye!", "See you later!", "Farewell!", "Bye!"],
        "how_are_you": ["I'm doing well, thank you!", "I'm great!", "I'm fine, how about you?"],
        "name": ["I'm a chatbot!", "You can call me Chatbot.", "I don't have a name."],
        "help": ["I can answer your questions.", "How can I help you?"],
        "weather": ["I can look up the weather for you. Where are you located?", "Tell me your city and I'll check the weather."],  # Example of a more complex intent
        "default": ["I didn't understand that.", "Could you please rephrase?", "I'm still learning."]
    }

    # Enhanced Keyword Matching (using preprocessed input):
    for keyword, response_list in responses.items():
        keyword_tokens = preprocess_text(keyword)  # Preprocess keywords too
        if any(token in preprocessed_input for token in keyword_tokens):  # Check if ANY keyword token is present
            return random.choice(response_list)

    # Simple Context Awareness (Example - Weather):
    if "weather" in preprocessed_input:
        # Here you would integrate with a weather API (e.g., OpenWeatherMap)
        # to get the actual weather information.  This is a placeholder:
        city = ""
        for token in preprocessed_input:  # Look for a city name (very basic)
            if token.istitle():  # A simple heuristic (not perfect)
                city = token
                break

        if city:
            return f"The weather in {city} is currently sunny. (This is a simulated response)."  # Replace with actual API call
        else:
            return "Please tell me the city you'd like the weather for."


    return random.choice(responses["default"])


def chatbot():
    print("Welcome to the Advanced Chatbot!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye!")
            break

        bot_response = get_response(user_input)
        print("Chatbot:", bot_response)


if __name__ == "__main__":
    chatbot()weather
