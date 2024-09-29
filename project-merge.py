import os
import re
import shutil
import fnmatch
import argparse
import subprocess
import importlib.util
from pathlib import Path
from datetime import datetime

def load_config(config_path):
    # Load the config file
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return vars(config)

def should_include_file(file_path, config):
    # Check if the file should be included based on the config
    path_parts = Path(file_path).parts
    for part in path_parts:
        if any(fnmatch.fnmatch(part, pattern) for pattern in config['exclude_patterns']):
            return False
    
    # Get the filename and extension
    filename = os.path.basename(file_path)
    _, ext = os.path.splitext(filename)
    
    # Check if the file extension is in the include patterns and not excluded
    return (ext.lower() in config['include_patterns'] and
            not any(fnmatch.fnmatch(filename, pattern) for pattern in config['exclude_patterns']))

def process_directory(directory_path, combined_content, config):
    # Walk through the directory and process each file
    for root, dirs, files in os.walk(directory_path):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in config['exclude_patterns'])]
        
        # Process each file in the directory
        for filename in files:
            file_path = os.path.join(root, filename)
            if should_include_file(file_path, config):
                relative_path = os.path.relpath(file_path, directory_path)
                _, ext = os.path.splitext(filename)
                
                # Add file content to the combined content with Markdown formatting
                combined_content += f"\n\n`{relative_path}`\n```{ext[1:]}\n"
                try:
                    # Read the file content
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        combined_content += content
                except UnicodeDecodeError:
                    # Handle binary files gracefully
                    combined_content += "# Binary file, contents not displayed"
                combined_content += "\n```"
    return combined_content

def clone_github_repo(url, temp_dir):
    # Clone the GitHub repository
    try:
        subprocess.run(['git', 'clone', url, temp_dir], check=True, capture_output=True)
        return temp_dir
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        raise

def get_repo_name_from_url(url):
    # Extract the repository name from the URL
    match = re.search(r'/([^/]+)/?$', url)
    if match:
        return match.group(1).replace('.git', '')
    return None

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Unify your codebase into a single, LLM-friendly file.")
    parser.add_argument("--config", default="config.py", help="Path to the Python configuration file")
    parser.add_argument("--input_dir", help="Path to the directory containing the code files")
    parser.add_argument("--output_dir", help="Path to the output directory")
    parser.add_argument("--github_url", help="URL of the GitHub repository to process")
    args = parser.parse_args()

    # Load the configuration file
    config = load_config(args.config)

    # Use command-line arguments if provided, otherwise fall back to config defaults
    if args.output_dir:
        output_dir = Path(args.output_dir).resolve()
    elif config['custom_output_path']:
        output_dir = Path(config['custom_output_path']).resolve()
    else:
        output_dir = Path(config['default_output_path']).resolve()

    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get the GitHub URL if provided, otherwise use the default URL from config
    github_url = args.github_url or config['default_github_url']

    # Check if both GitHub URL and input directory are specified, if so, error out
    if github_url and args.input_dir:
        print("Error: Please specify either a GitHub URL or an input directory, not both.")
        return

    # Initialize the temporary directory
    temp_dir = None
    try:
        # Handle GitHub URL if provided
        if github_url:
            script_dir = Path(__file__).parent.resolve()
            temp_dir = script_dir / "temp_repo"
            try:
                # Create the temporary directory if it doesn't exist
                temp_dir.mkdir(exist_ok=True)
                input_path = Path(clone_github_repo(github_url, str(temp_dir)))
                root_folder_name = get_repo_name_from_url(github_url)
            except Exception as e:
                print(f"Failed to process GitHub repository: {e}")
                return
        elif args.input_dir:
            input_path = Path(args.input_dir).resolve()
            root_folder_name = input_path.name
        else:
            print("Error: Please specify either a GitHub URL or an input directory.")
            return

        # Check if the input path is a valid directory
        if not input_path.is_dir():
            print(f"Error: {input_path} is not a valid directory")
            return

        # Generate a unique filename using timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file_name = f"{root_folder_name}_{timestamp}.md"
        output_file = output_dir / output_file_name

        # Simplified header for the combined content
        combined_content = f"# {root_folder_name}\n"

        combined_content = process_directory(str(input_path), combined_content, config)

        # Write the combined content to the output file
        output_file.write_text(combined_content, encoding='utf-8')

        print(f"All files have been combined into {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Clean up the temporary directory if it was created
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()