import requests


def wikipedia_search(query: str, max_chars: int = 2000) -> str:
    direct_result = _fetch_summary(query)
    if direct_result:
        return direct_result[:max_chars]

    fallback_title = _search_best_match(query)
    if fallback_title:
        return _fetch_summary(fallback_title)[:max_chars]

    return ""


def _fetch_summary(title: str) -> str:
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + requests.utils.quote(title)
        resp = requests.get(url, timeout=8)
        if resp.status_code == 200:
            return resp.json().get("extract", "")
    except requests.RequestException:
        pass
    return ""


def _search_best_match(query: str) -> str:
    try:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 2,
        }
        resp = requests.get("https://en.wikipedia.org/w/api.php", params=params, timeout=8)
        if resp.status_code == 200:
            results = resp.json().get("query", {}).get("search", [])
            if results:
                return results[0]["title"]
    except requests.RequestException:
        pass
    return ""