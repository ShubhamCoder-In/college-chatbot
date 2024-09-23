from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import pickle
import ast

file_path = 'chatbot.csv'  # Adjust this to your file path
chatbot_data = pd.read_csv(file_path)

app = Flask(__name__)

model = load_model('chatbot_model.h5')
with open('label_encoder.pkl', 'rb') as file:
    label_encoder = pickle.load(file)

with open('tfidf_vectorizer.pkl', 'rb') as file:
    tfidf_vectorizer = pickle.load(file)

def get_response(user_input):
    user_input_tfidf = tfidf_vectorizer.transform([user_input]).toarray()
    predicted_tag_index = np.argmax(model.predict(user_input_tfidf))
    predicted_tag = label_encoder.inverse_transform([predicted_tag_index])[0]
    
    # Return a random response for the predicted tag
    responses = chatbot_data[chatbot_data['tag'] == predicted_tag]['response'].values[0]
    response_list = ast.literal_eval(responses)
    return np.random.choice(response_list)


# Home page route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    

    # Validate the input to ensure it's not empty or nonsensical
    if not user_message:
        return jsonify({"message": "Please enter a valid question."})
    answer = get_response(user_message)
    return jsonify({"message": answer})

if __name__ == '__main__':
    app.run(debug=True)
