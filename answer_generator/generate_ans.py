from extraction_doc import extract_text_from_file, clean_text
import time
from transformers import pipeline
import os
import shutil


def run_model_and_measure_time(model_name, context, question, top_k=3):
    """
    Runs a question-answering model on a given context and question, and measures the time taken to get the answers.

    Args:
        model_name (str): The name or path of the pre-trained model to be used for question-answering.
        context (str): The text from which the model should extract the answer.
        question (str): The question to be answered based on the context.
        top_k (int): The number of possible answers to return.

    Returns:
        tuple: 
            - list: A list of extracted answers from the model.
            - float: The time taken to process the question and return the answers (in seconds).
    """
    qa_pipeline = pipeline('question-answering', model=model_name)

    start_time = time.time()
    results = qa_pipeline(question=question, context=context, top_k=top_k)
    end_time = time.time()

    elapsed_time = end_time - start_time

    # Return all possible answers
    answers = [result['answer'] for result in results]
    return answers, elapsed_time


def run_models_on_question(models, context, question, top_k=3):
    """
    Runs each model on the given context and question, records the answers and execution time.
    
    Args:
        models (list): List of model names to run.
        context (str): The text context to answer from.
        question (str): The question to answer.
        top_k (int): The number of answers to return.

    Returns:
        dict: A dictionary with model names as keys and execution times as values.
        dict: A dictionary with model names as keys and lists of answers as values.
    """
    times = {}
    answers = {}

    for model in models:
        model_answers, elapsed_time = run_model_and_measure_time(model, context, question, top_k=top_k)
        times[model] = elapsed_time
        answers[model] = model_answers

    return times, answers


def display_model_answers(models, answers, question):
    """
    Prints the question and the answers given by each model.
    
    Args:
        models (list): List of model names.
        answers (dict): Dictionary of model answers.
        question (str): The original question asked.
    """
    print(f"\n\n\n\nThe Question: {question}\n")
    for model in models:
        model_answers = answers[model]
        print(f"Model: {model}")
        for idx, answer in enumerate(model_answers, start=1):
            if answer.endswith(','):
                answer = answer[:-1] + '.'
            elif not answer.endswith('.'):
                answer += '.'
            print(f"Answer {idx}: {answer}")



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


def contaxt_to_generate_directory_lisener(question):
    dir_name = r'data\context_to_generate_ans'  # directory to listen for new files
    fin_dir = r"data\finshed\finished_context"
    
    
    for file in os.listdir(dir_name):
        context = read_file(os.path.join(dir_name, file))
        models = ['timpal0l/mdeberta-v3-base-squad2']
        times, answers = run_models_on_question(models, context, question)
        display_model_answers(models, answers, question)
        
        

        
