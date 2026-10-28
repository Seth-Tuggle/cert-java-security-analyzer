"""
Setup RAG System for CERT Java Coding Standards
This script fetches CERT coding standards and creates a vector database
"""

import os
import requests
from bs4 import BeautifulSoup
import json
from openai import OpenAI
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def extract_standards_from_file(filename):
    """Extract standard IDs and URLs from the text file"""
    standards = []
    with open(filename, 'r') as f:
        content = f.read()
        # Pattern to match: number. STANDARD_ID - url
        pattern = r'\d+\.\s+([A-Z0-9-]+)\.\s+(.+?)\s+-\s+(https?://[^\s]+)'
        matches = re.findall(pattern, content)
        
        for match in matches:
            standard_id = match[0]
            description = match[1].strip()
            url = match[2].strip()
            standards.append({
                'id': standard_id,
                'description': description,
                'url': url
            })
    return standards

def fetch_standard_content(url):
    """Fetch and parse content from CERT wiki page"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract main content
        main_content = soup.find('div', {'id': 'main-content'})
        if not main_content:
            main_content = soup.find('div', {'class': 'wiki-content'})
        
        if main_content:
            # Remove script and style elements
            for script in main_content(['script', 'style']):
                script.decompose()
            
            text = main_content.get_text(separator='\n', strip=True)
            return text
        return None
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None

def create_embeddings_and_store(standards_data):
    """Create embeddings for standards and store them"""
    knowledge_base = []
    
    for standard in standards_data:
        print(f"Processing {standard['id']}...")
        
        content = fetch_standard_content(standard['url'])
        if content:
            # Create a comprehensive text for embedding
            full_text = f"""
Standard: {standard['id']}
Title: {standard['description']}
URL: {standard['url']}

Content:
{content}
"""
            knowledge_base.append({
                'id': standard['id'],
                'description': standard['description'],
                'url': standard['url'],
                'content': content,
                'full_text': full_text
            })
        else:
            print(f"Failed to fetch content for {standard['id']}")
    
    # Save the knowledge base
    with open('cert_knowledge_base.json', 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
    
    print(f"\nSuccessfully processed {len(knowledge_base)} standards")
    print("Knowledge base saved to 'cert_knowledge_base.json'")
    
    return knowledge_base

def main():
    print("CERT Java Coding Standards RAG System Setup")
    print("=" * 50)
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("ERROR: OPENAI_API_KEY not found in .env file")
        return
    
    # Extract standards from file
    print("\n1. Extracting standards from CodingRules.txt...")
    standards = extract_standards_from_file('CodingRules.txt')
    print(f"Found {len(standards)} standards")
    
    # Fetch content and create knowledge base
    print("\n2. Fetching content from CERT wiki pages...")
    knowledge_base = create_embeddings_and_store(standards)
    
    print("\n3. Setup complete!")
    print(f"Knowledge base contains {len(knowledge_base)} standards")
    print("\nYou can now run '2_analyze_java_code.py' to analyze Java code")

if __name__ == "__main__":
    main()