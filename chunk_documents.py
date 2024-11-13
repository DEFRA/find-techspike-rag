from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from pathlib import Path
import os
from openai import OpenAI
import argparse
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_topic_summary(text):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """You are a topic modeling assistant which determines the main message from a set of similar sentences. 
                Generate a very brief topic that captures the main theme of the text."""
            },
            {
                "role": "user",
                "content": f"Generate a brief topic for this text: {text}"
            }
        ],
        temperature=0.3,
        max_tokens=20
    )
    return response.choices[0].message.content.strip()

def process_document(file_path, n_clusters=8):
    # Read the contents
    with open(file_path, 'r') as f:
        text = f.read()

    # Initialize the SBERT model
    model = SentenceTransformer('all-mpnet-base-v2')
    
    # Split document into sentences
    sentences = text.split(".")
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    # Generate embeddings
    sentence_embeddings = model.encode(sentences)
    
    # Perform clustering
    clustering_model = AgglomerativeClustering(n_clusters=n_clusters)
    clustering_model.fit(sentence_embeddings)
    
    # Group sentences by cluster
    clusters = {}
    for sentence_id, cluster_id in enumerate(clustering_model.labels_):
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(sentences[sentence_id])
    
    # Process clusters and generate documents
    documents = []
    for cluster_id, cluster_sentences in clusters.items():
        cluster_text = " ".join(cluster_sentences)
        topic = get_topic_summary(cluster_text)
        documents.append({
            'id': cluster_id,
            'content': cluster_text,
            'metadata': {
                'topic': topic,
                'source_file': Path(file_path).name
            }
        })
    return documents

def save_chunks_to_file(documents, output_file):
    """Save chunks to a formatted text file"""
    with open(output_file, 'w') as f:
        for doc in documents:
            f.write(f"\nChunk {doc['id']} - Topic: {doc['metadata']['topic']}\n")
            f.write(f"Source: {doc['metadata']['source_file']}\n")
            f.write("-" * 80 + "\n")
            # Split content back into sentences for readability
            sentences = doc['content'].split(". ")
            for sentence in sentences:
                if sentence.strip():
                    f.write(f" - {sentence.strip()}.\n")
            f.write("\n")

def main():
    parser = argparse.ArgumentParser(description='Process documents using sentence transformers')
    parser.add_argument('--input_dir', type=str, default='data/actions',
                       help='Directory containing input text files')
    parser.add_argument('--n_clusters', type=int, default=8,
                       help='Number of clusters for document chunking')
    parser.add_argument('--output_file', type=str,
                       help='Optional output file to save chunks (e.g., chunks.txt)')
    
    args = parser.parse_args()
    
    # Get the project root directory and data path
    project_root = Path.cwd()
    data_dir = project_root / args.input_dir
    
    if not os.path.exists(data_dir):
        logging.error(f"Input directory {data_dir} does not exist!")
        return
    
    # Process all text files
    text_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
    
    if not text_files:
        logging.error(f"No text files found in {data_dir}")
        return
        
    all_documents = []
    
    for file_name in text_files:
        file_path = os.path.join(data_dir, file_name)
        logging.info(f"Processing file: {file_name}")
        documents = process_document(file_path, args.n_clusters)
        all_documents.extend(documents)
    
    logging.info(f"Processed {len(all_documents)} chunks from {len(text_files)} files")
    
    if args.output_file:
        save_chunks_to_file(all_documents, args.output_file)
        logging.info(f"Saved chunks to {args.output_file}")
    
    # Print summary of processing
    print("\nProcessing Summary:")
    print("-" * 50)
    for doc in all_documents:
        print(f"Chunk {doc['id']}:")
        print(f"Topic: {doc['metadata']['topic']}")
        print(f"Source: {doc['metadata']['source_file']}")
        print("-" * 50)

if __name__ == "__main__":
    main()

        