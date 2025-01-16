from typing import Optional, List, Dict, Any
from openai import OpenAI
from tools import run_command
import os
import json

class CodingAgent:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.base_dir = os.getcwd()
        
    def execute_command(self, command: str) -> None:
        """Execute terminal commands."""
        try:
            result = run_command(command)
            if result:
                print(result)
        except Exception as e:
            print(f"Error executing command: {str(e)}")
    
    def write_file(self, file_path: str, content: str) -> None:
        """Write content to a file."""
        try:
            # Ensure file_path is not empty
            if not file_path:
                raise ValueError("File path cannot be empty")

            # Convert to absolute path if necessary
            if not os.path.isabs(file_path):
                file_path = os.path.join(self.base_dir, file_path)

            # Ensure the directory exists
            directory = os.path.dirname(file_path)
            if directory:  # Only create directory if path has a directory component
                os.makedirs(directory, exist_ok=True)
                
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"File written successfully: {file_path}")
        except Exception as e:
            print(f"Error writing file {file_path}: {str(e)}")
    
    def generate_code(self, prompt: str):
        """Generate code using the AI model."""
        parts = prompt.split("<system>", 1)
        if len(parts) > 1:
            system_content = parts[1].split("</system>")[0].strip()
            user_content = parts[1].split("</system>")[1].strip()
        else:
            system_content = "You are a helpful coding assistant"
            user_content = prompt

        return self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            max_tokens=8000,
            temperature=1.3,
            stream=True
        )

    def process_response(self, response_json: Dict[str, Any]) -> None:
        """Process the JSON response from the AI."""
        # Execute commands
        if "commands" in response_json:
            for cmd in response_json["commands"]:
                if cmd.strip():  # Only execute non-empty commands
                    self.execute_command(cmd)
        
        # Create files
        if "files" in response_json:
            for file_info in response_json["files"]:
                if "path" in file_info and "content" in file_info:
                    if file_info["path"].strip():  # Only create files with non-empty paths
                        self.write_file(file_info["path"], file_info["content"])

def main():
    api_key = input("Enter your DeepSeek API key: ")
    agent = CodingAgent(api_key)
    
    system_prompt = """
    You are a proactive software engineer. You must respond with valid JSON only, no additional text or markdown formatting.

    Your response must follow this structure:
    {
        "commands": [
            "command1",
            "command2"
        ],
        "files": [
            {
                "path": "path/to/file1",
                "content": "file content here"
            },
            {
                "path": "path/to/file2",
                "content": "file content here"
            }
        ],
        "explanation": "Optional explanation of what the code does"
    }

    When creating a project, you must:
    1. Create a root directory for the project.
    2. Create all necessary subdirectories (e.g., 'static', 'templates' for Flask).
    3. Generate all required files with their appropriate content.
    4. Include any necessary commands to set up the project (e.g., installing dependencies).

    For example, if the user asks for a Flask "Hello World" app, you should create:
    - A root directory (e.g., 'helloworld_app').
    - A 'static' directory with a 'style.css' file.
    - A 'templates' directory with an 'index.html' file.
    - An 'app.py' file with the Flask application code.
    - Commands to install Flask (e.g., 'pip install flask').

    Always ensure the project structure is complete and ready to run.
    """

    while True:
        user = input("\nEnter your prompt (or 'quit' to exit): ")
        if user.lower() == 'quit':
            break
            
        prompt = f"<system>{system_prompt}</system>\n{user}"
        
        current_response = ""
        print("\nGenerating response...")
        for chunk in agent.generate_code(prompt):
            if hasattr(chunk.choices[0].delta, 'content'):
                text = chunk.choices[0].delta.content
                if text:
                    current_response += text
        
        # Parse and process the JSON response
        try:
            if current_response:
                # Find the first { and last } to extract the JSON object
                start = current_response.find('{')
                end = current_response.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = current_response[start:end]
                    response_data = json.loads(json_str)
                    
                    print("\nExecuting commands and creating files...")
                    # Process the response
                    agent.process_response(response_data)
                    
                    # Print explanation if available
                    if "explanation" in response_data:
                        print(f"\nExplanation: {response_data['explanation']}")
                else:
                    print("\nError: No valid JSON found in the response")
        except json.JSONDecodeError as e:
            print(f"\nError parsing JSON response: {str(e)}")
            print("Raw response:", current_response)
        except Exception as e:
            print(f"\nError processing response: {str(e)}")

if __name__ == "__main__":
    main()