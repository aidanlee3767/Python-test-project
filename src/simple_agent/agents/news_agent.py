# flake8: noqa: E501

import time
from typing import Optional, List, Dict, Any

import pandas as pd
import requests

from src.simple_agent.agents.parse_url import parse_article_content

NEWS_API_KEY = "b01f1c03cbb44b31a1ad0fb98c6eb155"

# News API Constants
TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
EVERYTHING_URL = "https://newsapi.org/v2/everything"

COUNTRIES = {
    "ae", "ar", "at", "au", "be", "bg", "br", "ca", "ch", "cn", "co", "cu", "cz",
    "de", "eg", "fr", "gb", "gr", "hk", "hu", "id", "ie", "il", "in", "it", "jp",
    "kr", "lt", "lv", "ma", "mx", "my", "ng", "nl", "no", "nz", "ph", "pl", "pt",
    "ro", "rs", "ru", "sa", "se", "sg", "si", "sk", "th", "tr", "tw", "ua", "us",
    "ve", "za",
}

DEFAULT_LANGUAGES = {
    "ae": "ar", "ar": "es", "at": "de", "au": "en", "be": "nl", "bg": "bg",
    "br": "pt", "ca": "en", "ch": "de", "cn": "zh", "co": "es", "cu": "es",
    "cz": "cs", "de": "de", "eg": "ar", "fr": "fr", "gb": "en", "gr": "el",
    "hk": "zh", "hu": "hu", "id": "id", "ie": "en", "il": "he", "in": "hi",
    "it": "it", "jp": "ja", "kr": "ko", "lt": "lt", "lv": "lv", "ma": "ar",
    "mx": "es", "my": "ms", "ng": "en", "nl": "nl", "no": "no", "nz": "en",
    "ph": "en", "pl": "pl", "pt": "pt", "ro": "ro", "rs": "sr", "ru": "ru",
    "sa": "ar", "se": "sv", "sg": "en", "si": "sl", "sk": "sk", "th": "th",
    "tr": "tr", "tw": "zh", "ua": "uk", "us": "en", "ve": "es", "za": "zu",
}

LANGUAGES = {
    "ar", "de", "en", "es", "fr", "he", "it", "nl", "no", "pt", "ru", "sv", "ud", "zh"
}

CATEGORIES = {
    "business", "entertainment", "general", "health", "science", "sports", "technology"
}


def validate_parameters(
    country: Optional[str] = None,
    language: Optional[str] = None,
    category: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Validate and auto-correct API parameters.
    
    Returns:
        dict: Validated parameters with warnings if any
    """
    warnings = []
    validated = {}
    
    # Validate country
    if country:
        country = country.lower()
        if country not in COUNTRIES:
            warnings.append(f"Invalid country code: '{country}'. Available: {sorted(COUNTRIES)}")
            country = None
        else:
            validated["country"] = country
    
    # Validate language
    if language:
        language = language.lower()
        if language not in LANGUAGES:
            warnings.append(f"Invalid language code: '{language}'. Available: {sorted(LANGUAGES)}")
            language = None
        else:
            validated["language"] = language
    
    # Auto-set default language for country if not specified
    if country and not language and country in DEFAULT_LANGUAGES:
        validated["language"] = DEFAULT_LANGUAGES[country]
        print(f"💡 Auto-set language to '{DEFAULT_LANGUAGES[country]}' for country '{country}'")
    
    # Validate category
    if category:
        category = category.lower()
        if category not in CATEGORIES:
            warnings.append(f"Invalid category: '{category}'. Available: {sorted(CATEGORIES)}")
            category = None
        else:
            validated["category"] = category
    
    return {"params": validated, "warnings": warnings}


def get_latest_news_json(
    num_articles: int = 10,
    category: Optional[str] = None,
    country: Optional[str] = None,
    query: Optional[str] = None,
    language: Optional[str] = None,
    sort_by: str = "publishedAt",
) -> List[Dict[str, Any]]:
    """
    Fetch latest news articles from News API in JSON format.

    Args:
        num_articles (int): Number of articles to fetch (default: 10, max: 100)
        category (str): Category (business, entertainment, general, health, science, sports, technology)
        country (str): 2-letter country code (us, kr, gb, etc.)
        query (str): Search keyword (e.g., "Seoul", "AI", "Olympics")
        language (str): 2-letter language code (en, ko, es, etc.)
        sort_by (str): Sort order - 'publishedAt' (newest), 'relevancy', or 'popularity'

    Returns:
        list: List of article dictionaries. Returns empty list on error.
    """
    if not NEWS_API_KEY:
        print("❌ Error: NewsAPI key not configured.")
        return []

    # Validate parameters
    validation = validate_parameters(country, language, category)
    
    # Show warnings
    for warning in validation["warnings"]:
        print(f"⚠️  {warning}")
    
    validated_params = validation["params"]
    
    # Use /everything endpoint if query is provided, otherwise /top-headlines
    if query:
        url = EVERYTHING_URL
        params = {
            "apiKey": NEWS_API_KEY,
            "q": query,
            "pageSize": min(num_articles, 100),
            "sortBy": sort_by,
        }
        # Add language if specified
        if "language" in validated_params:
            params["language"] = validated_params["language"]
    else:
        url = TOP_HEADLINES_URL
        params = {
            "apiKey": NEWS_API_KEY,
            "pageSize": min(num_articles, 100),
        }
        # Add validated parameters
        if "category" in validated_params:
            params["category"] = validated_params["category"]
        if "country" in validated_params:
            params["country"] = validated_params["country"]
        if "language" in validated_params:
            params["language"] = validated_params["language"]

    try:
        print(f"🔍 Fetching news with parameters: {params}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Check API response status
        if data.get("status") != "ok":
            print(f"❌ API Error: {data.get('message', 'Unknown error')}")
            return []

        articles = data.get("articles", [])

        if not articles:
            print("💡 No articles found matching criteria.")
            return []

        print(f"✅ Found {len(articles)} articles.")
        return articles

    except requests.exceptions.RequestException as e:
        print(f"❌ API request error: {e}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return []


def get_latest_news_formatted(
    num_articles: int = 10,
    category: Optional[str] = None,
    country: Optional[str] = None,
    query: Optional[str] = None,
    language: Optional[str] = None,
) -> List[str]:
    """Get news as formatted string list."""
    articles = get_latest_news_json(num_articles, category, country, query, language)

    formatted_news = []
    for i, article in enumerate(articles):
        title = article.get("title", "No title")
        url = article.get("url", "")
        source = article.get("source", {}).get("name", "Unknown source")
        published_at = article.get("publishedAt", "")
        formatted_news.append(
            f"{i + 1}. [{source}] {title}\n"
            f"   Published: {published_at}\n"
            f"   Link: {url}"
        )

    return formatted_news


def get_latest_news_dataframe(
    num_articles: int = 10,
    category: Optional[str] = None,
    country: Optional[str] = None,
    query: Optional[str] = None,
    language: Optional[str] = None,
    include_parsed_content: bool = True,
) -> pd.DataFrame:
    """Get news as pandas DataFrame."""
    articles = get_latest_news_json(num_articles, category, country, query, language)

    if not articles:
        return pd.DataFrame()

    df_data = {
        "Source": [a.get("source", {}).get("name", "") for a in articles],
        "Author": [a.get("author", "") for a in articles],
        "Title": [a.get("title", "") for a in articles],
        "Description": [a.get("description", "") for a in articles],
        "URL": [a.get("url", "") for a in articles],
        "Published At": [a.get("publishedAt", "") for a in articles],
        "Content": [a.get("content", "") for a in articles],
    }

    df = pd.DataFrame(df_data)

    print(f"\n✅ DataFrame created with shape: {df.shape}")

    if include_parsed_content:
        df = add_parsed_content_to_dataframe(df)
        print("\n✅ Content parsing complete!")

    return df


def get_news_content(url: str) -> Dict[str, Any]:
    """Fetch and parse full article content from URL."""
    try:
        parsed_data = parse_article_content(url)
        return {
            "Parsed Content": parsed_data.get("content", ""),
            "Parsed Author": parsed_data.get("author", ""),
            "Meta Description": parsed_data.get("meta_description", ""),
            "Parsed Publish Date": parsed_data.get("publish_date", ""),
            "Tags": ", ".join(parsed_data.get("tags", [])),
            "Word Count": parsed_data.get("word_count", 0),
            "Reading Time (min)": parsed_data.get("reading_time", 0),
            "Parse Status": parsed_data.get("status", "not_attempted"),
        }
    except Exception as e:
        print(f"❌ Error parsing article: {e}")
        return {
            "Parsed Content": "",
            "Parsed Author": "",
            "Meta Description": "",
            "Parsed Publish Date": "",
            "Tags": "",
            "Word Count": 0,
            "Reading Time (min)": 0,
            "Parse Status": "error",
        }


def add_parsed_content_to_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Add parsed content columns to existing DataFrame."""
    df_copy = df.copy()

    # Initialize new columns
    new_cols = {
        "Parsed Content": "",
        "Parsed Author": "",
        "Meta Description": "",
        "Parsed Publish Date": "",
        "Tags": "",
        "Word Count": 0,
        "Reading Time (min)": 0,
        "Parse Status": "pending",
    }
    
    for col, default in new_cols.items():
        df_copy[col] = default

    # Parse each URL
    for index, row in df_copy.iterrows():
        print(f"🔍 [{index + 1}/{len(df_copy)}] Parsing: {row['Title'][:50]}...")
        
        url = row["URL"]
        parsed_data = get_news_content(url)

        for key, value in parsed_data.items():
            df_copy.at[index, key] = value

        time.sleep(1)  # Rate limiting

    return df_copy


if __name__ == "__main__":
    # Example usage demonstrating the enhanced features

    # 1. US Technology news
    print("\n=== US Technology News ===")
    df_us_tech = get_latest_news_dataframe(
        num_articles=5,
        category="technology",
        country="us",
        include_parsed_content=False
    )

    # 2. Korean news (auto-set language to Korean)
    print("\n=== Korean News ===")
    df_korea = get_latest_news_dataframe(
        num_articles=5,
        country="kr",
        include_parsed_content=False
    )

    # 3. Search query: AI news in English
    print("\n=== AI News (English) ===")
    df_ai = get_latest_news_dataframe(
        num_articles=5,
        query="artificial intelligence",
        language="en",
        include_parsed_content=False
    )

    # 4. UK Business news
    print("\n=== UK Business News ===")
    df_uk_business = get_latest_news_dataframe(
        num_articles=5,
        category="business",
        country="gb",
        include_parsed_content=False
    )

    # 5. Spanish health news
    print("\n=== Spanish Health News ===")
    df_es_health = get_latest_news_dataframe(
        num_articles=5,
        category="health",
        language="es",
        include_parsed_content=False
    )

    # Save examples
    if not df_us_tech.empty:
        df_us_tech.to_csv("us_tech_news.csv", index=False)
        print("\n✅ Saved to us_tech_news.csv")