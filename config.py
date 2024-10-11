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

# Set of patterns to include in the code merge process
include_patterns = {
    # Web Development
    '.html', '.htm', '.css', '.scss', '.sass', '.less',
    '.js', '.ts', '.jsx', '.tsx',
    '.vue', '.svelte',
    '.php', '.asp', '.jsp', '.mjs',

    # Backend Development
    '.py',    # Python
    '.rb',    # Ruby
    '.java',  # Java
    '.cs',    # C#
    '.go',    # Go
    '.rs',    # Rust
    '.scala', # Scala
    '.kt',    # Kotlin
    '.groovy',# Groovy
    '.clj',   # Clojure
    '.coffee',# CoffeeScript
    '.ex', '.exs',  # Elixir
    '.hs',    # Haskell
    '.lua',   # Lua
    '.pl',    # Perl
    '.r',     # R

    # Systems Programming
    '.c', '.cpp', '.h', '.hpp', '.cc', '.cxx',
    '.m', '.mm',  # Objective-C
    '.swift',

    # Data and Configuration
    '.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.conf', '.cfg',

    # Database
    '.sql', '.prisma', '.graphql', '.gql',

    # Shell and Scripting
    '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd',

    # Documentation
    '.md', '.markdown', '.txt', '.rst', '.tex',

    # Data Files
    '.csv', '.tsv',

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

    # Server Configuration
    '.htaccess',
    '.nginx',
    '.service',  # systemd service files

    # Other
    '.proto',  # Protocol Buffers
    '.dockerfile',
    '.editorconfig',
    '.plist',    # property list files (macOS)
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
    'local_settings.py',
    'celerybeat-schedule', 'celerybeat.pid',

    # JavaScript/Node.js
    'node_modules', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    '.next', 'out',
    'npm-debug.log*', 'yarn-debug.log*', 'yarn-error.log*', 'lerna-debug.log*',
    '.pnpm-debug.log*',
    'report.[0-9]*.[0-9]*.[0-9]*.[0-9]*.json',
    'pids', '*.seed', '*.pid.lock',
    'lib-cov',
    'coverage', '*.lcov',
    '.nyc_output',
    '.grunt',
    'bower_components',
    '.lock-wscript',
    'build/Release',
    'jspm_packages/',
    'web_modules/',
    '*.tsbuildinfo',
    '.npm',
    '.eslintcache',
    '.stylelintcache',
    '.rpt2_cache/', '.rts2_cache_cjs/', '.rts2_cache_es/', '.rts2_cache_umd/',
    '.node_repl_history',
    '*.tgz',
    '.yarn-integrity',
    '.cache', '.parcel-cache',
    '.nuxt',
    '.docusaurus',
    '.serverless/',
    '.fusebox/',
    '.dynamodb/',
    '.tern-port',
    '.vscode-test',
    '.yarn/cache', '.yarn/unplugged', '.yarn/build-state.yml', '.yarn/install-state.gz', '.pnp.*',

    # Ruby
    'Gemfile.lock',

    # Java
    '*.class', '*.jar',

    # C/C++
    '*.o', '*.ko', '*.obj', '*.elf', '*.ilk', '*.map', '*.exp', '*.gch', '*.pch',
    '*.lib', '*.a', '*.la', '*.lo', '*.dll', '*.so', '*.so.*', '*.dylib',

    # Swift and Xcode
    'Info.plist',
    'Preview Content',
    'xcuserdata/',
    '*.xcassets',
    '*.xcodeproj',
    '*.pbxproj',
    '*.hmap',
    '*.ipa',
    '*.dSYM.zip',
    '*.dSYM',
    'timeline.xctimeline',
    'playground.xcworkspace',
    '.build/',
    'Carthage/Build/',
    'fastlane/report.xml',
    'fastlane/Preview.html',
    'fastlane/screenshots/**/*.png',
    'fastlane/test_output',
    '*Tests',
    '*UITests',

    # IDEs and Editors
    '.idea', '.vscode', '.cursorignore', '.cursorrules',
    '.spyderproject', '.spyproject', '.ropeproject',

    # Version Control
    '.git', '.github',

    # Databases
    '*.sqlite', '*.db', 'db.sqlite3', 'db.sqlite3-journal',

    # Logs and Temporary Files
    'logs', '*.log', '*.tmp', '*.temp', '*.swp', '*.bak', '*.pid',

    # OS-specific
    '.DS_Store', 'Thumbs.db',

    # Build and Dependency Directories
    'build', 'dist', 'target', 'out',

    # Environment and Configuration
    '.env', '.env*', '.env.development.local', '.env.test.local', '.env.production.local', '.env.local',
    '.venv', 'env', 'venv', 'ENV',

    # Documentation
    'docs/_build', '/site',

    # Testing and Coverage
    'htmlcov', '.coverage',

    # Translations
    '*.mo', '*.pot',

    # Web Development
    '.webassets-cache',
    '.vuepress/dist',
    '.temp',

    # Web Scraping
    '.scrapy',

    # Docker
    'Dockerfile',

    # Flask
    'instance',

    # Licensing
    'LICENSE',

    # Other
    '.cache',
    'dist',

    # Firebase
    'GoogleService-Info.plist',
    'firebase-debug.log',

     # Custom Directories
    '.private',
    'merged-files',
    'temp_repo',
}