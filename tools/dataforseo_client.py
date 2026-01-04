import os
import requests
import json
import base64
import hashlib
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from pathlib import Path

# Try to load from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- Configuration ---
DATAFORSEO_LOGIN = os.environ.get("DATAFORSEO_LOGIN")
DATAFORSEO_PASSWORD = os.environ.get("DATAFORSEO_PASSWORD")
BASE_URL = "https://api.dataforseo.com/v3"

# Cache directory for API responses
CACHE_DIR = Path(__file__).parent.parent / "outputs" / ".dataforseo_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_auth_header():
    if not DATAFORSEO_LOGIN or not DATAFORSEO_PASSWORD:
        raise ValueError("DataForSEO credentials not found. Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD environment variables.")
    credentials = f"{DATAFORSEO_LOGIN}:{DATAFORSEO_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}", "Content-Type": "application/json"}


def _make_request(endpoint: str, data: List[Dict]) -> Dict:
    """Helper to make POST requests to DataForSEO."""
    url = f"{BASE_URL}{endpoint}"
    headers = get_auth_header()
    response = None
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {endpoint}: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        return {"status_code": 500, "status_message": str(e)}


# =============================================================================
# CACHING UTILITIES
# =============================================================================

def _get_cache_key(endpoint: str, data: Dict) -> str:
    """Generate a cache key from endpoint and request data."""
    cache_str = f"{endpoint}_{json.dumps(data, sort_keys=True)}"
    return hashlib.md5(cache_str.encode()).hexdigest()


def _get_from_cache(cache_key: str, max_age_days: int = 30) -> Optional[Dict]:
    """Retrieve data from cache if it exists and isn't too old."""
    cache_file = CACHE_DIR / f"{cache_key}.json"
    
    if not cache_file.exists():
        return None
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            cached = json.load(f)
        
        # Check if cache is too old
        cached_time = datetime.fromisoformat(cached.get('cached_at', '2000-01-01'))
        if datetime.now() - cached_time > timedelta(days=max_age_days):
            return None
        
        return cached.get('data')
    except (json.JSONDecodeError, KeyError):
        return None


def _save_to_cache(cache_key: str, data: Dict):
    """Save API response to cache with timestamp."""
    cache_file = CACHE_DIR / f"{cache_key}.json"
    
    cached_data = {
        'cached_at': datetime.now().isoformat(),
        'data': data
    }
    
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cached_data, f, indent=2)


# =============================================================================
# DATAFORSEO LABS KEYWORD SUGGESTIONS
# =============================================================================

def get_keyword_suggestions(seed_keyword: str,
                           location_name: str = "United States",
                           language_name: str = "English",
                           limit: int = 30,
                           use_cache: bool = True) -> List[Dict]:
    """
    Get keyword suggestions using DataForSEO Labs endpoint.
    
    This is the primary function for keyword research. It returns long-tail
    keywords that contain your seed phrase, with search volume, CPC, competition, etc.
    
    Args:
        seed_keyword: The seed keyword/topic to expand
        location_name: Geographic location (default: "United States")
        language_name: Language (default: "English")
        limit: Max keywords to return (default: 30)
        use_cache: Use cached results if available (default: True)
        
    Returns:
        List of keyword dicts with: keyword, search_volume, cpc, competition, difficulty
    """
    endpoint = "/dataforseo_labs/google/keyword_suggestions/live"
    
    task = {
        "keyword": seed_keyword,
        "location_name": location_name,
        "language_name": language_name,
        "include_seed_keyword": True,
        "include_serp_info": False,
        "include_clickstream_data": False,
        "limit": limit,
        # Optional: ignore absolute-zero volume
        "filters": [["keyword_info.search_volume", ">", 0]]
    }
    
    # Check cache first
    if use_cache:
        cache_key = _get_cache_key(endpoint, task)
        cached_result = _get_from_cache(cache_key)
        if cached_result:
            print(f"  [OK] Using cached results for '{seed_keyword}'")
            return cached_result
    
    # Make API request
    response = _make_request(endpoint, [task])
    
    # Check for errors
    if response.get("status_code") != 20000:
        print(f"[ERROR] API Error: {response.get('status_message', 'Unknown error')}")
        return []
    
    # Extract items from response
    try:
        if "tasks" not in response or not response["tasks"]:
            print(f"[ERROR] No tasks in response")
            return []
            
        task_result = response["tasks"][0]
        if task_result.get("status_code") != 20000:
            print(f"[ERROR] Task error: {task_result.get('status_message', 'Unknown error')}")
            return []
        
        if "result" not in task_result or not task_result["result"]:
            print(f"[ERROR] No result in task")
            return []
            
        items = task_result["result"][0].get("items", [])
        
        if not items:
            print(f"  [WARNING]  No keyword suggestions found - topic may have zero search volume")
            return []
            
    except (IndexError, KeyError) as e:
        print(f"[ERROR] Error parsing response: {e}")
        print(f"Response structure: {json.dumps(response, indent=2)[:500]}")
        return []
    
    # Simplify the data structure
    simplified = []
    for item in items:
        info = item.get("keyword_info", {})
        props = item.get("keyword_properties", {})
        intent_info = item.get("search_intent_info", {})
        
        # Extract search intent from main_intent field (FIX: was using wrong fields)
        search_intent = None
        if intent_info and "main_intent" in intent_info:
            search_intent = intent_info.get("main_intent")
        
        simplified.append({
            "keyword": item.get("keyword"),
            "search_volume": info.get("search_volume", 0),
            "cpc": info.get("cpc", 0),
            "competition": info.get("competition", 0.0),
            "competition_level": info.get("competition_level", "LOW"),
            "difficulty": props.get("keyword_difficulty", 0),
            "search_intent": search_intent,  # Now correctly extracted!
            "monthly_searches": info.get("monthly_searches", [])
        })
    
    # Cache the results
    if use_cache:
        _save_to_cache(cache_key, simplified)
    
    return simplified


def get_related_keywords(seed_keyword: str,
                        location_name: str = "United States",
                        language_name: str = "English",
                        depth: int = 1,
                        limit: int = 10,
                        use_cache: bool = True) -> List[Dict]:
    """
    Get semantically related keywords using DataForSEO Labs endpoint.
    
    This finds keywords that are semantically related but may NOT contain
    your seed phrase. Examples for "hire react developer":
    - "react developer salary"
    - "react developer hourly rate"
    - "freelance react js cost"
    
    Uses Google's "searches related to" SERP section.
    
    Args:
        seed_keyword: The seed keyword/topic
        location_name: Geographic location (default: "United States")
        language_name: Language (default: "English")
        depth: How deep to traverse (default: 1 for budget control)
        limit: Max keywords per level (default: 10 for budget control)
        use_cache: Use cached results if available (default: True)
        
    Returns:
        List of keyword dicts with: keyword, search_volume, cpc, competition, difficulty, search_intent
    """
    endpoint = "/dataforseo_labs/google/related_keywords/live"
    
    task = {
        "keyword": seed_keyword,
        "location_name": location_name,
        "language_name": language_name,
        "depth": depth,
        "limit": limit,
        "include_seed_keyword": True,
        "include_serp_info": False,
        "filters": [["keyword_data.keyword_info.search_volume", ">", 0]]
    }
    
    # Check cache first
    if use_cache:
        cache_key = _get_cache_key(endpoint, task)
        cached_result = _get_from_cache(cache_key)
        if cached_result:
            print(f"  [OK] Using cached related keywords for '{seed_keyword}'")
            return cached_result
    
    # Make API request
    response = _make_request(endpoint, [task])
    
    # Check for errors
    if response.get("status_code") != 20000:
        print(f"[ERROR] API Error: {response.get('status_message', 'Unknown error')}")
        return []
    
    # Extract items from response
    try:
        if "tasks" not in response or not response["tasks"]:
            print(f"[ERROR] No tasks in response")
            return []
            
        task_result = response["tasks"][0]
        if task_result.get("status_code") != 20000:
            print(f"[ERROR] Task error: {task_result.get('status_message', 'Unknown error')}")
            return []
        
        if "result" not in task_result or not task_result["result"]:
            print(f"[ERROR] No result in task")
            return []
            
        items = task_result["result"][0].get("items", [])
        
        if not items:
            print(f"  [WARNING]  No related keywords found")
            return []
            
    except (IndexError, KeyError) as e:
        print(f"[ERROR] Error parsing response: {e}")
        return []
    
    # Flatten nested structure and extract data
    simplified = []
    for item in items:
        # Main keyword (has full data)
        keyword_data = item.get("keyword_data", {})
        info = keyword_data.get("keyword_info", {})
        props = keyword_data.get("keyword_properties", {})
        intent_info = keyword_data.get("search_intent_info", {})
        
        # Extract search intent from main_intent field
        search_intent = None
        if intent_info and "main_intent" in intent_info:
            search_intent = intent_info.get("main_intent")
        
        simplified.append({
            "keyword": keyword_data.get("keyword"),
            "search_volume": info.get("search_volume", 0),
            "cpc": info.get("cpc", 0),
            "competition": info.get("competition", 0.0),
            "competition_level": info.get("competition_level", "LOW"),
            "difficulty": props.get("keyword_difficulty", 0),
            "search_intent": search_intent,
            "monthly_searches": info.get("monthly_searches", [])
        })
        
        # NOTE: related_keywords are just strings (no full data)
        # We'd need separate API calls to get data for each
        # For budget control, we skip this for now
    
    # Cache the results
    if use_cache:
        _save_to_cache(cache_key, simplified)
    
    return simplified





def basic_keyword_brief(seed_keyword: str,
                       location_name: str = "United States",
                       language_name: str = "English",
                       limit: int = 30,
                       use_related: bool = True,
                       related_limit: int = 10) -> Dict:
    """
    Generate a keyword brief.
    
    If data is found: Returns main, secondary, and long-tail keywords with metrics.
    If NO data is found: Returns explicit signal for AI to take over semantically.
    
    Args:
        seed_keyword: The topic/seed phrase
        location_name: Geographic location
        language_name: Language
        limit: Max suggestions to analyze
        use_related: Also fetch semantically related keywords
        related_limit: Max related keywords to fetch
        
    Returns:
        Dict with keywords or 'manual_mode' flag if no data.
    """
    print(f"Generating keyword brief for: '{seed_keyword}'...")
    
    # Step 1: Get keyword suggestions (phrase matches)
    suggestions = get_keyword_suggestions(
        seed_keyword,
        location_name=location_name,
        language_name=language_name,
        limit=limit
    )
    
    all_keywords = []
    if suggestions:
        all_keywords.extend(suggestions)
    
    # Step 2: Optionally get related keywords (semantic neighbors)
    if use_related:
        print(f"  - Fetching semantic neighbors...")
        related = get_related_keywords(
            seed_keyword,
            location_name=location_name,
            language_name=language_name,
            depth=1,
            limit=related_limit
        )
        
        if related:
            print(f"  [OK] Found {len(related)} related keywords")
            # Merge and dedupe
            seen_keywords = {kw["keyword"].lower() for kw in all_keywords}
            for kw in related:
                if kw["keyword"].lower() not in seen_keywords:
                    all_keywords.append(kw)
                    seen_keywords.add(kw["keyword"].lower())

    # ZERO-VOLUME / LOW DATA HANDLING
    # If we have very few keywords or no data, signal AI to take over
    if not all_keywords or len(all_keywords) < 3:
        print("  [WARNING]  Low/No data found. Signaling AI to use Semantic Mode.")
        return {
            "seed": seed_keyword,
            "manual_mode": True,  # SIGNAL FOR AI AGENT
            "reason": "Low or zero search volume data found",
            "main_keyword": seed_keyword, 
            "main_keyword_data": None,
            "secondary_keywords": [],
            "long_tail_keywords": [],
            "intent_breakdown": {},
            "all_suggestions": []
        }
    
    print(f"  [OK] Total unique keywords: {len(all_keywords)}")
    
    # Sort by search volume (highest first)
    suggestions_sorted = sorted(
        all_keywords,
        key=lambda x: x.get("search_volume", 0),
        reverse=True
    )
    
    # MAIN KEYWORD SELECTION:
    # Prefer keyword that matches core seed phrase + has good volume
    # Extract core words from seed (remove common modifiers)
    core = seed_keyword.lower()
    for modifier in ["best", "top", "how to", "what is", "for"]:
        core = core.replace(modifier, "")
    core_words = [w.strip() for w in core.split() if w.strip()]
    
    def matches_seed_intent(kw: str) -> bool:
        """Check if keyword contains core seed words"""
        kw_low = kw.lower()
        return any(word in kw_low for word in core_words if len(word) > 2)
    
    # Pick first high-volume keyword that matches seed intent
    main = None
    for s in suggestions_sorted:
        if s["keyword"] and matches_seed_intent(s["keyword"]):
            main = s
            break
    
    # Fallback to highest volume if no match
    if main is None:
        main = suggestions_sorted[0]
    
    print(f"  [OK] Main keyword: '{main['keyword']}' ({main['search_volume']} vol, ${(main['cpc'] or 0):.2f} CPC, intent: {main.get('search_intent', 'unknown')})")
    
    # SECONDARY KEYWORDS: next 5 highest-volume suggestions
    secondary_candidates = [
        s for s in suggestions_sorted
        if s["keyword"] != main["keyword"]
    ]
    secondary = secondary_candidates[:5]
    
    print(f"  [OK] Secondary keywords: {len(secondary)}")
    
    # LONG-TAIL KEYWORDS: remaining suggestions (limit to 10)
    long_tail = secondary_candidates[5:15]
    
    print(f"  [OK] Long-tail keywords: {len(long_tail)}")
    
    # INTENT BREAKDOWN: Analyze search intent across all keywords
    intent_counts = {"informational": 0, "commercial": 0, "transactional": 0, "navigational": 0, "unknown": 0}
    for kw in all_keywords:
        intent = kw.get("search_intent", "unknown")
        if intent:
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        else:
            intent_counts["unknown"] += 1
    
    print(f"  [OK] Intent breakdown: {', '.join(f'{k}: {v}' for k, v in intent_counts.items() if v > 0)}")
    
    return {
        "seed": seed_keyword,
        "manual_mode": False,
        "main_keyword": main["keyword"],
        "main_keyword_data": main,
        "secondary_keywords": [s["keyword"] for s in secondary],
        "secondary_keywords_data": secondary,
        "long_tail_keywords": [s["keyword"] for s in long_tail],
        "long_tail_keywords_data": long_tail,
        "intent_breakdown": intent_counts,
        "all_suggestions": suggestions_sorted
    }
    
    # MAIN KEYWORD SELECTION:
    # Prefer keyword that matches core seed phrase + has good volume
    # Extract core words from seed (remove common modifiers)
    core = seed_keyword.lower()
    for modifier in ["best", "top", "how to", "what is", "for"]:
        core = core.replace(modifier, "")
    core_words = [w.strip() for w in core.split() if w.strip()]
    
    def matches_seed_intent(kw: str) -> bool:
        """Check if keyword contains core seed words"""
        kw_low = kw.lower()
        return any(word in kw_low for word in core_words if len(word) > 2)
    
    # Pick first high-volume keyword that matches seed intent
    main = None
    for s in suggestions_sorted:
        if s["keyword"] and matches_seed_intent(s["keyword"]):
            main = s
            break
    
    # Fallback to highest volume if no match
    if main is None:
        main = suggestions_sorted[0]
    
    print(f"  [OK] Main keyword: '{main['keyword']}' ({main['search_volume']} vol, ${(main['cpc'] or 0):.2f} CPC, intent: {main.get('search_intent', 'unknown')})")
    
    # SECONDARY KEYWORDS: next 5 highest-volume suggestions
    secondary_candidates = [
        s for s in suggestions_sorted
        if s["keyword"] != main["keyword"]
    ]
    secondary = secondary_candidates[:5]
    
    print(f"  [OK] Secondary keywords: {len(secondary)}")
    
    # LONG-TAIL KEYWORDS: remaining suggestions (limit to 10)
    long_tail = secondary_candidates[5:15]
    
    print(f"  [OK] Long-tail keywords: {len(long_tail)}")
    
    # INTENT BREAKDOWN: Analyze search intent across all keywords
    intent_counts = {"informational": 0, "commercial": 0, "transactional": 0, "navigational": 0, "unknown": 0}
    for kw in all_keywords:
        intent = kw.get("search_intent", "unknown")
        if intent:
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        else:
            intent_counts["unknown"] += 1
    
    print(f"  [OK] Intent breakdown: {', '.join(f'{k}: {v}' for k, v in intent_counts.items() if v > 0)}")
    
    return {
        "seed": seed_keyword,
        "main_keyword": main["keyword"],
        "main_keyword_data": main,
        "secondary_keywords": [s["keyword"] for s in secondary],
        "secondary_keywords_data": secondary,
        "long_tail_keywords": [s["keyword"] for s in long_tail],
        "long_tail_keywords_data": long_tail,
        "intent_breakdown": intent_counts,
        "all_suggestions": suggestions_sorted
    }


# =============================================================================
# CLI INTERFACE
# =============================================================================

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="DataForSEO Labs Keyword Research Tool")
    parser.add_argument("command", choices=["brief", "suggestions"], help="Command to run")
    parser.add_argument("keyword", help="Seed keyword or topic")
    parser.add_argument("--limit", type=int, default=30, help="Max keywords to return (default: 30)")
    parser.add_argument("--output", help="Save results to JSON file")
    parser.add_argument("--location", default="United States", help="Location (default: United States)")
    parser.add_argument("--language", default="English", help="Language (default: English)")
    
    args = parser.parse_args()
    
    if args.command == "brief":
        result = basic_keyword_brief(
            args.keyword,
            location_name=args.location,
            language_name=args.language,
            limit=args.limit
        )
        
        # Print results
        print("\n" + "="*70)
        print("KEYWORD BRIEF")
        print("="*70)
        print(f"\n[TARGET] Main Keyword: {result['main_keyword']}")
        if result['main_keyword_data']:
            data = result['main_keyword_data']
            print(f"   Volume: {data['search_volume']}")
            print(f"   CPC: ${(data['cpc'] or 0):.2f}")
            print(f"   Difficulty: {data['difficulty']}/100")
        
        print(f"\n[SECONDARY] Secondary Keywords ({len(result['secondary_keywords'])}):")
        for kw in result['secondary_keywords']:
            print(f"   - {kw}")
        
        print(f"\n[LONG-TAIL] Long-tail Keywords ({len(result['long_tail_keywords'])}):")
        for kw in result['long_tail_keywords'][:5]:  # Show first 5
            print(f"   - {kw}")
        if len(result['long_tail_keywords']) > 5:
            print(f"   ... and {len(result['long_tail_keywords']) - 5} more")
        
        if result.get("manual_mode"):
            print("\n!!! LOW DATA VOLUME DETECTED - SEMANTIC STRATEGY REQUIRED !!!")
            print("The API returned low or no data for this specific topic.")
            print("Switching to SEMANTIC KEYWORD STRATEGY.")
            print("You must brainstorm keywords yourself based on the topic.")

        # Save to file if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            print(f"\n[SAVED] Full results saved to: {args.output}")
    
    elif args.command == "suggestions":
        suggestions = get_keyword_suggestions(
            args.keyword,
            location_name=args.location,
            language_name=args.language,
            limit=args.limit
        )
        
        print("\n" + "="*70)
        print("KEYWORD SUGGESTIONS")
        print("="*70)
        print(f"\nFound {len(suggestions)} keywords:\n")
        
        for i, kw in enumerate(suggestions[:20], 1):  # Show first 20
            print(f"{i:2}. {kw['keyword']:40} Vol: {kw['search_volume']:6}  CPC: ${(kw['cpc'] or 0):6.2f}  Diff: {kw['difficulty']:3}/100")
        
        if len(suggestions) > 20:
            print(f"\n... and {len(suggestions) - 20} more")
        
        # Save if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(suggestions, f, indent=2)
            print(f"\n[SAVED] Results saved to: {args.output}")
