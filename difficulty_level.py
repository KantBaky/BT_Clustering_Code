import preprocessing
from tf_idf import tf_idf
import mysql.connector
import pandas as pd
pd.set_option('display.max_rows', 500)


# Load preprocessed questions and related data lazily
preprocessed_questions = preprocessing.get_preprocessed_questions()
bt_verbs = preprocessing.bt_verbs

# If no preprocessed questions are available, set empty defaults and skip heavy processing
if not preprocessed_questions:
    difficulty_levels = []
    tfidf_matrix = []
    tfidf_x_dif_lev = []
    tfidf_x_dif_lev_X = []
    df_list = []
    combined_df = pd.DataFrame()

else:
    # Flatten the nested list
    bt_keywords = [verb for sublist in bt_verbs for verb in sublist]
    bt_keywords_lower = {keyword.lower() for keyword in bt_keywords}
    _bloom_level_map = {
        'evaluation': 6,
        'synthesis': 5,
        'analysis': 4,
        'application': 3,
        'comprehension': 2,
        'knowledge': 1,
    }

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bloom_taxonomy",
        connection_timeout=5,
    )
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT `keywords`, `bloom_level` FROM `bloom_keywords`")
        bloom_level_by_keyword = {}
        for keyword, level in mycursor.fetchall():
            bloom_level_by_keyword.setdefault(
                keyword.lower(), _bloom_level_map.get(level)
            )
    finally:
        mydb.close()

    # Function to get the bloom taxonomy level of words
    def get_bloom_level(keyword):
        return bloom_level_by_keyword.get(keyword.lower())
    
    # Function to calculate the difficulty level of words
    def calculate_difficulty_level(word, pos_tag):
        if word.lower() in bt_keywords and pos_tag.startswith('VB'):
            return 5  # Verb
        elif pos_tag.startswith('MD') or pos_tag.startswith('VB'):
            return 3  # Non-Bloom's Taxonomy verbs or Supporting Verb (MD = modal verb)
        elif pos_tag.startswith(('NN', 'JJ', 'RB')):
            return 2  # Noun or Adjective or Adverb
        else:
            return 1  # Default

    def difficulty_levels_for_questions(questions):
        tagged_questions = preprocessing.preprocessed_question_pos_tags
        if len(tagged_questions) != len(questions):
            raise ValueError(
                "POS tags from preprocessing are not aligned with the questions."
            )

        difficulty_levels = []

        for tagged_tokens in tagged_questions:
            difficulty_level_for_question = {
                word: calculate_difficulty_level(word, pos)
                * (get_bloom_level(word) or 1)
                for word, pos in tagged_tokens
            }

            difficulty_levels.append(difficulty_level_for_question)

        return difficulty_levels


    # Get difficulty level of words
    difficulty_levels = difficulty_levels_for_questions(preprocessed_questions)

    # compute tf-idf
    tfidf_matrix = tf_idf(preprocessed_questions)
    terms = list(tfidf_matrix[0]) if tfidf_matrix else []

    # Multiply difficulty levels by TF-IDF scores 
    def tfidf_by_dif_lev(questions):

        multiplied_difficulty_levels = [
            {
                term: float(difficulty_levels[i].get(term, 0)) * tfidf_matrix[i][term]
                for term in terms
            }
            for i in range(len(questions))
        ]

        return multiplied_difficulty_levels

    tfidf_x_dif_lev = tfidf_by_dif_lev(preprocessed_questions)

    # Getting matrix X of the tfidf_x_dif_lev
    tfidf_x_dif_lev_X = [
        [tfidf_x_dif_lev[i].get(term, 0) for term in terms]
        for i in range(len(preprocessed_questions))
    ]

    # Create a list to store DataFrames
    df_list = []

    # Loop through each dictionary in tfidf_x_dif_lev
    for dictionary in tfidf_x_dif_lev:
        # Convert dictionary to DataFrame using keys as columns and values as data
        df = pd.DataFrame.from_dict(dictionary, orient='index', columns=['TF-IDF x Difficulty Level'])
        # Add the DataFrame to the list
        df_list.append(df)

    # Combine the DataFrames into a single DataFrame (guard if list empty)
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
    else:
        combined_df = pd.DataFrame()

# print("\n\033[4;1;3mTF-IDF x Difficulty Level:\033[0m")
# # Display the combined DataFrame
# print(combined_df.T)