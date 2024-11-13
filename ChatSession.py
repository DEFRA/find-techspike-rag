from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever
from haystack.components.embedders import OpenAITextEmbedder
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder
from haystack.dataclasses import ChatMessage, StreamingChunk
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from dotenv import load_dotenv
import yaml
import logging

# Load environment variables
load_dotenv()

# Load configuration from YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Set logging level
logging.basicConfig(level=config["logging_level"])

# Initialize components for the RAG pipeline:
# - ChromaEmbeddingRetriever: Retrieves relevant documents from ChromaDB using embeddings
# - OpenAITextEmbedder: Generates embeddings for input questions using OpenAI's model
# - OpenAIGenerator: Generates responses using OpenAI's language model
# - PromptBuilder: Constructs prompts using retrieved context and chat history

class ChatSession:
    """A class to manage chat interactions with context-aware responses.
    
    Maintains chat history and retrieved context documents to provide
    contextually relevant responses using a RAG (Retrieval Augmented Generation) pipeline.
    """

    def __init__(self, config):
        """Initialize chat session with necessary components."""
        # Vector database to store and retrieve documents
        self.document_store = ChromaDocumentStore(persist_path=config["persist_path"])
        
        # Creates embeddings from text using OpenAI's models
        self.text_embedder = OpenAITextEmbedder(model=config["embedding_model"])
        
        # Retrieves relevant documents from ChromaDB using embeddings
        self.retriever = ChromaEmbeddingRetriever(
            document_store=self.document_store,
            top_k=config["top_k"]
        )
        
        # Generates responses using OpenAI's language models
        self.generator = OpenAIGenerator()
        
        # Builds prompts combining context, history and user input
        self.prompt_builder = PromptBuilder(template=config["template"])
        
        # Stores conversation history
        self.chat_history = []
        
        # Stores retrieved context documents
        self.context_history = []

    def chat(self, question: str) -> str:
        """Process a chat question and return a contextual response.
        
        Args:
            question (str): The user's input question
            
        Returns:
            str: Generated response with source document names
            
        The method:
        1. Embeds the question and retrieves relevant documents
        2. Stores retrieved context
        3. Builds a prompt using context and chat history
        4. Generates a response using the prompt
        5. Updates chat history
        6. Returns response with source citations
        """
        # Embed question and retrieve relevant docs
        embedded_query = self.text_embedder.run(question)
        retrieved_docs = self.retriever.run(embedded_query["embedding"])
        
        # Store context
        self.context_history.extend(retrieved_docs["documents"])
        
        # Build prompt with retrieved context and chat history
        prompt_params = {
            # "documents": retrieved_docs["documents"], 
            "documents": self.context_history,
            "question": question,
            "chat_history": self.chat_history
        }
        prompt = self.prompt_builder.run(**prompt_params)
        
        # Generate answer
        # Send prompt to LLM generator and get response
        response = self.generator.run(prompt["prompt"])
        # Extract first reply from response object as our answer
        answer = response["replies"][0]
        
        # Update chat history
        self.chat_history.append(ChatMessage.from_user(question))
        self.chat_history.append(ChatMessage.from_assistant(answer))
        
        # Get unique source names
        sources = sorted(set(doc.meta['name'] for doc in self.context_history))
        
        # # Return formatted response with sources on new lines
        # sources_text = "\n- ".join(sources)
        # return f"{answer}\n\nSources:\n- {sources_text}"
        return f"{answer}\n\nSources:\n - {', \n - '.join(sources)}" #output the document names

    def reset(self):
        """Reset the chat history and context history."""
        self.chat_history = []
        self.context_history = []

# Ensure no code runs on import
if __name__ == "__main__":

    # Create ChatSession with config
    chat_session = ChatSession(config)
    
    # Example usage - ask a question and print response
    response = chat_session.chat("Write a short description about the character Arya Stark")
    print(response)
