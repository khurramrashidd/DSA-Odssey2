from flask import Flask, render_template, jsonify, url_for, request
import json
import os
import google.generativeai as genai

app = Flask(__name__)  

# --- Gemini AI Setup ---
# It's highly recommended to set your API key as an environment variable
# and not to hardcode it directly in your code.
# For example: os.environ.get("GEMINI_API_KEY")
# For this example, I'm using the key you provided, but be careful with it.
API_KEY = "AIzaSyBZ_Mea6_FaJVcWTYhc4r1OAlGzjdQIkxw"

# Configure the Gemini API client
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Main route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API route to serve the journey data
@app.route('/api/journey-data')
def get_journey_data():
    # Construct the full path to the JSON file
    json_path = os.path.join(app.static_folder, 'journeyData.json')
    # Open and load the JSON file
    #with open(json_path) as f:
    # Inside the get_journey_data function
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Return the data as a JSON response
    return jsonify(data)

# --- New API route for Gemini AI ---
@app.route('/api/get-code', methods=['POST'])
def get_code_solution():
    """
    This new route will get the problem name and language from the frontend,
    then use the Gemini AI to generate a code solution.
    """
    data = request.get_json()
    problem_name = data.get('problem_name')
    language = data.get('language')

    if not problem_name or not language:
        return jsonify({"error": "Problem name and language are required."}), 400

    try:
        # Construct a detailed prompt for the AI
        prompt = (f"Provide a code solution for the problem '{problem_name}' in {language}. "
                  "The code solution should have the best possible time and space complexity. "
                  "After coding, give a brief explanation of the code and the time and space complexity of your solution.")

        # Call the Gemini API
        response = model.generate_content(prompt)

        # Return the generated code in the response
        return jsonify({"code_solution": response.text})

    except Exception as e:
        # Handle potential errors from the API call
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5000)