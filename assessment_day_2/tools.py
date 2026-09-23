import json
import re
from config import PRODUCTS, MOCK_DATABASE_DISCLAIMER

# Mock Product Search Tool Disclaimer
TOOL_DISCLAIMER = (
    "This is a mock product-search tool for demonstrating external tool use. "
    "It searches a fictional local database and does NOT access live shopping websites."
)

def search_products(query: str) -> str:
    """
    Search the mock smartphone database for product information based on a query.
    Supports specific filters like 'highest RAM', 'cheapest phone', 'phones under X', 
    '256 GB phones', 'at least 8 GB RAM', or general keyword searching.
    """
    query_lower = query.lower().strip()
    
    results = []

    # Filter 1: Highest RAM
    if "highest ram" in query_lower or "max ram" in query_lower or "maximum ram" in query_lower:
        max_ram = max(p["ram"] for p in PRODUCTS.values())
        top_phones = {k: v for k, v in PRODUCTS.items() if v["ram"] == max_ram}
        return json.dumps({
            "disclaimer": TOOL_DISCLAIMER,
            "query": query,
            "match_type": "highest_ram",
            "results": top_phones
        }, indent=2)

    # Filter 2: Cheapest phone
    if "cheapest" in query_lower or "lowest price" in query_lower or "minimum price" in query_lower:
        min_price = min(p["price"] for p in PRODUCTS.values())
        cheapest = {k: v for k, v in PRODUCTS.items() if v["price"] == min_price}
        return json.dumps({
            "disclaimer": TOOL_DISCLAIMER,
            "query": query,
            "match_type": "cheapest_phone",
            "results": cheapest
        }, indent=2)

    # Filter 3: Price threshold (e.g. "under 25000", "under ₹25,000", "budget 27000")
    price_match = re.search(r'(?:under|below|budget|less than|\<=?)\s*(?:₹|rs\.?)?\s*([\d,]+)', query_lower)
    if price_match:
        limit = int(price_match.group(1).replace(',', ''))
        filtered = {k: v for k, v in PRODUCTS.items() if v["price"] <= limit}
        return json.dumps({
            "disclaimer": TOOL_DISCLAIMER,
            "query": query,
            "match_type": f"price_under_{limit}",
            "results": filtered
        }, indent=2)

    # Filter 4: RAM requirement (e.g. "at least 8 GB RAM", "8 gb ram")
    ram_match = re.search(r'(\d+)\s*gb\s*ram', query_lower)
    if ram_match:
        min_ram = int(ram_match.group(1))
        filtered = {k: v for k, v in PRODUCTS.items() if v["ram"] >= min_ram}
        return json.dumps({
            "disclaimer": TOOL_DISCLAIMER,
            "query": query,
            "match_type": f"min_ram_{min_ram}gb",
            "results": filtered
        }, indent=2)

    # Filter 5: Storage requirement (e.g. "256 GB phones", "256 gb storage")
    storage_match = re.search(r'(\d+)\s*gb\s*storage|\b(\d+)\s*gb\b', query_lower)
    if storage_match:
        target_storage = int(storage_match.group(1) or storage_match.group(2))
        filtered = {k: v for k, v in PRODUCTS.items() if v["storage"] == target_storage}
        if filtered:
            return json.dumps({
                "disclaimer": TOOL_DISCLAIMER,
                "query": query,
                "match_type": f"storage_{target_storage}gb",
                "results": filtered
            }, indent=2)

    # Filter 6: General Keyword Search / Full Catalog Return
    matched = {}
    for name, specs in PRODUCTS.items():
        if query_lower in name.lower() or query_lower in ["all", "phones", "smartphones", "catalog", "products", "search"]:
            matched[name] = specs
            
    if not matched:
        matched = PRODUCTS  # Fallback to returning all products for inspection if query is general

    return json.dumps({
        "disclaimer": TOOL_DISCLAIMER,
        "query": query,
        "match_type": "general_search",
        "results": matched
    }, indent=2)


# OpenAI / Groq Tool Schema Definition
SEARCH_PRODUCTS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_products",
        "description": "Search the mock smartphone database for product information such as price, RAM, storage, battery, and ratings.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query or criteria (e.g., 'highest RAM', 'cheapest phone', 'phones under 25000', '256 GB phones', 'at least 8 GB RAM')."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
}
