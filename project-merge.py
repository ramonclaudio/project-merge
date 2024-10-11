import os
import re
import shutil
import fnmatch
import argparse
import subprocess
import importlib.util
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

github_token = os.getenv('GITHUB_ACCESS_TOKEN')

def load_config(config_path):
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return vars(config)

def should_include_file(file_path, root_path, config):
    relative_path = os.path.relpath(file_path, root_path)
    path_parts = Path(relative_path).parts
    for part in path_parts:
        if any(fnmatch.fnmatch(part, pattern) for pattern in config['exclude_patterns']):
            return False
    
    filename = os.path.basename(file_path)
    _, ext = os.path.splitext(filename)
    
    return (ext.lower() in config['include_patterns'] and
            not any(fnmatch.fnmatch(filename, pattern) for pattern in config['exclude_patterns']))

def process_directory(directory_path, combined_content, config):
    for root, dirs, files in os.walk(directory_path):
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in config['exclude_patterns'])]
        
        for filename in files:
            file_path = os.path.join(root, filename)
            if should_include_file(file_path, directory_path, config):
                relative_path = os.path.relpath(file_path, directory_path)
                _, ext = os.path.splitext(filename)
                
                combined_content += f"\n\n`{relative_path}`\n```{ext[1:]}\n"
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        combined_content += content.rstrip()
                except UnicodeDecodeError:
                    combined_content += "# Binary file, contents not displayed"
                combined_content += "\n```"
    return combined_content

def clone_github_repo(url, temp_dir, github_token=None):
    try:
        if github_token:
            url = url.replace('https://', f'https://{github_token}@')
        subprocess.run(['git', 'clone', url, temp_dir], check=True, capture_output=True)
        return temp_dir
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        raise

def get_repo_name_from_url(url):
    match = re.search(r'/([^/]+)/?$', url)
    if match:
        return match.group(1).replace('.git', '')
    return None

def create_directory_tree(directory_path, config):
    def is_directory_empty(path, relative_path):
        for root, dirs, files in os.walk(path):
            rel_root = os.path.relpath(root, directory_path)
            dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(os.path.join(rel_root, d), pattern) for pattern in config['exclude_patterns'])]
            included_files = [f for f in files if should_include_file(os.path.join(root, f), directory_path, config)]
            if included_files:
                return False
        return True

    def build_tree(path, relative_path="", prefix=""):
        if is_directory_empty(path, relative_path):
            return [], []

        tree = []
        root_files = []
        items = sorted(os.listdir(path))
        directories = [item for item in items if os.path.isdir(os.path.join(path, item))]
        files = [item for item in items if os.path.isfile(os.path.join(path, item))]
        
        for i, item in enumerate(directories):
            item_path = os.path.join(path, item)
            item_relative_path = os.path.join(relative_path, item)
            is_last = (i == len(directories) - 1 and not files)
            
            if not any(fnmatch.fnmatch(item_relative_path, pattern) for pattern in config['exclude_patterns']):
                subtree, subfiles = build_tree(item_path, item_relative_path, prefix + ("    " if is_last else "│   "))
                if subtree or subfiles:
                    tree.append(f"{prefix}{'└── ' if is_last else '├── '}{item}/")
                    tree.extend(subtree)
                    root_files.extend(subfiles)

        for i, item in enumerate(files):
            item_path = os.path.join(path, item)
            if should_include_file(item_path, directory_path, config):
                if prefix:
                    tree.append(f"{prefix}{'└── ' if i == len(files) - 1 else '├── '}{item}")
                else:
                    root_files.append(item)

        return tree, root_files

    tree, root_files = build_tree(directory_path)
    root_name = os.path.basename(directory_path)
    
    for i, file in enumerate(sorted(root_files)):
        is_last = (i == len(root_files) - 1)
        tree.append(f"{'└── ' if is_last else '├── '}{file}")

    return f"└── {root_name}/\n" + "\n".join(tree)

def main():
    parser = argparse.ArgumentParser(description="Unify your codebase into a single, LLM-friendly file.")
    parser.add_argument("--config", default="config.py", help="Path to the Python configuration file")
    parser.add_argument("--input_dir", help="Path to the directory containing the code files")
    parser.add_argument("--output_dir", help="Path to the output directory")
    parser.add_argument("--github_url", help="URL of the GitHub repository to process")
    args = parser.parse_args()

    config = load_config(args.config)

    input_dir = args.input_dir or config['default_input_path']
    github_url = args.github_url or config.get('default_github_url')

    output_dir = Path(args.output_dir).resolve() if args.output_dir else Path(config['default_output_path']).resolve() if config['custom_output_path'] else Path(config['default_output_path']).resolve() if config['custom_output_path'] else Path(config['default_output_path']).resolve()

    output_dir.mkdir(parents=True, exist_ok=True)

    temp_dir = None
    try:
        if github_url:
            script_dir = Path(__file__).parent.resolve()
            temp_dir = script_dir / "temp_repo"
            try:
                temp_dir.mkdir(exist_ok=True)
                input_path = Path(clone_github_repo(github_url, str(temp_dir), github_token))
                root_folder_name = get_repo_name_from_url(github_url)
            except Exception as e:
                print(f"Failed to process GitHub repository: {e}")
                return
        elif input_dir:
            input_path = Path(input_dir).resolve()
            root_folder_name = input_path.name
        else:
            print("Error: No input directory or GitHub URL specified in config or command-line arguments.")
            return

        if not input_path.is_dir():
            print(f"Error: {input_path} is not a valid directory")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file_name = f"{root_folder_name}_{timestamp}.md"
        output_file = output_dir / output_file_name

        directory_tree = create_directory_tree(str(input_path), config)

        combined_content = f"# {root_folder_name}\n\n## Directory Tree\n```md\n{directory_tree}\n```"

        combined_content = process_directory(str(input_path), combined_content, config)

        output_file.write_text(combined_content, encoding='utf-8')

        print(f"\nMerged File: {output_file}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
