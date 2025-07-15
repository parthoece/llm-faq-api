import requests
import html

def fetch_stackoverflow_posts(query, max_posts=3):
    url = "https://api.stackexchange.com/2.3/search/advanced"
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "pagesize": max_posts
    }
    res = requests.get(url, params=params)
    posts = res.json().get("items", [])
    return [f"{'✅' if p['is_answered'] else '❌'} {html.unescape(p['title'])} ({p['link']})" for p in posts]