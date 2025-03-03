from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load your BERT model and tokenizer
model_path = "./trained_model"  # Ensure this path is correct
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()

# Define labels
labels = {0: "Not Cyberbullying", 1: "Ethnicity/Race", 2: "Gender/Sexual", 3: "Religion", 4: "Age"}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        user_input = data.get('text', '')

        if not user_input.strip():
            return jsonify({"error": "Empty input"}), 400

        # Tokenize input text
        inputs = tokenizer(user_input, return_tensors="pt", padding=True, truncation=True)

        # Get prediction
        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        prediction_label = labels.get(predicted_class, "Unknown")

        return jsonify({"prediction": prediction_label})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
