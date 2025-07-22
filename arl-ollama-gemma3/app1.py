from flask import Flask, request, jsonify, render_template
from intent_parser import llama_intent_parser
from db_utils import get_trending_products
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat/intent', methods=['POST'])
def parse_intent():
    user_input = request.json.get("message", "")
    parsed_intent = llama_intent_parser(user_input)

    if parsed_intent:
        return jsonify({"intent_data": parsed_intent})  # ✅ match frontend key
    else:
        return jsonify({"error": "Could not parse intent."}), 400

@app.route('/chat/result', methods=['POST'])
def get_results():
    intent_data = request.json.get("intent_data", {})  # ✅ match frontend key

    if intent_data.get("intent") == "trend":
        result = get_trending_products(intent_data)
        return jsonify({"trend_result": result})  # ✅ match frontend key
    else:
        return jsonify({"trend_result": []})

@app.route('/env_vars', methods=['GET'])
def get_environment_variables():
    """
    Returns all environment variables as a JSON response.
    """
    env_vars = dict(os.environ)  # Convert os.environ to a dictionary
    return jsonify(env_vars)

if __name__ == '__main__':
    app.run(debug=True)