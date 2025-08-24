from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from news import get_latest_it_news_dataframe


def compute_similarity_matrix(self):
    """코사인 유사도 행렬 계산"""
    self.similarity_matrix = cosine_similarity(self.tfidf_matrix)
    return self.similarity_matrix


def find_similar_articles(self, article_index, df, n_similar=3):
    """특정 기사와 유사한 기사들 찾기"""
    similarities = self.similarity_matrix[article_index].copy()
    similarities[article_index] = -1  # 자기 자신 제외
    # 상위 유사 기사 인덱스
    similar_indices = similarities.argsort()[-n_similar:][::-1]
    print(similar_indices)
    return similar_indices


if __name__ == "__main__":
    df = get_latest_it_news_dataframe(10)
    vectorizer = TfidfVectorizer()
    makeshift = df["Content"].to_dict()
    clean_texts = [text for text in makeshift.values() if text is not None]
    tfidf_matrix = vectorizer.fit_transform(clean_texts)

    similarity_matrix = cosine_similarity(tfidf_matrix)
    print(similarity_matrix)
