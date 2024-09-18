from doc_extraction import extract_text_from_file, clean_text 
import time
from transformers import pipeline
import matplotlib.pyplot as plt


def run_model_and_measure_time(model_name, context, question):
    """
    Runs a question-answering model on a given context and question, and measures the time taken to get the answer.

    Args:
        model_name (str): The name or path of the pre-trained model to be used for question-answering.
        context (str): The text from which the model should extract the answer.
        question (str): The question to be answered based on the context.

    Returns:
        tuple: 
            - str: The extracted answer from the model.
            - float: The time taken to process the question and return the answer (in seconds).
    
    Example:
        answer, elapsed_time = run_model_and_measure_time('deepset/xlm-roberta-large-squad2', context, question)
        print(f"Answer: {answer}, Time: {elapsed_time:.2f} seconds")
    """

    qa_pipeline = pipeline('question-answering', model=model_name)
    
    start_time = time.time()
    result = qa_pipeline(question=question, context=context)
    end_time = time.time()

    elapsed_time = end_time - start_time
 
    return result['answer'], elapsed_time


def upload_file():
    """
    Handles file upload and returns the file path of the uploaded file.
    
    Returns:
        str: The path to the uploaded file.
    """
    
    file_path = input("Enter the path to the file: ")
    return file_path

def process_file(file_path):
    """
    Extracts text from the file, cleans the text, and returns the processed content.
    
    Args:
        file_path (str): The path to the file.
    
    Returns:
        str: The cleaned and processed text content.
    """
    context = extract_text_from_file(file_path)
    context = clean_text(context)
    return context

def get_user_question():
    """
    Prompts the user to enter a question.
    
    Returns:
        str: The question entered by the user.
    """
    question = input("Enter your question: ")
    return question

def run_models_on_question(models, context, question):
    """
    Runs each model on the given context and question, records the answer and execution time.
    
    Args:
        models (list): List of model names to run.
        context (str): The text context to answer from.
        question (str): The question to answer.
    
    Returns:
        dict: A dictionary with model names as keys and execution times as values.
        dict: A dictionary with model names as keys and answers as values.
    """
    times = {}
    answers = {}

    for model in models:
        answer, elapsed_time = run_model_and_measure_time(model, context, question)
        times[model] = elapsed_time
        answers[model] = answer

    return times, answers


def display_execution_times(times):
    """
    Displays a bar chart comparing the execution times of different models.
    
    Args:
        times (dict): Dictionary containing model names and their execution times.
    """
    model_names = list(times.keys())
    execution_times = list(times.values())

    plt.barh(model_names, execution_times, color='skyblue')
    plt.xlabel('Time (seconds)')
    plt.title('Comparison of Execution Time for Different Models')
    plt.show()


def display_model_answers(models, answers, question):
    """
    Prints the question and the answers given by each model.
    
    Args:
        models (list): List of model names.
        answers (dict): Dictionary of model answers.
        question (str): The original question asked.
    """
    print(f"\nThe Question: {question}")
    for i in range(len(models)-1, -1, -1):
        model = models[i]
        answer = answers[model]
        print(f"\nModel: {model}\nAnswer: {answer}")




def main():
    file_path = upload_file()
    context = process_file(file_path)
    question = get_user_question()

    # models = [
    #     'FacebookAI/xlm-roberta-large',
    #     'deepset/xlm-roberta-large-squad2',
    #     'xlm-roberta-base',
    #     'avichr/heBERT',
    #     'timpal0l/mdeberta-v3-base-squad2',
    #     'tdklab/hebert-finetuned-hebrew-squad'
    # ]
    
    models = [
        'deepset/xlm-roberta-large-squad2',
        'timpal0l/mdeberta-v3-base-squad2',
    ]

    times, answers = run_models_on_question(models, context, question)
    display_execution_times(times)
    display_model_answers(models, answers, question)
main()