from flask import Flask, request, jsonify, render_template

from transformers import DistilBertTokenizerFast, DistilBertForQuestionAnswering
import torch

app = Flask(__name__)

# Load the trained model and tokenizer
model = DistilBertForQuestionAnswering.from_pretrained('./trained_chatbot_model')
tokenizer = DistilBertTokenizerFast.from_pretrained('./trained_chatbot_model')


def get_relevant_context(user_message):
    if "admission" in user_message.lower():
        return "Our admissions process is designed to be straightforward. We offer undergraduate and postgraduate programs..."
    elif "fee" in user_message.lower():
        return "The fee structure varies depending on the program and whether you are a domestic or international student..."
    elif "course" in user_message.lower():
        return "Each program has a specific set of courses and a detailed curriculum. If you have a particular course or major in mind..."
    # Add more conditions here based on the common questions
    else:
        return "I can assist with information about admissions, fees, courses, deadlines, and more."
# Home page route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    

    # Validate the input to ensure it's not empty or nonsensical
    if not user_message:
        return jsonify({"message": "Please enter a valid question."})

    # Example context and model logic (as shown previously)
    context = get_relevant_context(user_message)

    # If the message passes validation, proceed with model inference
    inputs = tokenizer(user_message, context, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        start_index = torch.argmax(outputs.start_logits)
        end_index = torch.argmax(outputs.end_logits)

    # Decode the model's response
    if start_index < end_index:
        answer = tokenizer.decode(inputs["input_ids"][0][start_index:end_index + 1])
    else:
        answer = "I'm sorry, I couldn't find a relevant answer. Could you rephrase your question?"

    return jsonify({"message": answer})

if __name__ == '__main__':
    app.run(debug=True)
