# https://newsapi.org/sources
# https://newsapi.org/docs/client-libraries/python
# flake8: noqa: E501

import time
from typing import Optional

import pandas as pd
import requests

from simple_agent.agents.parse_url import parse_article_content

NEWS_API_KEY = "b01f1c03cbb44b31a1ad0fb98c6eb155"


def get_latest_news_json(
    num_articles: int = 10,
    category: Optional[str] = None,
    country: Optional[str] = "us",
    query: Optional[str] = None,
    language: str = "en",
):
    """
    NewsAPI를 사용하여 최신 뉴스 기사를 JSON 형태로 가져옵니다.

    Args:
        num_articles (int): 가져올 기사 수 (기본값: 10)
        category (str): 카테고리 (technology, business, entertainment, health, science, sports)
        country (str): 국가 코드 (us, kr, etc.)
        query (str): 검색 키워드 (e.g., "Seoul", "culture", "K-pop")
        language (str): 언어 코드 (en, ko, etc.)

    Returns:
        list: 기사 목록. 오류 발생 시 빈 리스트를 반환합니다.
    """
    if not NEWS_API_KEY:
        print("❌ 에러: NewsAPI 키가 설정되지 않았습니다.")
        return []

    # query가 있으면 /everything 엔드포인트 사용 (더 유연함)
    if query:
        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": NEWS_API_KEY,
            "q": query,
            "language": language,
            "pageSize": num_articles,
            "sortBy": "publishedAt",  # 최신순
        }
    else:
        # query가 없으면 /top-headlines 사용
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "pageSize": num_articles,
        }
        if category:
            params["category"] = category
        if country:
            params["country"] = country

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # API 에러 체크
        if data.get("status") != "ok":
            print(f"❌ API 에러: {data.get('message', 'Unknown error')}")
            return []

        articles = data.get("articles", [])

        if not articles:
            print("💡 새로운 뉴스를 찾을 수 없습니다.")
            return []

        print(f"✅ {len(articles)}개의 기사를 찾았습니다.")
        return articles

    except requests.exceptions.RequestException as e:
        print(f"❌ API 요청 중 에러가 발생했습니다: {e}")
        return []
    except Exception as e:
        print(f"❌ 알 수 없는 에러가 발생했습니다: {e}")
        return []


def get_latest_news_formatted(
    num_articles: int = 10,
    category: Optional[str] = None,
    country: Optional[str] = "us",
    query: Optional[str] = None,
    language: str = "en",
):
    """뉴스를 포맷팅된 문자열 리스트로 반환"""
    articles = get_latest_news_json(num_articles, category, country, query, language)

    formatted_news = []
    for i, article in enumerate(articles):
        title = article.get("title", "제목 없음")
        url = article.get("url", "")
        source = article.get("source", {}).get("name", "출처 불명")
        formatted_news.append(f"{i + 1}. [{source}] {title}\n   - 링크: {url}")

    return formatted_news


def get_latest_news_dataframe(
    num_articles: int = 10,
    category: Optional[str] = None,
    country: Optional[str] = "us",
    query: Optional[str] = None,
    language: str = "en",
    include_parsed_content: bool = True,
) -> pd.DataFrame:
    """뉴스를 DataFrame으로 반환"""
    articles = get_latest_news_json(num_articles, category, country, query, language)

    if not articles:
        return pd.DataFrame()

    sources = []
    authors = []
    titles = []
    descriptions = []
    urls = []
    published_ats = []
    contents = []

    for article in articles:
        sources.append(article.get("source", {}).get("name", ""))
        authors.append(article.get("author", ""))
        titles.append(article.get("title", ""))
        descriptions.append(article.get("description", ""))
        urls.append(article.get("url", ""))
        published_ats.append(article.get("publishedAt", ""))
        contents.append(article.get("content", ""))

    new_article_data = {
        "Source": sources,
        "Author": authors,
        "Title": titles,
        "Description": descriptions,
        "URL": urls,
        "Published At": published_ats,
        "Content": contents,
    }

    df = pd.DataFrame(new_article_data)

    print("\n✅ DataFrame 변환 완료!")
    print(f"DataFrame 크기: {df.shape} (행: {df.shape[0]}, 열: {df.shape[1]})")

    if include_parsed_content:
        df = add_parsed_content_to_dataframe(df)
        print("\n✅ 파싱 완료!")

    return df


def get_news_content(url: str):
    """주어진 URL에서 뉴스 기사의 내용을 가져옵니다."""
    try:
        parsed_data = parse_article_content(url)

        res = {
            "Parsed Content": parsed_data.get("content", ""),
            "Parsed Author": parsed_data.get("author", ""),
            "Meta Description": parsed_data.get("meta_description", ""),
            "Parsed Publish Date": parsed_data.get("publish_date", ""),
            "Tags": ", ".join(parsed_data.get("tags", [])),
            "Word Count": parsed_data.get("word_count", 0),
            "Reading Time (min)": parsed_data.get("reading_time", 0),
            "Parse Status": parsed_data.get("status", "not_attempted"),
        }

        return res

    except Exception as e:
        print(f"❌ 뉴스 기사 내용을 가져오는 중 에러 발생: {e}")
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
    """기존 DataFrame에 URL 파싱 결과 추가"""
    df_copy = df.copy()

    # 새 컬럼들 초기화
    df_copy["Parsed Content"] = ""
    df_copy["Parsed Author"] = ""
    df_copy["Meta Description"] = ""
    df_copy["Parsed Publish Date"] = ""
    df_copy["Tags"] = ""
    df_copy["Word Count"] = 0
    df_copy["Reading Time (min)"] = 0
    df_copy["Parse Status"] = "pending"

    for index, row in df_copy.iterrows():
        print(f"🔍 [{index + 1}/{len(df_copy)}] {row['Title'][:40]}...")

        url = row["URL"]
        parsed_data = get_news_content(url)

        df_copy.at[index, "Parsed Content"] = parsed_data["Parsed Content"]
        df_copy.at[index, "Parsed Author"] = parsed_data["Parsed Author"]
        df_copy.at[index, "Meta Description"] = parsed_data["Meta Description"]
        df_copy.at[index, "Parsed Publish Date"] = parsed_data["Parsed Publish Date"]
        df_copy.at[index, "Tags"] = parsed_data["Tags"]
        df_copy.at[index, "Word Count"] = parsed_data["Word Count"]
        df_copy.at[index, "Reading Time (min)"] = parsed_data["Reading Time (min)"]
        df_copy.at[index, "Parse Status"] = parsed_data["Parse Status"]

        time.sleep(1)

    return df_copy


if __name__ == "__main__":
    # 사용 예시:

    # 1. IT 뉴스 (기존 방식)
    print("\n=== IT 뉴스 ===")
    df_tech = get_latest_news_dataframe(
        5, category="technology", include_parsed_content=False
    )

    # 2. Seoul 관련 뉴스
    print("\n=== Seoul 뉴스 ===")
    df_seoul = get_latest_news_dataframe(5, query="Seoul", include_parsed_content=False)

    # 3. 문화 뉴스
    print("\n=== 문화 뉴스 ===")
    df_culture = get_latest_news_dataframe(
        5, query="culture", include_parsed_content=False
    )

    # 4. 한국 뉴스 (한글)
    print("\n=== 한국 뉴스 ===")
    df_korea = get_latest_news_dataframe(
        5, country="kr", language="ko", include_parsed_content=False
    )

    # CSV 저장 예시
    df_tech.to_csv("it_news_articles.csv", index=False)
