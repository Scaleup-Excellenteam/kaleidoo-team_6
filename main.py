import os
import shutil
import time
import sys
from flask import Flask, request, jsonify

# Import your existing modules
sys.path.append(r'C:\Users\Dor Shukrun\AllCoding\Exelanteam\Klaido\kaleidoo-team_6')
from extraction_doc.extractor import save_text_to_file
from milvus.script.indexing import get_context
from answer_generator.generate_ans import contaxt_to_generate_directory_lisener

app = Flask(__name__)

# Define source and destination paths
SRC_FOLDER = r'data\uploads_for_all_data_type'
DEST_FOLDER = r'data\finshed\source_files_all_data_typs'
FIXED_DEST_FOLDER = r'data\extracted_text_from_media'


@app.route('/submit_question', methods=['POST'])
def submit_question():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    try:
        # Process the files first
        check_and_process_files(SRC_FOLDER, DEST_FOLDER, save_text_to_file, FIXED_DEST_FOLDER)

        # Get context from the vector database
        get_context(question)

        # Generate the answer
        contaxt_to_generate_directory_lisener(question)

        # Load the generated answer from a file or variable (assuming answer is saved in a file)
        with open(r'data\generated_answers\answer.txt', 'r') as f:
            answer = f.read()

        return jsonify({'question': question, 'answer': answer})

    except Exception as e:
        print(f"Error processing the question: {e}")
        return jsonify({'error': 'Failed to process the question'}), 500


def check_and_process_files(src_folder, dest_folder, process_file, fixed_dest_folder):
    """
    Process files in the source folder and move them to the destination folder.
    """
    files = os.listdir(src_folder)

    if files:
        file_path = os.path.join(src_folder, files[0])

        try:
            # Ensure the destination folders exist
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            if not os.path.exists(fixed_dest_folder):
                os.makedirs(fixed_dest_folder)

            # Process the file using the provided function
            process_file(file_path, fixed_dest_folder)

            # Move the file to the destination folder
            shutil.move(file_path, dest_folder)
            print(f"{file_path} has been moved to the destination folder")

        except Exception as e:
            print(f"Error processing the file {file_path}: {e}")

    # Simulate a wait for 3 seconds (you can remove this for real-time processing)
    time.sleep(3)


if __name__ == '__main__':
    app.run(debug=True)
