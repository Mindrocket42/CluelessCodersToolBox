import os

def create_directory_structure(structure_text):
    # Split the text into lines and clean them
    lines = [line.rstrip('\n') for line in structure_text.split('\n') if line.strip()]
    
    # folder holding root folder goes here (inside the speech marks)
    base_path = r"FOLDER LOCATION"  
    current_path = base_path
    path_stack = []

    for line in lines:
        # Count leading spaces to determine indentation level
        indent = len(line) - len(line.lstrip())
        indent_level = indent // 4  # Assuming 4 spaces per indent level
        
        # Clean the line
        clean_line = line.lstrip().replace('│', '').replace('├──', '').replace('└──', '').replace('─', '').strip()
        
        # Skip empty lines or lines with just tree characters
        if not clean_line or all(c in '│├└─' for c in clean_line):
            continue
            
        # Remove comments
        clean_line = clean_line.split('#')[0].strip()
        
        # Adjust path stack based on indentation
        while len(path_stack) > indent_level:
            path_stack.pop()
            
        if not path_stack:
            current_path = base_path
        else:
            current_path = os.path.join(base_path, *path_stack)
            
        # Add current item to path
        path_stack.append(clean_line.rstrip('/'))
        full_path = os.path.join(base_path, *path_stack)
        
        # Create directory or file
        if clean_line.endswith('/'):
            if not os.path.exists(full_path):
                os.makedirs(full_path)
                print(f"Created directory: {full_path}")
        else:
            # Ensure parent directory exists
            parent_dir = os.path.dirname(full_path)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
            
            # Create file
            if not os.path.exists(full_path):
                with open(full_path, 'w') as f:
                    pass
                print(f"Created file: {full_path}")

# File structure formatted as makdown goes here. Below is an example placeholder
markdown_structure = '''
ProjectRoot/
│
├── README.md                          # Project overview and documentation
├── package.json                       # Node.js project file with dependencies and metadata
├── .gitignore                         # List of files and directories to ignore in Git
│
├── src/                               # Source code directory
│   ├── app.js                         # Main application logic
│   ├── utils.js                       # Utility functions and helpers
│   ├── config.json                    # Configuration settings for the application
│   └── README.md                      # Documentation for the source code
│
├── assets/                            # Resources such as images and styles
│   ├── images/
│   │   ├── logo.png                   # Company or project logo
│   │   └── background.jpg             # Background image for UI or website
│   │
│   ├── styles/
│   │   ├── main.css                   # Main stylesheet for application
│   │   └── theme.css                  # Additional styles for themes
│   │
│   └── favicon.ico                    # Small icon for browser tabs
│
├── docs/                              # Documentation files
│   ├── user-guide.docx                # Step-by-step guide for users
│   ├── changelog.txt                  # List of changes across versions
│   └── license.pdf                    # Legal license agreement
│
├── test/                              # Tests and related files
│   ├── test-suite-1.spec.js           # Tests for module 1
│   ├── test-suite-2.spec.js           # Tests for module 2
│   └── coverage-report.html           # Code coverage summary
'''

# Create the directory structure
create_directory_structure(markdown_structure)
print("Directory structure created successfully!")
