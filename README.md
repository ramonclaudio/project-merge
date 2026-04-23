# project-merge

I wanted to paste entire projects into Claude or ChatGPT without manually opening every file or fighting upload limits. Nothing clean existed yet. So I built this: point it at a local directory or a GitHub URL, get back one Markdown file with every code file wrapped in a fenced block. Respects include/exclude patterns in `config.py`.

Python utility that consolidates a codebase into a single LLM-friendly Markdown file.

## Install

```bash
git clone https://github.com/ramonclaudio/project-merge.git
cd project-merge
pip install -r requirements.txt
```

## Usage

```bash
# Merge a local directory
python project-merge.py --input_path /path/to/project

# Merge a GitHub repo
python project-merge.py --github_url https://github.com/owner/repo

# Custom output directory (default: merged-files)
python project-merge.py --input_path /path/to/project --output_path /path/to/output
```

For private GitHub repos, set a `GITHUB_ACCESS_TOKEN` in `.env`.

## Configuration

`config.py` holds the include/exclude patterns and default paths. Include patterns default to common web/backend/config file extensions. Exclude patterns skip `node_modules`, `.git`, build artifacts, and the usual suspects.

## License

MIT
