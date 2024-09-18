from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
import numpy as np

# Connect to Milvus
connections.connect(alias="default", host='localhost', port='19530')

# Define the schema for Milvus Collection
fields = [
    FieldSchema(name="question_vector", dtype=DataType.FLOAT_VECTOR, dim=128, is_primary=False),
    FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=512)
]

schema = CollectionSchema(fields, description="Chat Q&A Collection")
collection = Collection("qa_collection", schema)

# Ensure collection exists
if not collection.has_collection("qa_collection"):
    collection.create_index(field_name="question_vector", index_params={"index_type": "IVF_FLAT", "params": {"nlist": 128}})
    collection.load()

def insert_question_answer(question, answer):
    # Convert the question into a random vector (you can replace this with actual embedding logic)
    question_vector = np.random.rand(128).tolist()

    # Insert the question, vector, and answer into Milvus
    collection.insert([question_vector, question, answer])

def search_question(question_vector, top_k=5):
    # Perform search with the provided vector and return the top_k results
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search([question_vector], anns_field="question_vector", param=search_params, limit=top_k)
    return results
