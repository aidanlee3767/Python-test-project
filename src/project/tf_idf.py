from news import get_latest_it_news_dataframe
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

if __name__ == "__main__":
    df = get_latest_it_news_dataframe(10)
    vectorizer = TfidfVectorizer()
    makeshift = df["Content"].to_dict()
    clean_texts = [text for text in makeshift.values() if text is not None]
    tfidf_matrix = vectorizer.fit_transform(clean_texts)

    def perform_clustering(tfidf_matrix, df, n_clusters=3):
        """K-means clustering"""
        # K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(tfidf_matrix)

        # Create result DataFrame
        # Since we filtered out None values, we need to get the valid indices
        valid_indices = [i for i, text in enumerate(df["Content"]) if text is not None]
        cluster_df = df.iloc[valid_indices].copy()
        cluster_df["Cluster"] = clusters
        return cluster_df, kmeans

    # Use the function
    clustered_df, kmeans_model = perform_clustering(tfidf_matrix, df, n_clusters=3)
    print(clustered_df[["Content", "Cluster"]])
