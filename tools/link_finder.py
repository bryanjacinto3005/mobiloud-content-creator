import argparse
import sys
import re
import json

def parse_markdown_directory(file_path):
    """
    Parses the blog_link_directory.md file.
    Expected format:
    - [Title](URL)
      - **Summary:** Summary text...
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = []
    # logic to parse blocks. 
    # We can split by lines and look for patterns.
    lines = content.split('\n')
    
    current_entry = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Match link line: - [Title](URL)
        link_match = re.search(r'^\-\s+\[(.*?)\]\((.*?)\)$', line)
        if link_match:
            # Save previous entry if exists and valid
            if current_entry.get('title') and current_entry.get('url'):
                entries.append(current_entry)
            
            current_entry = {
                'title': link_match.group(1),
                'url': link_match.group(2),
                'summary': ''
            }
            continue
            
        # Match summary line: - **Summary:** ...
        summary_match = re.search(r'^\-\s+\*\*Summary:\*\*\s+(.*)', line)
        if summary_match and current_entry:
            current_entry['summary'] = summary_match.group(1)
            
    # Add last entry
    if current_entry.get('title') and current_entry.get('url'):
        entries.append(current_entry)
        
    return entries

def score_entry(entry, query_terms):
    """
    Scores an entry based on keyword matches in title and summary.
    """
    text = (entry['title'] + " " + entry['summary']).lower()
    score = 0
    for term in query_terms:
        if term in text:
            score += 1
            # Bonus for title match
            if term in entry['title'].lower():
                score += 2
    return score

def main():
    parser = argparse.ArgumentParser(description='Find relevant internal links from the directory.')
    parser.add_argument('query', help='The search query string (e.g. topic or keywords)')
    parser.add_argument('--limit', type=int, default=5, help='Number of results to return')
    parser.add_argument('--path', default='directories/blog_link_directory.md', help='Path to the directory file')
    
    args = parser.parse_args()
    
    try:
        entries = parse_markdown_directory(args.path)
    except FileNotFoundError:
        print(f"Error: File not found at {args.path}. Please check the path.", file=sys.stderr)
        sys.exit(1)

    query_terms = [t.lower() for t in args.query.split() if len(t) > 3] # Filter short words
    
    if not query_terms:
         # dynamic fallback if query is too short/generic
         query_terms = [t.lower() for t in args.query.split()]

    scored_entries = []
    for entry in entries:
        score = score_entry(entry, query_terms)
        if score > 0:
            scored_entries.append((score, entry))
            
    # Sort by score desc, then alphabetical title
    scored_entries.sort(key=lambda x: (-x[0], x[1]['title']))
    
    top_entries = [x[1] for x in scored_entries[:args.limit]]
    
    print(json.dumps(top_entries, indent=2))

if __name__ == "__main__":
    main()
