#!/usr/bin/env python3
"""
MobiLoud Markdown Word Counter

A robust tool to count words in markdown blog posts, designed to match Google Docs word counts 
as closely as possible. It correctly handles YAML front matter, metadata, lists, quotes, 
and headers while ignoring markdown syntax (links, formatting chars).

Usage:
    python word_counter.py <file_path> [--target WORD_COUNT] [--tolerance TOLERANCE]

Examples:
    python word_counter.py outputs/my-article.md
    python word_counter.py outputs/my-article.md --target 2000
"""

import re
import sys
import argparse
from pathlib import Path

def clean_markdown_content(content):
    """
    Cleaner that attempts to preserve all visible text while removing markdown formatting.
    """
    # 1. Remove YAML Front Matter ONLY if it's at the very start of the string
    # Matches --- at start, content, --- on new line.
    if content.startswith('---'):
        content = re.sub(r'\A---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # 2. Remove Custom Metadata Headers (Meta Title, etc.)
    # We remove the *keys* but keeping the *values* might be what the user wants?
    # Usually "Meta Title: Some Title" -> "Some Title" is visible content?
    # But often metadata lines are NOT part of the body text word count.
    # We will exclude them to be safe as "article body" count, 
    # BUT if the user is copy-pasting the WHOLE file into GDocs, GDocs counts them.
    # Given the user's discrepancy is likely the body, we'll strip known metadata keys lines entirely 
    # to be consistent with "blog post word count".
    # If the user wants raw file count, that's different. 
    # Let's assume the user wants the content count.
    content = re.sub(r'^(Meta Title|Meta Description|URL Slug):\s*.*$', '', content, flags=re.MULTILINE)

    # 3. Remove Code Blocks (skip content inside? usually code blocks count as words in GDocs)
    # GDocs logic: Counts words in code blocks. 
    # So we should validly Strip the fences ` ``` ` but KEEP the content inside.
    content = re.sub(r'^```\w*\s*$', '', content, flags=re.MULTILINE) # Remove opening fence
    content = re.sub(r'^```\s*$', '', content, flags=re.MULTILINE)     # Remove closing fence
    content = re.sub(r'^~~~\w*\s*$', '', content, flags=re.MULTILINE) # Remove opening tildes
    content = re.sub(r'^~~~\s*$', '', content, flags=re.MULTILINE)     # Remove closing tildes

    # 4. Remove Links but KEEP Anchor Text
    # [text](url) -> text
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)

    # 5. Remove Images (Alt text is technically content? Usually not counted in body)
    # ![alt](url) -> remove entire thing or keep alt? 
    # Standard practice: remove images.
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)

    # 6. Remove HTML Tags (but keep content?)
    # <br>, <div>, etc.
    content = re.sub(r'<[^>]+>', '', content)

    # 7. Remove Header Markers (#)
    content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)

    # 8. Remove Bullet/List Markers
    content = re.sub(r'^[\*\-\+]\s+', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\d+\.\s+', '', content, flags=re.MULTILINE)

    # 9. Remove Blockquote Markers (>)
    content = re.sub(r'^>\s+', '', content, flags=re.MULTILINE)

    # 10. Remove Horizontal Rules
    content = re.sub(r'^---\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^___\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\*\*\*\s*$', '', content, flags=re.MULTILINE)

    # 11. Remove Bold/Italic wrappers (*, _)
    # We just remove all * and _ that are surrounding text.
    # Easier: remove all * and _ characters.
    content = re.sub(r'[*_]', '', content)

    # 12. Remove Reference-style link definitions
    # [id]: url "title"
    content = re.sub(r'^\[.+?\]:\s*.*$', '', content, flags=re.MULTILINE)

    return content

def count_words(content):
    """
    Count words using a simple whitespace splitter, filtering empty strings.
    This effectively matches Google Docs "Text -> Word count".
    """
    # Replace newlines/tabs with space
    content = content.replace('\n', ' ').replace('\t', ' ')
    # Split by whitespace
    words = [w for w in content.split(' ') if w.strip()]
    return len(words)

def check_word_count(file_path, target=None, tolerance=200):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        sys.exit(1)

    cleaned_content = clean_markdown_content(raw_content)
    word_count = count_words(cleaned_content)
    
    result = {
        'file': file_path,
        'word_count': word_count,
        'target': target,
        'tolerance': tolerance,
        'pass': True
    }

    if target is not None:
        min_acc = target - tolerance
        max_acc = target + tolerance
        result['min_acceptable'] = min_acc
        result['max_acceptable'] = max_acc
        result['deviation'] = word_count - target
        
        if not (min_acc <= word_count <= max_acc):
            result['pass'] = False
            
    return result

def format_result(result):
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"Word Count Report: {Path(result['file']).name}")
    output.append(f"{'='*60}")
    output.append(f"Word Count: {result['word_count']} words")
    
    if result['target'] is not None:
        pass_icon = "✅" if result['pass'] else "❌"
        output.append(f"Target: {result['target']} words (±{result['tolerance']})")
        output.append(f"Status: {pass_icon} {'PASS' if result['pass'] else 'FAIL'}")
        
        if not result['pass']:
            if result['word_count'] < result['min_acceptable']:
                output.append(f"   SHORTAGE: Needs ~{result['min_acceptable'] - result['word_count']} more words")
            else:
                output.append(f"   EXCESS: Needs ~{result['word_count'] - result['max_acceptable']} fewer words")
            
    output.append(f"{'='*60}\n")
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description='Count words in markdown file.')
    parser.add_argument('file', help='Path to markdown file')
    parser.add_argument('--target', type=int, help='Target word count')
    parser.add_argument('--tolerance', type=int, default=200, help='Tolerance (default: 200)')
    
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
        
    result = check_word_count(args.file, args.target, args.tolerance)
    print(format_result(result))
    
    if not result['pass']:
        sys.exit(1)

if __name__ == '__main__':
    main()
