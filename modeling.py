from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from news import get_latest_it_news_dataframe

if __name__ == "__main__":
    df = get_latest_it_news_dataframe(10)
    makeshift = df["Content"].to_dict()
    clean_texts = [text for text in makeshift.values() if text is not None]
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(clean_texts)

    # Option 2: Use CountVectorizer for LDA (LDA works better with raw counts)
    count_vectorizer = CountVectorizer(max_features=100, stop_words="english")
    doc_word_matrix = count_vectorizer.fit_transform(
        clean_texts
    )  # Use clean_texts, not tfidf_matrix

    # 3. LDA 모델 학습
    lda = LatentDirichletAllocation(n_components=2, random_state=42)
    lda.fit(doc_word_matrix)

    # 4. 토픽별 주요 단어 확인
    feature_names = count_vectorizer.get_feature_names_out()  # Use count_vectorizer
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[-5:][::-1]]
        print(f"토픽 {topic_idx + 1}: {', '.join(top_words)}")

    # Optional: If you also want clustering
    print("\n=== 클러스터링 결과 ===")
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(tfidf_matrix)

    # Create result DataFrame
    valid_indices = [i for i, text in enumerate(df["Content"]) if text is not None]
    cluster_df = df.iloc[valid_indices].copy()
    cluster_df["Cluster"] = clusters

    print("클러스터 분포:")
    print(cluster_df["Cluster"].value_counts().sort_index())
