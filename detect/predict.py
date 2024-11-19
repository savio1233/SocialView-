
import pandas as pd
import spacy
import joblib


def main(content):
    def preprocess(text):
        if pd.isnull(text):
            return ""
        # Tokenize the text and remove stop words and punctuation
        doc = nlp(text)
        filtered_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return " ".join(filtered_tokens)

    nlp = spacy.load("en_core_web_sm")

    loaded_model = joblib.load('detect/sentiment_model.joblib')

    # Function to predict sentiment
    def predict_sentiment(text):
        text = preprocess(text)
        print(text)
        prediction = loaded_model.predict([text])
        print("Prediction: ", prediction)
        if prediction > 1:
            return "Positive"
        elif prediction < 0:
            return "Negative"
        else: 
            return "Neutral"

    # Test the function
    prediction = predict_sentiment(content)
    print("Predicted sentiment:", prediction)
    return prediction