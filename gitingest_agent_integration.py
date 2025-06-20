# gitingest_agent_integration.py
"""
GitIngest + Multi-Agent Integration
Combines GitIngest repository analysis with your local LLM agents
"""

import requests
import json
from pathlib import Path

class GitIngestAgent:
    def __init__(self, agent1_url="http://localhost:8001", agent2_url="http://localhost:8002"):
        self.agent1_url = agent1_url
        self.agent2_url = agent2_url
        self.gitingest_api = "https://gitingest.com/api/ingest"
    
    def ingest_repository(self, github_url: str, save_to_data=True):
        """
        1. Use GitIngest to analyze a GitHub repository
        2. Save the analysis to your data folder for RAG
        3. Create a report using your multi-agent system
        """
        
        print(f"🔍 Ingesting repository: {github_url}")
        
        # Step 1: Get repository analysis from GitIngest
        payload = {
            "url": github_url,
            "include_patterns": ["*.py", "*.md", "*.txt", "*.yml", "*.json"],
            "exclude_patterns": ["*.pyc", "__pycache__/*", "node_modules/*", ".git/*"]
        }
        
        try:
            response = requests.post(
                self.gitingest_api,
                json=payload,
                timeout=120
            )
            
            if response.status_code != 200:
                print(f"❌ GitIngest error: {response.status_code}")
                return None
                
            analysis = response.json()
            print("✅ Repository analysis complete")
            
            # Step 2: Save to data folder for your RAG system
            if save_to_data:
                self.save_to_rag_data(analysis, github_url)
            
            # Step 3: Generate report using your agents
            report = self.create_code_analysis_report(analysis, github_url)
            
            return {
                "analysis": analysis,
                "report": report,
                "github_url": github_url
            }
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def save_to_rag_data(self, analysis: dict, github_url: str):
        """Save GitIngest analysis to your data folder for RAG queries"""
        
        # Create filename from repo URL
        repo_name = github_url.split("/")[-1].replace(".git", "")
        filename = f"data/gitingest_{repo_name}.txt"
        
        # Format for RAG consumption
        content = f"GitHub Repository Analysis: {github_url}\n"
        content += "=" * 60 + "\n\n"
        
        if "summary" in analysis:
            summary = analysis["summary"]
            content += f"Repository Summary:\n"
            content += f"- Total files: {summary.get('total_files', 'N/A')}\n"
            content += f"- Languages: {', '.join(summary.get('languages', []))}\n"
            content += f"- Total lines: {summary.get('total_lines', 'N/A')}\n\n"
        
        if "tree" in analysis:
            content += f"Project Structure:\n{analysis['tree']}\n\n"
        
        if "files" in analysis:
            content += "Key Files and Content:\n\n"
            for filepath, file_content in analysis["files"].items():
                content += f"File: {filepath}\n"
                content += "-" * 40 + "\n"
                content += file_content + "\n\n"
        
        # Save to data folder
        try:
            Path("data").mkdir(exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"💾 Saved to RAG data: {filename}")
        except Exception as e:
            print(f"❌ Error saving to data folder: {e}")
    
    def create_code_analysis_report(self, analysis: dict, github_url: str):
        """Use Agent2 to create a comprehensive code analysis report"""
        
        print("🤖 Creating analysis report with Agent2...")
        
        # Prepare questions for Agent2 to research
        questions = [
            f"What is the purpose and main functionality of the repository {github_url}?",
            "What are the key technologies and frameworks used in this project?",
            "What is the overall architecture and structure of this codebase?",
            "What are the main components and how do they interact?",
            "What are the key files and their purposes?"
        ]
        
        report_request = {
            "topic": f"Code Analysis Report: {github_url}",
            "questions": questions,
            "report_style": "detailed"
        }
        
        try:
            response = requests.post(
                f"{self.agent2_url}/create_report",
                json=report_request,
                timeout=300  # 5 minutes for detailed analysis
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Analysis report generated")
                
                # Save report
                repo_name = github_url.split("/")[-1]
                report_filename = f"analysis_report_{repo_name}.md"
                
                with open(report_filename, 'w', encoding='utf-8') as f:
                    f.write(f"# Code Analysis Report\n\n")
                    f.write(f"**Repository:** {github_url}\n")
                    f.write(f"**Generated:** {result.get('timestamp', 'N/A')}\n\n")
                    f.write(result["report"])
                    
                    f.write(f"\n\n## Research Sources\n")
                    for i, research in enumerate(result["research_used"], 1):
                        f.write(f"{i}. {research['question']}\n")
                
                print(f"📝 Report saved: {report_filename}")
                return result["report"]
                
            else:
                print(f"❌ Agent2 error: {response.status_code}")
                return "Error generating report"
                
        except Exception as e:
            print(f"❌ Error creating report: {e}")
            return f"Error: {e}"

def demo_workflow():
    """Demonstrate the complete GitIngest + Multi-Agent workflow"""
    
    print("🚀 GITINGEST + MULTI-AGENT DEMO")
    print("=" * 50)
    print()
    
    # Initialize the integration
    agent = GitIngestAgent()
    
    # Example repositories
    repos = [
        "https://github.com/fastapi/fastapi",
        "https://github.com/streamlit/streamlit", 
        "https://github.com/pydantic/pydantic",
        "https://github.com/pallets/flask"
    ]
    
    print("Available repositories to analyze:")
    for i, repo in enumerate(repos, 1):
        print(f"{i}. {repo}")
    print()
    
    try:
        choice = input("Choose a repository (1-4) or enter a custom GitHub URL: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(repos):
            repo_url = repos[int(choice) - 1]
        elif choice.startswith("https://github.com"):
            repo_url = choice
        else:
            repo_url = repos[0]  # Default
        
        print(f"\n🔄 Processing: {repo_url}")
        print("This will:")
        print("1. Analyze the repository with GitIngest")
        print("2. Save analysis to your RAG data folder")
        print("3. Generate a detailed report using your agents")
        print("4. You can then query the repository using your RAG system")
        print()
        
        # Run the complete workflow
        result = agent.ingest_repository(repo_url)
        
        if result:
            print("\n✅ WORKFLOW COMPLETE!")
            print("=" * 30)
            print("What you can do now:")
            print("1. Ask questions about this repository using rag_file_loader.py")
            print("2. Review the generated analysis report")
            print("3. The repository data is now in your local knowledge base")
            
    except KeyboardInterrupt:
        print("\nDemo cancelled.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    demo_workflow()
