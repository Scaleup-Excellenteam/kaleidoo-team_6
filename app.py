from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import time
# from milvus_db import insert_question_answer  # Import the insert function from milvus_db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
# Store chat history in a list
chat_history = []

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html', chat=chat_history)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' in request.files:
        files = request.files.getlist('files')
        for file in files:
            if file.filename:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                # Simulate processing the file (e.g., parsing or extracting content)
                process_file(file_path)
    return redirect(url_for('index'))

def process_file(file_path):
    """Choose the correct processing function based on file extension"""
    file_ext = os.path.splitext(file_path)[1].lower()

    # if file_ext in ['.mp4', '.avi', '.mov']:  # Example video file extensions
    #     process_video(file_path)
    # elif file_ext in ['.mp3', '.wav']:  # Example audio file extensions
    #     process_audio(file_path)
    # elif file_ext in ['.pdf', '.docx', '.txt']:  # Example document file extensions
    #     process_document(file_path)
    # else:
    #     print(f"Unsupported file type: {file_path}")


@app.route('/submit_question', methods=['POST'])
def submit_question():
    # Expect JSON data
    data = request.get_json()
    question = data.get('question')

    if question:
        # Process the question and generate an answer (this is where you'd implement your logic)
        answer = f"Answer for: {question}"  # Placeholder response for the question

        # Add the question and answer to the chat history
        chat_history.append((question, answer))

        # Optionally, store the question and answer in the database
        # insert_question_answer(question, answer)

        # Send the question and answer back as JSON response
        return jsonify({"question": question, "answer": answer})

    return jsonify({"error": "No question provided"}), 400


if __name__ == '__main__':
    app.run(debug=True)
