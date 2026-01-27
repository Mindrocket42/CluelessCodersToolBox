import os
import fnmatch
import re
from pathlib import Path

def parse_gitignore(gitignore_path):
    """Parse a .gitignore file and return a list of patterns."""
    if not os.path.exists(gitignore_path):
        return []
    
    patterns = []
    with open(gitignore_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            # Add the pattern
            patterns.append(line)
    return patterns

def is_excluded(path, root_folder, patterns):
    """Check if a path should be excluded based on gitignore patterns."""
    if not patterns:
        return False
    
    # Get the relative path from the root folder
    rel_path = os.path.relpath(path, root_folder)
    # Convert Windows backslashes to forward slashes for consistency
    rel_path = rel_path.replace('\\', '/')
    
    # Check if the path matches any of the patterns
    for pattern in patterns:
        # Handle negation patterns (those starting with !)
        if pattern.startswith('!'):
            # If the path matches a negation pattern, it should NOT be excluded
            if match_gitignore_pattern(rel_path, pattern[1:]):
                return False
        # Regular exclusion pattern
        elif match_gitignore_pattern(rel_path, pattern):
            return True
    
    return False

def match_gitignore_pattern(path, pattern):
    """Match a path against a gitignore pattern."""
    # Convert gitignore pattern to regex pattern
    
    # Handle directory-specific patterns (ending with /)
    dir_only = pattern.endswith('/')
    if dir_only:
        pattern = pattern[:-1]
    
    # Escape special regex characters but keep gitignore's special characters
    pattern = re.escape(pattern)
    
    # Convert gitignore's glob patterns to regex
    # * matches anything except /
    pattern = pattern.replace('\\*', '[^/]*')
    # ** matches anything including /
    pattern = pattern.replace('\\*\\*', '.*')
    # ? matches a single character
    pattern = pattern.replace('\\?', '.')
    
    # Handle patterns with directories
    if '/' in pattern:
        # If pattern has a leading slash, it matches from the root
        if pattern.startswith('/'):
            pattern = '^' + pattern[1:]
        # Otherwise, it can match anywhere in the path
        else:
            pattern = pattern
    else:
        # If no slashes, the pattern can match at any level
        pattern = '(^|/)' + pattern
    
    # If dir_only is True, ensure we're matching a directory
    if dir_only:
        pattern = pattern + '(/|$)'
    else:
        pattern = pattern + '$'
    
    return re.search(pattern, path) is not None

def save_folder_structure(root_folder, output_file, gitignore_path=None):
    """Traverse the directory and save the folder structure to a text file, excluding gitignored files."""
    # Parse gitignore if provided
    gitignore_patterns = []
    if gitignore_path and os.path.exists(gitignore_path):
        gitignore_patterns = parse_gitignore(gitignore_path)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        for folder_path, subfolders, filenames in os.walk(root_folder):
            # Check if the current folder should be excluded
            if is_excluded(folder_path, root_folder, gitignore_patterns):
                # Remove this folder from the list of subfolders to prevent further traversal
                subfolders[:] = []
                continue
            
            # Filter out excluded subfolders
            subfolders[:] = [subfolder for subfolder in subfolders 
                            if not is_excluded(os.path.join(folder_path, subfolder), 
                                              root_folder, gitignore_patterns)]
            
            # Filter out excluded files
            filenames = [filename for filename in filenames 
                        if not is_excluded(os.path.join(folder_path, filename), 
                                          root_folder, gitignore_patterns)]
            
            # Write the current folder to the output file
            indent_level = folder_path.replace(root_folder, '').count(os.sep)
            indent = '│   ' * indent_level  # Create tree structure indentation
            folder_name = os.path.basename(folder_path)
            
            # Don't print the root folder name if we're at the root
            if folder_path != root_folder:
                file.write(f"{indent}├── {folder_name}/\n")
            
            # Write the files in the current folder
            for filename in filenames:
                file.write(f"{indent}│   ├── {filename}\n")

def main():
    root_folder = input("Enter the root folder path: ").strip()
    
    if not os.path.exists(root_folder):
        print("Error: The specified folder does not exist.")
        return
    
    # Look for .gitignore in the root folder
    gitignore_path = os.path.join(root_folder, '.gitignore')
    if os.path.exists(gitignore_path):
        print(f"Found .gitignore file at: {gitignore_path}")
    else:
        print("No .gitignore file found in the root folder.")
        gitignore_path = input("Enter path to .gitignore file (or leave empty to proceed without it): ").strip()
        if gitignore_path and not os.path.exists(gitignore_path):
            print(f"Warning: The specified .gitignore file does not exist: {gitignore_path}")
            gitignore_path = None
    
    output_file = "folder_structure.txt"
    save_folder_structure(root_folder, output_file, gitignore_path)
    print(f"Folder structure saved to '{output_file}'")

if __name__ == "__main__":
    main()
