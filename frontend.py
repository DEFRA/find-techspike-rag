from ChatSession import ChatSession
import gradio as gr
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load configuration from YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Create a global chat session
chat_session = ChatSession(config)

def chat_response(message, history):
    return chat_session.chat(message)

def reset_chat():
    chat_session.reset()
    return None

def main():
    with gr.Blocks() as demo:
        gr.Markdown("# Game of Thrones Chat")
        gr.Markdown("Ask questions about Game of Thrones")
        
        chatbot = gr.ChatInterface(
            fn=chat_response,
            chatbot=gr.Chatbot(height=500),
            textbox=gr.Textbox(scale=7, container=False, min_width=600),
        )
        
        reset_btn = gr.Button("Reset Chat History")
        reset_btn.click(fn=reset_chat, outputs=chatbot)
    
    demo.launch(share=False)

if __name__ == "__main__":
    main() 