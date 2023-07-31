from collections import Counter
from operator import itemgetter

def keyword_search(reviews, keywords, property_name):
    if not reviews:
        return []

    keyword_counts = []
    for review in reviews:
        text = review.text
        count = Counter(text.split())
        keyword_count = sum(count[k] for k in keywords if k in count)
        keyword_counts.append((review, keyword_count))
    sorted_reviews = sorted(keyword_counts, key=itemgetter(1), reverse=True)
    top_reviews = [r for r, _ in sorted_reviews[:10]]
    return top_reviews