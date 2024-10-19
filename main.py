import os
import shutil
import time
import sys
import openai
from dotenv import load_dotenv

sys.path.append(r'C:\Users\Dor Shukrun\AllCoding\Exelanteam\Klaido\kaleidoo-team_6')



from extraction_doc.extractor import *
from milvus.script.indexing import get_context
from answer_generator.generate_ans import contaxt_to_generate_directory_lisener

def load_api_key() -> str:
    return os.getenv("OPENAI_API_KEY")


def generate_summary(api_key: str, question: str, context: str) -> str:
    openai.api_key = api_key
    try:

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": ("You are a study assistant. The user can load a large amount of information into another model that performs RAG. "
                                "You will receive the most relevant vectors, and I want you to answer the questions provided "
                                "strictly based on the data you received and not from any other dataset."
                    ),
                },
                {"role": "system", "content": f"Here is the context: {context}"},
                {"role": "user", "content": f"{question}"}
            ],
        )
        

        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"An error occurred: {str(e)}"



def check_and_process_files(src_folder, dest_folder, process_file, fixed_dest_folder):
    while True:
        # List files in the source folder
        files = os.listdir(src_folder)
        
        if files:
            # Get the first file in the folder
            file_path = os.path.join(src_folder, files[0])
            
            try:
                # Ensure the destination folders exist
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                if not os.path.exists(fixed_dest_folder):
                    os.makedirs(fixed_dest_folder)
                
                # Process the file using the provided function
                process_file(file_path, fixed_dest_folder) #TODO here we can navigate the file into the right place
                
                # Move the file to the destination folder if processing is successful
                shutil.move(file_path, dest_folder)
                print(f"{file_path} has been moved to the destination folder")
                
            except Exception as e:
                print(f"Error processing the file {file_path}: {e}")
                
        # Wait for 3 seconds before the next check
        time.sleep(3)
        input("Press Enter to continue...")
        break
        
def get_user_question():
    """
    Prompts the user to enter a question.
    
    Returns:
        str: The question entered by the user.
    """
    question = input("Enter your question: ")
    return question

def read_file(file_path):
    """
    Reads the content of a file and returns it as a string.
    
    Args:
        file_path (str): The path to the file.
    
    Returns:
        str: The content of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def better_results():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    context = read_file(r'data\context_to_generate_ans\context.txt')
    ans = generate_summary(api_key, question, context) 
    print(f"Answer: {ans}")

if __name__ == "__main__":
    # Define source and destination paths
    src = r'data\uploads_for_all_data_type'
    dest = r'data\finshed\source_files_all_data_typs'
    fixed_dest_folder = r'data\extracted_text_from_media'
    
    # Start the file processing function
    print("Extracting text from files...")
    check_and_process_files(src, dest, save_text_to_file, fixed_dest_folder) # saving in directory (data\extracted_text_from_media)
    print("All files have been processed")
    question = get_user_question()
    get_context(question) # getting the context from the vector database and saving it in a file (data\context_to_generate_ans\context.txt)
    contaxt_to_generate_directory_lisener(question) # getting the context from the file and generating the answers
    
    # better results
    choice = input("Do you want to get better results? (y/n): ")
    if choice.lower() == 'y':
        better_results()

        
    
    
    
    
    
    
