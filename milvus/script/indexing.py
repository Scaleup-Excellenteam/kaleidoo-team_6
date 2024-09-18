from pymilvus import FieldSchema, CollectionSchema, DataType, Collection, connections, utility
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import time
import shutil


def connect_to_milvus(host="localhost", port="19530"):
    connections.connect("default", host=host, port=port)
    print("Connected to Milvus")


def create_collection():
    vector_field = FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=768) 
    id_field = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True)
    schema = CollectionSchema(fields=[id_field, vector_field], description="Text to vector example")
    collection = Collection(name="text_collection", schema=schema)
    print("Collection created")
    return collection


def load_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return [line.strip() for line in lines] 


def text_to_vector(model, text):
    return model.encode(text)


def insert_data(collection, texts, model):
    vectors = [text_to_vector(model, text) for text in texts] 
    ids = list(range(len(texts)))  
    collection.insert([ids, vectors])
    print("Data inserted")


def build_index(collection):
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 100}
    }
    collection.create_index(field_name="vector", index_params=index_params)
    print("Index built")


def load_collection(collection):
    collection.load()
    print("Collection loaded into memory")

def search_by_question(collection, model, question, texts):
    query_vector = text_to_vector(model, question)  
    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 10}
    }
    results = collection.search(
        data=[query_vector],
        anns_field="vector",
        param=search_params,
        limit=5 
    )
    
    print("Search results:")
    for result in results:
        for match in result:
            original_text = texts[match.id] 
            print(f"ID: {match.id}, Distance: {match.distance}, Text: {original_text}")
    
    return results


def get_or_create_collection():
    if utility.has_collection("text_collection"):
        collection = Collection("text_collection")
        print("Collection loaded from Milvus")
    else:
        collection = create_collection()
    return collection

def directory_not_empty(directory):
    return bool(os.listdir(directory))



def get_context(question):
    connect_to_milvus()
    collection = get_or_create_collection()
    model = SentenceTransformer('paraphrase-mpnet-base-v2')
    file_dir = r'data\extracted_text_from_media'
    proc_dir = r"data\processed_files"
    
    for file in os.listdir(file_dir):
        file_path = os.path.join(file_dir, file) 
        text = load_data_from_file(file_path)
        shutil.move(file_path, proc_dir)
        print("inserting data...\n")
        insert_data(collection, text, model)
        print("building index...\n")
        build_index(collection)
        print("loading collection...\n")
        load_collection(collection)
     
    print("searching by question...\n")   
    context = search_by_question(collection, model, question, text)
    

    print("saving context to file...\n")  
    saved_context_dir = r"data\context_to_generate_ans"
    output_file_name = "context.txt"
    output_file_path = os.path.join(saved_context_dir, output_file_name)
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for result in context:
            for match in result:
                f.write(f"ID: {match.id}, Distance: {match.distance}, Text: {text[match.id]}\n")
    
    print(f"Context saved to {output_file_path}")

    
    
    
        
    
    
   


# if __name__ == "__main__":
#     connect_to_milvus()
#     collection = get_or_create_collection()
#     model = SentenceTransformer('paraphrase-mpnet-base-v2')
#     file_dir = r"doc_extraction\data\fixed_files"
#     proc_dir = r"doc_extraction\data\processed_files"
 
    
#     while True:
#         if directory_not_empty(file_dir):
#             for file in os.listdir(file_dir):
#                 file_path = os.path.join(file_dir, file) 
#                 text = load_data_from_file(file_path)
#                 shutil.move(file_path, proc_dir)
#                 insert_data(collection, text, model)
#                 build_index(collection)
#                 load_collection(collection)
#         else:
#             print("No new files to process. Sleeping for 3 seconds.")
#             time.sleep(3)

#         choice = input("Do you want to search for a question? (y/n): ")
#         if choice.lower() != 'y':
#             break
        
#         question = input("Enter your question: ")
#         search_by_question(collection, model, question, text)  




