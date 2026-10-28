import numpy as np
from gensim.models import Word2Vec

from preprocessing import get_preprocessed_questions
from tf_idf import tf_idf
from difficulty_level import difficulty_levels


preprocessed_questions = get_preprocessed_questions()
tfidf_matrix = tf_idf(preprocessed_questions)

word2vec_model = Word2Vec(
    preprocessed_questions,
    vector_size=300,
    window=5,
    min_count=1,
    workers=1,
    sg=0,
    seed=39,
    epochs=100,
)


def _weighted_question_embedding(question, weights):
    weighted_vectors = [
        (word2vec_model.wv[word], weights.get(word, 0.0))
        for word in question
        if word in word2vec_model.wv and weights.get(word, 0.0) > 0
    ]
    total_weight = sum(weight for _, weight in weighted_vectors)
    if not weighted_vectors or total_weight == 0:
        return np.zeros(word2vec_model.vector_size)
    return sum(vector * weight for vector, weight in weighted_vectors) / total_weight


word2vec_embeddings = [
    _weighted_question_embedding(question, {word: 1.0 for word in question})
    for question in preprocessed_questions
]
tfidf_wordEmb = [
    _weighted_question_embedding(question, weights)
    for question, weights in zip(preprocessed_questions, tfidf_matrix)
]
df_X_WE = [
    _weighted_question_embedding(question, difficulty_levels[index])
    for index, question in enumerate(preprocessed_questions)
]
word2vec_tfidf_dl_embeddings = [
    _weighted_question_embedding(
        question,
        {
            word: weights.get(word, 0.0) * difficulty_levels[index].get(word, 1.0)
            for word in question
        },
    )
    for index, (question, weights) in enumerate(zip(preprocessed_questions, tfidf_matrix))
]
