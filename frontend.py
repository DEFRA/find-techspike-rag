from ChatSession import ChatSession
import gradio as gr
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load configuration from YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

def chat_response(message, history):
    chat_session = ChatSession(config)
    return chat_session.chat(message)

def main():
    demo = gr.ChatInterface(
        fn=chat_response,
        title="Game of Thrones Chat",
        description="Ask questions about Game of Thrones",
    )
    demo.launch(share=False)

if __name__ == "__main__":
    main() 