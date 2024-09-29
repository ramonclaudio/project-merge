from pathlib import Path

# Get the directory of the current file (config.py)
current_dir = Path(__file__).parent.resolve()

# Default paths for input and output
# These paths are used if no command-line arguments are provided

# Default input path (set to None if not using)
default_input_path = None

# Default output path if custom output path is not provided
default_output_path = current_dir / "merged-files"

# Custom output path (set to None if not using)
custom_output_path = None

# GitHub URL (set to None if not using)
default_github_url = None

# Set of file extensions to include in the code merge process
include_patterns = {
    # Web Development
    '.html', '.htm', '.css', '.scss', '.sass', '.less',
    '.js', '.ts', '.jsx', '.tsx',
    '.vue', '.svelte',
    '.php', '.asp', '.jsp',

    # Backend Development
    # Python
    '.py',
    # Ruby
    '.rb',
    # Java
    '.java',
    # C#
    '.cs',
    # Go
    '.go',
    # Rust
    '.rs',
    # Scala
    '.scala',
    # Kotlin
    '.kt',
    # Groovy
    '.groovy',
    # Clojure
    '.clj',
    # CoffeeScript
    '.coffee',
    # Elixir
    '.ex', '.exs',
    # Haskell
    '.hs',
    # Lua
    '.lua',
    # Perl
    '.pl',
    # R
    '.r',

    # Data and Configuration
    '.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.conf', '.cfg',

    # Database
    '.sql', '.prisma', '.graphql', '.gql',

    # Shell and Scripting
    '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd',

    # Systems Programming
    '.c', '.cpp', '.h', '.hpp', '.cc', '.cxx',
    '.m', '.mm',  # Objective-C
    '.swift',

    # Documentation
    '.md', '.markdown', '.txt', '.rst', '.tex',

    # Data Files
    '.csv', '.tsv',

    # Other
    '.proto',  # Protocol Buffers
    '.dockerfile',
    '.editorconfig',
    '.htaccess',
    '.nginx',
    '.service',  # systemd service files
    '.plist',    # property list files (macOS)

    # Project Configuration
    '.gitignore',
    '.dockerignore',
    'Dockerfile',
    'docker-compose.yml',
    'docker-compose.yaml',
    'requirements.txt',
    'setup.py',
    'setup.cfg',
    'pyproject.toml',
    'package.json',
    'Gemfile',
    'pnpm-workspace.yaml',
    'README.md',

    # CI/CD Configuration
    '.travis.yml',
    '.gitlab-ci.yml',
    'Jenkinsfile',
}

# Set of patterns to exclude from the merge process
exclude_patterns = {
    # Python
    '__pycache__', '*.py[cod]', '*$py.class', '*.so',
    '.Python', 'build', 'develop-eggs', 'dist', 'downloads', 'eggs', '.eggs',
    'lib', 'lib64', 'parts', 'sdist', 'var', 'wheels', 'share/python-wheels',
    '*.egg-info', '.installed.cfg', '*.egg', 'MANIFEST',
    '*.manifest', '*.spec',
    'pip-log.txt', 'pip-delete-this-directory.txt',
    '.tox', '.nox', '.coverage', '.coverage.*', '.cache',
    'nosetests.xml', 'coverage.xml', '*.cover', '*.py,cover', '.hypothesis',
    '.pytest_cache', 'cover',
    '.pybuilder', 'target',
    '.ipynb_checkpoints',
    'profile_default', 'ipython_config.py',
    'Pipfile.lock', 'poetry.lock',
    '.pdm.toml', '.pdm-python', '.pdm-build',
    '__pypackages__',
    '*.sage.py',
    '.mypy_cache', '.dmypy.json', 'dmypy.json',
    '.pyre', '.pytype',
    'cython_debug',

    # JavaScript/Node.js
    'node_modules', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    '.next',

    # Ruby
    'Gemfile.lock',

    # Java
    '*.class', '*.jar',

    # C/C++
    '*.o', '*.ko', '*.obj', '*.elf', '*.ilk', '*.map', '*.exp', '*.gch', '*.pch',
    '*.lib', '*.a', '*.la', '*.lo', '*.dll', '*.so', '*.so.*', '*.dylib',

    # IDEs and Editors
    '.idea', '.vscode', '.cursorignore', '.cursorrules'

    # Version Control
    '.git', '.github',

    # Databases
    '*.sqlite', '*.db',

    # Logs and Temporary Files
    '*.log', '*.tmp', '*.temp', '*.swp', '*.bak', '*.pid',

    # OS-specific
    '.DS_Store', 'Thumbs.db',

    # Build and Dependency Directories
    'build', 'dist', 'target', 'out',

    # Environment and Configuration
    '.env*', '.venv', 'env', 'venv', 'ENV',

    # Documentation
    'docs/_build', '/site',

    # Testing and Coverage
    'htmlcov', '.coverage',

    # Translations
    '*.mo', '*.pot',

    # Web Development
    '.webassets-cache',

    # Task Runners and Build Tools
    'celerybeat-schedule', 'celerybeat.pid',

    # Custom Directories
    '/dev',

    # Other
    'LICENSE', 'local_settings.py', 'db.sqlite3', 'db.sqlite3-journal',
    '.spyderproject', '.spyproject', '.ropeproject', 'instance',
    '.scrapy', 'Dockerfile'
}