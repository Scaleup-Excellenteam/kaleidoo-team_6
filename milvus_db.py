from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
from sentence_transformers import SentenceTransformer
import numpy as np

# Establish connection with Milvus
connections.connect()

# Load a pre-trained model for embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define your schema
def create_collection():
    question_field = FieldSchema(name="question", dtype=DataType.FLOAT_VECTOR, dim=384)  # 384 is the dimension of the embedding model output
    answer_field = FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=1000)

    schema = CollectionSchema(fields=[question_field, answer_field], description="QA collection")
    collection = Collection(name="qa_collection", schema=schema)
    return collection

# Embed a question into a vector
def embed_text(text):
    return model.encode(text).tolist()

# Insert question-answer pairs into Milvus
def insert_question_answer(question, answer):
    collection = Collection("qa_collection")

    # Embed the question into a vector
    question_vector = embed_text(question)

    # Prepare data for insertion
    data = [
        [question_vector],  # Question vector
        [answer]            # Answer text
    ]

    # Insert data into the collection
    collection.insert(data)

# Create the collection (run once, or you can check if it already exists)
collection = create_collection()
