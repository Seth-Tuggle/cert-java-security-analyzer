"""
Java Code Security Analyzer using CERT Standards
This script analyzes Java code for CERT coding standard violations
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_knowledge_base():
    """Load the CERT standards knowledge base"""
    try:
        with open('cert_knowledge_base.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: cert_knowledge_base.json not found!")
        print("Please run 'setup_rag_system.py' first to create the knowledge base")
        return None

def create_context_from_knowledge_base(kb):
    """Create a condensed context string from knowledge base"""
    context = "CERT Java Secure Coding Standards:\n\n"
    for standard in kb:
        context += f"Standard {standard['id']}: {standard['description']}\n"
        context += f"URL: {standard['url']}\n"
        # Include key portions of content (truncated for token efficiency)
        content_preview = standard['content'][:2000] if len(standard['content']) > 2000 else standard['content']
        context += f"Details: {content_preview}\n\n"
    return context

def analyze_java_code(java_code, knowledge_base):
    """Analyze Java code for CERT standard violations"""
    
    # Create context from knowledge base
    context = create_context_from_knowledge_base(knowledge_base)
    
    # Create the prompt for GPT-4o-mini
    system_prompt = """You are an expert Java security analyzer specializing in CERT Secure Coding Standards. 
Your task is to analyze Java code and identify any violations of CERT coding standards.

For each violation found:
1. Identify the specific CERT standard ID (e.g., IDS01-J, ERR00-J)
2. Explain what the violation is
3. Show the problematic code snippet
4. Provide detailed remediation steps with corrected code examples

Be thorough and specific in your analysis."""

    user_prompt = f"""Using the following CERT Java Secure Coding Standards as reference:

{context}

Please analyze this Java code for security violations:

```java
{java_code}
```

Provide a detailed report that includes:
1. List of all CERT standard violations found
2. For each violation:
   - Standard ID and name
   - Explanation of the violation
   - The problematic code
   - Detailed remediation steps
   - Corrected code example
3. If no violations found, state that the code appears compliant

Format your response clearly with headers and code blocks."""

    try:
        print("Analyzing code with GPT-4o-mini...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error during analysis: {str(e)}"

def main():
    print("CERT Java Code Security Analyzer")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("ERROR: OPENAI_API_KEY not found in .env file")
        return
    
    # Load knowledge base
    print("\nLoading CERT standards knowledge base...")
    knowledge_base = load_knowledge_base()
    if not knowledge_base:
        return
    
    print(f"Loaded {len(knowledge_base)} CERT standards")
    
    # Input options
    print("\n" + "=" * 50)
    print("Choose input method:")
    print("1. Enter Java code directly")
    print("2. Load from file")
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    java_code = ""
    
    if choice == "1":
        print("\nEnter your Java code (type 'END' on a new line when done):")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        java_code = "\n".join(lines)
    
    elif choice == "2":
        filename = input("\nEnter Java file path: ").strip()
        try:
            with open(filename, 'r') as f:
                java_code = f.read()
        except FileNotFoundError:
            print(f"ERROR: File '{filename}' not found")
            return
    else:
        print("Invalid choice")
        return
    
    if not java_code.strip():
        print("ERROR: No code provided")
        return
    
    # Analyze the code
    print("\n" + "=" * 50)
    print("ANALYSIS RESULTS")
    print("=" * 50 + "\n")
    
    result = analyze_java_code(java_code, knowledge_base)
    print(result)
    
    # Option to save results
    save = input("\n\nSave results to file? (y/n): ").strip().lower()
    if save == 'y':
        output_file = input("Enter output filename (default: analysis_report.txt): ").strip()
        if not output_file:
            output_file = "analysis_report.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("CERT Java Code Security Analysis Report\n")
            f.write("=" * 50 + "\n\n")
            f.write("Analyzed Code:\n")
            f.write("-" * 50 + "\n")
            f.write(java_code)
            f.write("\n\n" + "=" * 50 + "\n\n")
            f.write("Analysis Results:\n")
            f.write("-" * 50 + "\n")
            f.write(result)
        
        print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()