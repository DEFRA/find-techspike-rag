from ChatSession import ChatSession
import yaml

# Load configuration from YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

def main():
    # Create ChatSession with config
    chat_session = ChatSession(config)
    
    print("Type 'exit' to quit or 'reset' to clear chat history")
    while True:
        question = input("\nAsk a question about Game of Thrones: ")
        if question.lower() == 'exit':
            print("Exiting the chat session.")
            break
        elif question.lower() == 'reset':
            chat_session.reset()
            print("Chat history has been reset.")
            continue
            
        response = chat_session.chat(question)
        print(f"Assistant: {response}\n")

if __name__ == "__main__":
    main() 