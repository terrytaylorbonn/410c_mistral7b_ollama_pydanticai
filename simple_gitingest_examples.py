# simple_gitingest_examples.py
"""
Simple GitIngest Examples - Quick Start Guide
"""

import requests
import json

def basic_usage():
    """Most basic GitIngest usage"""
    
    # 1. Simply paste a GitHub URL into GitIngest web interface
    print("METHOD 1: Web Interface (Easiest)")
    print("1. Go to https://gitingest.com/")
    print("2. Paste your GitHub repo URL")
    print("3. Click 'Ingest Repository'")
    print("4. Copy the generated summary")
    print()
    
    # 2. Direct URL method
    print("METHOD 2: Direct URL (Quick)")
    github_url = "https://github.com/python/cpython"
    gitingest_url = f"https://gitingest.com/api/ingest?url={github_url}"
    print(f"Direct link: {gitingest_url}")
    print()
    
    # 3. API method (programmatic)
    print("METHOD 3: API Call (Programmatic)")
    api_example()

def api_example():
    """Example API usage - Fixed for actual GitIngest API"""
    
    # Try a smaller repository first
    repo_url = "https://github.com/octocat/Hello-World"
    
    print(f"Testing with: {repo_url}")
    
    # Correct API format based on error response
    payload = {
        "input_text": repo_url,  # Changed from "url" to "input_text"
        "max_file_size": 32768,  # 32KB max file size
        "pattern_type": "include",  # or "exclude"
        "pattern": "*.py,*.md,*.txt,*.json"  # Comma-separated patterns
    }
    
    try:
        response = requests.post(
            "https://gitingest.com/api/ingest",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Successfully analyzed: {repo_url}")
            
            # GitIngest returns plain text, not JSON structure
            if isinstance(result, str):
                content = result
            elif isinstance(result, dict) and "content" in result:
                content = result["content"]
            else:
                content = str(result)
            
            print(f"Content length: {len(content)} characters")
            
            # Save to file for AI analysis
            with open("repo_analysis.txt", "w", encoding='utf-8') as f:
                f.write(f"Repository Analysis: {repo_url}\n")
                f.write("=" * 50 + "\n\n")
                f.write(content)
            
            print("📝 Analysis saved to 'repo_analysis.txt'")
            print("🤖 Ready to paste into AI chat!")
            
            # Show preview
            print(f"\nPreview (first 300 chars):")
            print("-" * 30)
            print(content[:300] + "..." if len(content) > 300 else content)
            
        elif response.status_code == 422:
            print(f"❌ Validation Error (422)")
            try:
                error_details = response.json()
                print(f"Error details: {json.dumps(error_details, indent=2)}")
            except:
                print(f"Error text: {response.text}")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Always show the web alternative
    print(f"\n💡 Web Interface Alternative:")
    print(f"   https://gitingest.com/")
    print(f"   Just paste: {repo_url}")

def use_with_local_llm():
    """Example: Using GitIngest output with your local Ollama setup"""
    
    print("USING GITINGEST WITH YOUR LOCAL LLM:")
    print("1. Run GitIngest on a repository")
    print("2. Save the output to a text file")
    print("3. Use it as context for your local Mistral/Phi3 model")
    print()
    
    # Example prompt template
    prompt_template = """
Analyze this repository and tell me:
1. What does this project do?
2. What are the main components?
3. How is it structured?
4. What technologies does it use?

Repository Analysis:
{gitingest_output}

Please provide a comprehensive analysis:
"""
    
    print("Example prompt template:")
    print(prompt_template)

def common_patterns():
    """Show common include/exclude patterns"""
    
    patterns = {
        "Python Projects": {
            "include": ["*.py", "*.md", "*.txt", "*.yml", "*.yaml", "requirements.txt"],
            "exclude": ["*.pyc", "__pycache__/*", ".git/*", "venv/*", ".env"]
        },
        "JavaScript/Node.js": {
            "include": ["*.js", "*.ts", "*.json", "*.md", "*.jsx", "*.tsx"],
            "exclude": ["node_modules/*", "*.min.js", "dist/*", ".git/*"]
        },
        "Documentation Only": {
            "include": ["*.md", "*.rst", "*.txt"],
            "exclude": [".git/*", "node_modules/*"]
        },
        "Configuration Files": {
            "include": ["*.yml", "*.yaml", "*.json", "*.toml", "*.ini", "*.conf"],
            "exclude": [".git/*", "*.log"]
        }
    }
    
    print("COMMON FILTER PATTERNS:")
    print("=" * 30)
    
    for project_type, filters in patterns.items():
        print(f"\n{project_type}:")
        print(f"  Include: {filters['include']}")
        print(f"  Exclude: {filters['exclude']}")

if __name__ == "__main__":
    print("🔍 GITINGEST QUICK START GUIDE")
    print("=" * 40)
    print()
    
    basic_usage()
    print()
    
    print("Running API example...")
    api_example()
    print()
    
    use_with_local_llm()
    print()
    
    common_patterns()
