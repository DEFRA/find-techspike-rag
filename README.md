# Project Name

## Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline using Haystack and OpenAI models. It is designed to provide context-aware responses by retrieving relevant documents and generating answers based on the retrieved context and chat history.

## Features

- **ChromaEmbeddingRetriever**: Retrieves relevant documents from ChromaDB using embeddings.
- **OpenAITextEmbedder**: Generates embeddings for input questions using OpenAI's model.
- **OpenAIGenerator**: Generates responses using OpenAI's language model.
- **PromptBuilder**: Constructs prompts using retrieved context and chat history.

## Installation

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add necessary environment variables, such as `OPENAI_API_KEY`.

## Configuration

- The configuration is managed via a `config.yaml` file. Key parameters include:
  - `persist_path`: Path for ChromaDB persistence.
  - `embedding_model`: Model used for generating embeddings.
  - `top_k`: Number of top documents to retrieve.
  - `template`: Template for prompt building.

## Usage

1. Build the vector database:
   ```bash
   python build_vector_db.py
   ```

2. Start a chat session:
   ```bash
   python initiate_chat.py
   ```

3. Example usage:
   ```bash
   python initiate_chat.py
   ```
   - Ask a question and receive a response with source document names.

## Code Structure

- **initiate_chat.py**: Main script to initiate chat sessions.
- **build_vector_db.py**: Script to build the vector database using ChromaDocumentStore.
- **spike_notebooks/**: Contains Jupyter notebooks for experimentation and testing.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.