import os
import glob
import json
from pathlib import Path
from typing import Dict, List, Any
import git
from collections import defaultdict
from fnmatch import fnmatch
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RepoAnalyzer:

    EXCLUDED_EXTENSIONS = {
        # Binary/Compiled
        '.pyc', '.pyo', '.pyd', '.so', '.dll', '.class', '.bin', '.exe',
        
        # Media
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', 
        '.mp3', '.mp4', '.wav', '.avi', '.mov', '.wmv',
        
        # Documents
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        
        # Archives
        '.zip', '.tar', '.gz', '.rar', '.7z',
        
        # Database and Data
        '.db', '.sqlite', '.pkl', '.model', '.h5', '.dat',
        
        # Other
        '.ico', '.ttf', '.eot', '.woff', '.woff2',
        '.log', '.cache', '.DS_Store', '.env'
    }

    EXCLUDED_DIRECTORIES = {
        'node_modules',
        'venv',
        '.git',
        '.idea',
        '__pycache__',
        'build',
        'dist',
        '.pytest_cache',
        '.vscode',
        'coverage',
        'Repo-Analyzer-Output'
    }
    
    def __init__(self, repo_path: str):
        """Initialize the repository analyzer."""
        self.repo_path = Path(repo_path)
        self.output_path = self.repo_path / '.Repo-Analyzer-Output'  # Save directly in the repo path
        
        # Ensure the output directory exists
        if not self.output_path.exists():
            self.output_path.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
        
        self.file_structure = defaultdict(dict)
        self.metadata = {}
        self.gitignore_patterns = self._parse_gitignore()

    def _parse_gitignore(self) -> List[str]:
        """Parse .gitignore file and return patterns."""
        gitignore_path = self.repo_path / '.gitignore'
        patterns = []
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r') as f:
                    patterns = [line.strip() for line in f 
                              if line.strip() and not line.startswith('#')]
            except Exception as e:
                logger.warning(f"Error reading .gitignore: {e}")
        return patterns

    def _is_binary_file(self, file_path: Path) -> bool:
        """Check if file is binary."""
        try:
            with open(file_path, 'tr') as check_file:
                check_file.read(1024)
                return False
        except UnicodeDecodeError:
            return True

    def _should_process_file(self, file_path: Path) -> bool:
        """Determine if a file should be processed based on filters."""
        try:
            # Check file extension first
            if file_path.suffix.lower() in self.EXCLUDED_EXTENSIONS:
                logger.info(f"Skipping file {file_path} due to excluded extension: {file_path.suffix}")
                return False

            # Check directory path for exclusions
            if any(excluded in file_path.parts for excluded in self.EXCLUDED_DIRECTORIES):
                logger.info(f"Skipping file {file_path} due to excluded directory")
                return False

            logger.info(f"Including file {file_path} for processing")
            return True
        except Exception as e:
            logger.error(f"Error in _should_process_file: {e}")
            return False




    def clone_repo(self, repo_url: str) -> None:
        """Clone a repository if URL is provided."""
        try:
            if not self.repo_path.exists():
                git.Repo.clone_from(repo_url, self.repo_path)
                logger.info(f"Successfully cloned repository from {repo_url}")
        except Exception as e:
            logger.error(f"Error cloning repository: {e}")
            raise

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze individual file content and metadata."""
        try:
            # Check if file is binary
            if self._is_binary_file(file_path):
                return {
                    'path': str(file_path.relative_to(self.repo_path)),
                    'size': os.path.getsize(file_path),
                    'extension': file_path.suffix,
                    'type': 'binary',
                    'last_modified': os.path.getmtime(file_path)
                }

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Scrub links or embeds to excluded file types
            content = self._scrub_excluded_links(content)

            return {
                'path': str(file_path.relative_to(self.repo_path)),
                'size': os.path.getsize(file_path),
                'extension': file_path.suffix,
                'content': content,
                'imports': self._extract_imports(content, file_path.suffix),
                'last_modified': os.path.getmtime(file_path),
                'type': 'text'
            }
        except UnicodeDecodeError:
            return {
                'path': str(file_path.relative_to(self.repo_path)),
                'error': 'File encoding not supported',
                'type': 'binary'
            }
        except Exception as e:
            return {
                'path': str(file_path.relative_to(self.repo_path)),
                'error': str(e)
            }

    def _extract_imports(self, content: str, extension: str) -> List[str]:
        """Extract import statements based on file type."""
        imports = []
        try:
            if extension == '.py':
                for line in content.split('\n'):
                    if line.strip().startswith(('import ', 'from ')):
                        imports.append(line.strip())
        except Exception as e:
            logger.warning(f"Error extracting imports: {e}")
        return imports

    def _scrub_excluded_links(self, content: str) -> str:
        """Remove links or embeds to excluded file types from content."""
        for ext in self.EXCLUDED_EXTENSIONS:
            content = content.replace(f'http://example.com/file{ext}', '')  # Example link format
            content = content.replace(f'https://example.com/file{ext}', '')  # Example link format
        return content

    def process_repository(self) -> None:
        """Process the entire repository with filtering."""
        try:
            self.output_path.mkdir(exist_ok=True)
            
            # Count total files first
            total_files = sum(1 for _ in self.repo_path.rglob('*') if _.is_file())
            processed = 0
            skipped_files = defaultdict(list)
            
            logger.info(f"Found {total_files} files to process...")
            
            for file_path in self.repo_path.rglob('*'):
                if file_path.is_file():
                    logger.info(f"Checking file: {file_path}")
                    processed += 1
                    
                    if processed % 100 == 0:
                        logger.info(f"Processed {processed}/{total_files} files...")
                    
                    # Check if the file should be processed
                    if not self._should_process_file(file_path):
                        reason = "Extension excluded" if file_path.suffix in self.EXCLUDED_EXTENSIONS else \
                                "Directory excluded" if any(excluded in file_path.parts for excluded in self.EXCLUDED_DIRECTORIES) else \
                                "Gitignore pattern match"
                        skipped_files[reason].append(str(file_path.relative_to(self.repo_path)))
                        continue
                    
                    # Get relative path to use in file_structure
                    relative_path = file_path.relative_to(self.repo_path)
                    
                    # Process the file if it should be included
                    self.file_structure[str(relative_path.parent)][relative_path.name] = self.analyze_file(file_path)

            # Update metadata
            self.metadata = {
                'total_files': sum(len(files) for files in self.file_structure.values()),
                'directory_structure': self._get_directory_structure(),
                'file_types': self._get_file_types(),
                'skipped_files': dict(skipped_files),
                'processing_summary': {
                    'processed_files': self.metadata.get('total_files', 0),
                    'skipped_files': sum(len(files) for files in skipped_files.values())
                }
            }
            
            logger.info("Repository processing complete.")
            
        except Exception as e:
            logger.error(f"Error processing repository: {e}")
            raise


    def _get_directory_structure(self) -> Dict[str, List[str]]:
        """Generate directory structure representation."""
        return {dir_path: list(files.keys()) 
                for dir_path, files in self.file_structure.items()}

    def _get_file_types(self) -> Dict[str, int]:
        """Count file types in repository."""
        extensions = defaultdict(int)
        for files in self.file_structure.values():
            for file_info in files.values():
                if 'extension' in file_info:
                    extensions[file_info['extension']] += 1
        return dict(extensions)

    def export_analysis(self) -> None:
        """Export the analysis results with a timestamped filename."""
        try:
            output = {
                'metadata': self.metadata,
                'file_structure': dict(self.file_structure)
            }
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_path / f'analysis_{timestamp}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2)
            
            logger.info(f"Analysis exported to {output_file}")
            
        except Exception as e:
            logger.error(f"Error exporting analysis: {e}")
            raise

def main():
    try:
        # Example usage
        repo_url = input("Enter repository URL (or press Enter for local path): ").strip()
        repo_path = input("Enter local repository path: ").strip()
        
        analyzer = RepoAnalyzer(repo_path)  # No output_path parameter needed
        
        if repo_url:
            analyzer.clone_repo(repo_url)
        
        logger.info("Processing repository...")
        analyzer.process_repository()
        analyzer.export_analysis()
        logger.info(f"Analysis complete. Results saved to {analyzer.output_path}/analysis.json")  # Updated log message
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main()
