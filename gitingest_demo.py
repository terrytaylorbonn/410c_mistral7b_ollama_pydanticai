# gitingest_demo.py
"""
GitIngest Getting Started Demo
https://gitingest.com/

GitIngest creates summaries of GitHub repositories that are perfect for:
- Code analysis with AI/LLMs
- Understanding project structure
- Getting quick repository overviews
- Preparing context for development tasks
"""

import requests
import json
import time
from urllib.parse import urlparse
import os

class GitIngestDemo:
    def __init__(self):
        self.base_url = "https://gitingest.com"
        self.api_url = f"{self.base_url}/api/ingest"
        
    def analyze_repo(self, github_url: str, include_patterns: list = None, exclude_patterns: list = None):
        """
        Analyze a GitHub repository using GitIngest
        
        Args:
            github_url: GitHub repository URL
            include_patterns: List of file patterns to include (e.g., ['*.py', '*.md'])
            exclude_patterns: List of file patterns to exclude (e.g., ['*.pyc', 'node_modules/*'])
        """
        
        print(f"Analyzing repository: {github_url}")
        print("-" * 50)
        
        # Prepare request payload
        payload = {
            "url": github_url,
            "include_patterns": include_patterns or [],
            "exclude_patterns": exclude_patterns or []
        }
        
        try:
            # Make request to GitIngest API
            response = requests.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                self.display_results(result, github_url)
                return result
            else:
                print(f"Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error analyzing repository: {e}")
            return None
    
    def display_results(self, result: dict, github_url: str):
        """Display the analysis results in a readable format"""
        
        print("📊 REPOSITORY ANALYSIS COMPLETE")
        print("=" * 50)
        
        # Basic info
        if "summary" in result:
            summary = result["summary"]
            print(f"Repository: {github_url}")
            print(f"Files analyzed: {summary.get('total_files', 'N/A')}")
            print(f"Total lines: {summary.get('total_lines', 'N/A')}")
            print(f"Languages: {', '.join(summary.get('languages', []))}")
            print()
        
        # File structure
        if "tree" in result:
            print("📁 PROJECT STRUCTURE:")
            print(result["tree"])
            print()
        
        # Key files
        if "files" in result:
            print("📄 KEY FILES CONTENT:")
            files = result["files"]
            for file_path, content in files.items():
                print(f"\n--- {file_path} ---")
                # Show first 500 characters
                preview = content[:500]
                if len(content) > 500:
                    preview += "... (truncated)"
                print(preview)
                print()
        
        # Save full results
        self.save_results(result, github_url)
    
    def save_results(self, result: dict, github_url: str):
        """Save results to a local file"""
        
        # Create filename from repo URL
        parsed = urlparse(github_url)
        repo_name = parsed.path.strip('/').replace('/', '_')
        filename = f"gitingest_{repo_name}_{int(time.time())}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"💾 Full results saved to: {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def create_ai_prompt(self, result: dict, task: str = "analyze this codebase"):
        """Create a prompt suitable for AI analysis"""
        
        prompt = f"""Please {task} based on the following repository analysis:

REPOSITORY SUMMARY:
"""
        
        if "summary" in result:
            summary = result["summary"]
            prompt += f"- Total files: {summary.get('total_files', 'N/A')}\n"
            prompt += f"- Languages: {', '.join(summary.get('languages', []))}\n"
            prompt += f"- Total lines: {summary.get('total_lines', 'N/A')}\n\n"
        
        if "tree" in result:
            prompt += f"PROJECT STRUCTURE:\n{result['tree']}\n\n"
        
        if "files" in result:
            prompt += "KEY FILES CONTENT:\n"
            for file_path, content in result["files"].items():
                prompt += f"\n--- {file_path} ---\n"
                prompt += content + "\n"
        
        # Save prompt to file
        prompt_filename = f"ai_prompt_{int(time.time())}.txt"
        try:
            with open(prompt_filename, 'w', encoding='utf-8') as f:
                f.write(prompt)
            print(f"🤖 AI prompt saved to: {prompt_filename}")
        except Exception as e:
            print(f"Error saving prompt: {e}")
        
        return prompt

def demo_examples():
    """Run some example analyses"""
    
    demo = GitIngestDemo()
    
    print("🚀 GITINGEST DEMO - GETTING STARTED")
    print("=" * 60)
    print()
    
    # Example repositories to analyze
    examples = [
        {
            "name": "Simple Python Project",
            "url": "https://github.com/psf/requests",
            "include": ["*.py", "*.md", "*.txt"],
            "exclude": ["*.pyc", "__pycache__/*", "tests/*"]
        },
        {
            "name": "JavaScript Library",
            "url": "https://github.com/lodash/lodash",
            "include": ["*.js", "*.json", "*.md"],
            "exclude": ["node_modules/*", "*.min.js", "test/*"]
        },
        {
            "name": "Documentation Project",
            "url": "https://github.com/microsoft/vscode-docs",
            "include": ["*.md", "*.json"],
            "exclude": ["node_modules/*", ".git/*"]
        }
    ]
    
    print("Available examples:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['name']} - {example['url']}")
    print()
    
    # Interactive selection
    try:
        choice = input("Choose an example (1-3) or enter a custom GitHub URL: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(examples):
            example = examples[int(choice) - 1]
            print(f"\nAnalyzing: {example['name']}")
            result = demo.analyze_repo(
                example["url"],
                include_patterns=example["include"],
                exclude_patterns=example["exclude"]
            )
        elif choice.startswith("https://github.com"):
            print(f"\nAnalyzing custom repository: {choice}")
            result = demo.analyze_repo(choice)
        else:
            print("Invalid choice. Using default example...")
            example = examples[0]
            result = demo.analyze_repo(
                example["url"],
                include_patterns=example["include"],
                exclude_patterns=example["exclude"]
            )
        
        # Create AI-ready prompt
        if result:
            print("\n" + "=" * 50)
            task = input("What would you like to analyze about this codebase? (press Enter for general analysis): ").strip()
            if not task:
                task = "provide a comprehensive analysis of this codebase including its purpose, architecture, and key components"
            
            demo.create_ai_prompt(result, task)
            
    except KeyboardInterrupt:
        print("\nDemo cancelled.")
    except Exception as e:
        print(f"Error during demo: {e}")

def quick_analysis(repo_url: str):
    """Quick analysis function"""
    demo = GitIngestDemo()
    return demo.analyze_repo(repo_url)

if __name__ == "__main__":
    # Run the interactive demo
    demo_examples()
