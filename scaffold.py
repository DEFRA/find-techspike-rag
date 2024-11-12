import subprocess
import logging
import yaml
# Load configuration from YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Set logging level
logging.basicConfig(level=config["logging_level"], format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_name):
    try:
        logging.info(f"Starting {script_name}")
        subprocess.run(["python", script_name], check=True)
        logging.info(f"Successfully completed {script_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running {script_name}: {e}")

def main():
    # Step 1: Build the vector database
    logging.info("Building vector database...")
    # run_script("build_vector_db.py")
    
    # Step 2: Initiate the chat session
    logging.info("Initiating chat session...")
    run_script("initiate_chat.py")
    
    # Step 3: Launch the web frontend
    logging.info("Launching web frontend...")
    run_script("frontend.py")

if __name__ == "__main__":
    main()