from flask import Flask, render_template, request, redirect, url_for
import os
import time
from milvus_db import insert_question_answer  # Import the insert function from milvus_db

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
    """Simulate file processing (replace with actual processing logic)"""
    print(f"Processing file: {file_path}")
    time.sleep(3)  # Simulate time taken to process the file
    print(f"Finished processing: {file_path}")

@app.route('/submit_question', methods=['POST'])
def submit_question():
    # Get the question from the form
    question = request.form.get('question')
    if question:
        # Here you can process the question and generate an answer
        answer = f"{question}"  # Placeholder response
        # Add the question and answer to chat history
        chat_history.append((question, answer))
        insert_question_answer(question, answer)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
