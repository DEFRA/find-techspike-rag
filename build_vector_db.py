from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack import Document
from haystack.components.embedders import OpenAIDocumentEmbedder
from datasets import load_dataset
from dotenv import load_dotenv
import yaml
# from haystack.utils import PipelineMaxComponentRuns

# Load environment variables
load_dotenv()

# Load configuration from YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


def main():
    # Initialize ChromaDB document store with a persistent storage path
    document_store = ChromaDocumentStore(persist_path=config["persist_path"])

    # Load Game of Thrones dataset from Hugging Face
    dataset = load_dataset(config["dataset_name"], split=config["dataset_split"])
    # Convert dataset documents into Haystack Document objects, preserving content and metadata
    docs = [Document(content=doc["content"], meta=doc["meta"]) for doc in dataset]

    # Initialize OpenAI embedder using the configured model
    doc_embedder = OpenAIDocumentEmbedder(
        model=config["embedding_model"],
    )
    
    # Generate embeddings for all documents
    docs_with_embeddings = doc_embedder.run(docs)
    # Store the embedded documents in ChromaDB
    document_store.write_documents(docs_with_embeddings["documents"])

if __name__ == "__main__":
    main()