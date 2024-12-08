import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS


# Load environment variables from a .env file
load_dotenv()

# Configure the generative AI model with the API key
genai.configure(api_key=os.environ["API_KEY"])

# Create a Flask app instance
app = Flask(__name__)

# Initialize chat history
chat_history = []

# Configuration for AI model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Home route that handles both GET and POST requests
@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history

    # Handle user input via POST request
    if request.method == "POST":
        user_input = request.form.get("user_input")

        if user_input:
            # Add user message to chat history
            chat_history.append({"role": "user", "parts": user_input})

            # Generate AI response
            try:
                if len(chat_history) == 1:  # If it's the first user message
                    response = "Hello! I'm an AI designed to help with questions related to education. What would you like to learn today?"
                else:
                    prompt_with_context = f"You are a knowledgeable assistant focused on education. Please answer the following question: {user_input}"
                    response = model.generate_content([prompt_with_context]).text
            except Exception as e:
                response = f"An error occurred: {e}"

            # Add AI response to chat history
            chat_history.append({"role": "assistant", "parts": response})

        return redirect(url_for('index'))

    return render_template("index.html", chat_history=chat_history)

# API route to handle POST requests from Postman or any HTTP client
@app.route("/api/chat", methods=["POST"])
def api_chat():
    global chat_history

    # Parse the user input from JSON body
    data = request.json
    user_input = data.get("user_input")

    if user_input:
        # Add user message to chat history
        chat_history.append({"role": "user", "parts": user_input})

        # Generate AI response
        try:
            if len(chat_history) == 1:  # If it's the first user message
                response = "Hello! I'm an AI designed to help with questions related to education. What would you like to learn today?"
            else:
                prompt_with_context = f"You are a knowledgeable assistant focused on education. Please answer the following question: {user_input}"
                response = model.generate_content([prompt_with_context]).text
        except Exception as e:
            response = f"An error occurred: {e}"

        # Add AI response to chat history
        chat_history.append({"role": "assistant", "parts": response})

        # Return response as JSON
        return jsonify({"response": response})

    return jsonify({"error": "No user input received"}), 400

# Start the Flask web server
if __name__ == "__main__":
    # app.run(debug=True)
    app.run()

CORS(app)    
