from initiate_chat import ChatSession
import yaml

# Load configuration from YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

def main():
    # Create ChatSession with config
    chat_session = ChatSession(config)
    
    while True:
        question = input("Ask a question about Game of Thrones (type 'exit' to quit): ")
        if question.lower() == 'exit':
            print("Exiting the chat session.")
            break
        response = chat_session.chat(question)
        print(f"Assistant: {response}\n")

if __name__ == "__main__":
    main() 