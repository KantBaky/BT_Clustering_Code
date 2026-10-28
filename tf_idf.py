# import required module
from collections import Counter
import math
import pandas as pd
pd.set_option('display.max_rows', 500)

# import preprocessing file (use lazy loader)
import preprocessing

# Load preprocessed questions via loader (may come from cache)
preprocessed_questions = preprocessing.get_preprocessed_questions()

def tf_idf(question_set):
    # set of questions
    questions = [' '.join(tokens) for tokens in question_set]

    # Tokenize the documents
    tokenized_questions = [doc.split() for doc in questions]

    # Create a list of unique terms
    unique_terms = sorted({word for doc in tokenized_questions for word in doc})
    term_counts = [Counter(doc) for doc in tokenized_questions]
    document_frequencies = Counter(
        term for doc in tokenized_questions for term in set(doc)
    )

    # Calculate inverse document frequency (IDF)
    total_questions = len(questions) 
    idf_matrix = [
        1 + math.log10(total_questions / document_frequencies[term])
        for term in unique_terms
    ]

    # Calculate TF-IDF scores from per-document token counts
    tfidf_matrix = []
    for i in range(total_questions):
        document_length = len(tokenized_questions[i])
        tfidf_row = {
            term: (term_counts[i].get(term, 0) / document_length * idf)
            if document_length else 0
            for term, idf in zip(unique_terms, idf_matrix)
        }
        tfidf_matrix.append(tfidf_row)
 
    return tfidf_matrix

if preprocessed_questions:
    tfidf = tf_idf(preprocessed_questions)

    # Getting the matrix X of the tfidf
    tfidf_X = [[value for value in dictionary.values()] for dictionary in tfidf]
else:
    tfidf = []
    tfidf_X = []

# list of words in the corpus
def word_list(document_list):   
    word_string = [' '.join(token) for token in document_list]
    combined_string = [doc.split() for doc in word_string]
    terms = sorted({word for doc in combined_string for word in doc})
    return terms

# Create a DataFrame to store the TF-IDF scores
try:
    tfidf_df = pd.DataFrame(data=tfidf_X, columns=word_list(preprocessed_questions))
except Exception:
    tfidf_df = pd.DataFrame()
# tfidf_df = pd.DataFrame(data=tf_idf_x(preprocessed_questions), columns=word_list(preprocessed_questions))

# print("\n\033[4;1;3mTF-IDF:\033[0m")
# # Display the DataFrame
# print(tfidf_df.T)