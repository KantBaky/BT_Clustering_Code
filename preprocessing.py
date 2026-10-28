import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
import nltk
import spacy
from openpyxl import load_workbook
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import re
import mysql.connector
import os
import time

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Default placeholders (avoid network/DB access at import)
preprocessed_questions = []
bloom_keywords = []
adverbs = []
bt_verbs = []
worksheet_bt_keywords = []
preprocessed_question_pos_tags = []
_last_dataset_key = None

# Helper functions for dataset selection
def _get_selected_dataset_name():
    """Return the requested worksheet name, defaulting to FBF."""
    dataset_name = (os.environ.get('BLOOM_DATASET') or 'FSC').strip().upper() # switch between FSC, FAS, FBF & FEGT for datasets
    supported_datasets = {'FSC', 'FAS', 'FBF', 'FEGT'}
    if dataset_name not in supported_datasets:
        raise ValueError(
            f"Unsupported BLOOM_DATASET '{dataset_name}'. Choose one of {sorted(supported_datasets)}."
        )
    return dataset_name

def _get_external_data():
    """Load questions and BT keywords from the local workbook, plus DB keywords/adverbs.
    This is done lazily to avoid network calls during module import.
    Returns: (questions, bloom_keywords, adverbs)
    """
    questions = []
    kws = []
    advs = []

    dataset_name = _get_selected_dataset_name()

    # Read questions, levels, and worksheet BT keywords from columns E:H.
    try:
        workbook_path = os.path.join(os.path.dirname(__file__), '20_01_2022_dataset.xlsx')
        workbook = load_workbook(workbook_path, read_only=True, data_only=True)
        try:
            if dataset_name not in workbook.sheetnames:
                raise ValueError(f"Worksheet '{dataset_name}' not found in '{workbook_path}'.")
            worksheet = workbook[dataset_name]
            questions = [
                {
                    'text': str(question),
                    'level': level or '',
                    'bt_keywords': [
                        keyword.strip()
                        for keyword in str(worksheet_keywords or '').split(',')
                        if keyword.strip()
                    ],
                }
                for question, level, _, worksheet_keywords in worksheet.iter_rows(
                    min_row=2, min_col=5, max_col=8, values_only=True
                )
                if question is not None and str(question).strip()
            ]
        finally:
            workbook.close()
    except Exception as e:
        print("Warning: failed to load local Excel data:", e)

    if not questions:
        raise RuntimeError(
            f"Unable to load questions for worksheet '{dataset_name}' from the local Excel workbook. "
            "Check that the workbook and selected worksheet are available."
        )

    # Load DB-backed bloom keywords and adverbs with retries and timeout
    try:
        last_exc = None
        for attempt in range(3):
            try:
                mydb = mysql.connector.connect(host="localhost", user="root", password="", database="bloom_taxonomy", connection_timeout=5)
                mycursor = mydb.cursor()
                mycursor.execute("SELECT keywords FROM bloom_keywords")
                bt_word = mycursor.fetchall()
                kws = [item[0] for item in bt_word]

                mycursor1 = mydb.cursor()
                mycursor1.execute("SELECT adverbs FROM adverbs_table")
                adv = mycursor1.fetchall()
                advs = [item[0] for item in adv]
                last_exc = None
                break
            except Exception as e:
                last_exc = e
                time.sleep(2 ** attempt)
        if last_exc is not None:
            print("Warning: failed to load DB data after retries:", last_exc)
    except Exception as e:
        print("Warning: failed to initialize DB client:", e)

    return questions, kws, advs


def get_preprocessed_questions(force_reload=False):
    """Return preprocessed questions, reusing only the current process's result.

    Parameters:
    - force_reload: if True, reload the workbook and database data.
    """
    global preprocessed_questions, bloom_keywords, adverbs, bt_verbs
    global worksheet_bt_keywords, preprocessed_question_pos_tags, _last_dataset_key

    selected_dataset = _get_selected_dataset_name()
    if _last_dataset_key != selected_dataset:
        preprocessed_questions = []
        bloom_keywords = []
        adverbs = []
        bt_verbs = []
        worksheet_bt_keywords = []
        preprocessed_question_pos_tags = []
        _last_dataset_key = selected_dataset

    if not force_reload and preprocessed_questions:
        return preprocessed_questions

    questions, bloom_keywords, adverbs = _get_external_data()

    if questions:
        worksheet_bt_keywords = [
            question['bt_keywords'] for question in questions
        ]
        processed_questions = [
            _preprocess_question_with_tags(
                question['text'], question['bt_keywords']
            )
            for question in questions
        ]
        preprocessed_questions = [tokens for tokens, _ in processed_questions]
        preprocessed_question_pos_tags = [
            tagged_tokens for _, tagged_tokens in processed_questions
        ]
        bt_verbs = [
            bt_keywords(question['text'], question['bt_keywords'])
            for question in questions
        ]
    else:
        preprocessed_questions = []
        bt_verbs = []
        worksheet_bt_keywords = []
        preprocessed_question_pos_tags = []

    return preprocessed_questions

# WH-Question words
wh_question_words = ["who", "what", "where", "when", "why", "how"]

# Preprocessing function
def preprocess_question(question, required_keywords=None):
    tokens, _ = _preprocess_question_with_tags(question, required_keywords)
    return tokens


def _preprocess_question_with_tags(question, required_keywords=None):
    required_keywords = required_keywords or []
    keyword_set = {keyword.lower() for keyword in bloom_keywords}
    keyword_set.update(keyword.lower() for keyword in required_keywords)
    preserved_words = {
        word.lower()
        for keyword in required_keywords
        for word in re.findall(r"[A-Za-z]+", keyword)
    }

    # Definition of a regular expression pattern to match words
    question = re.sub(r'\(([^)]*)\)', r'\1', question) 

    # Remove names, Process the text with spaCy
    doc = nlp(question)
    # Extract named entities
    for ent in doc.ents:
        for key in ent.text.split():
            if key.lower() in keyword_set:
                question = ''.join(key) + question.replace(ent.text,'')
            else:
                question = question.replace(ent.text,'')

    # Remove everything preceding bt-keywords except adverbs
    question = ''.join(getImpSentence(question, required_keywords))

    # Tokenization and sentence segmentation
    sentences = sent_tokenize(question)

    selected_sentences = [] 

    for sentence in sentences:
        # Check if the sentence contains any Bloom's Taxonomy keywords
        if any(keyword in sentence.lower() for keyword in keyword_set):
                selected_sentences.append(sentence)

    # Combine selected sentences into a single text
    selected_text = ' '.join(selected_sentences)
    
    # Tag original tokens before lowercasing or removing stop words.
    tokens = word_tokenize(selected_text)
    tagged_tokens = nltk.pos_tag(tokens)
       
    # Normalize tokens and remove stopwords, punctuation, and remaining numbers.
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = []
    lemmatized_tagged_tokens = []

    for token, tag in tagged_tokens:
        word = token.lower()
        if (
            word not in wh_question_words
            and word not in preserved_words
            and (word in stop_words or not word.isalpha())
        ):
            continue
        if word in preserved_words or word.endswith('ss'):
            lemma = word
        else:
            lemma = lemmatizer.lemmatize(word, get_wordnet_pos(tag))
        lemmatized_tokens.append(lemma)
        lemmatized_tagged_tokens.append((lemma, tag))
    
    return lemmatized_tokens, lemmatized_tagged_tokens

# Helper function to map POS tags to WordNet POS tags for lemmatization
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return 'a'  # Adjective
    elif treebank_tag.startswith('V'):
        return 'v'  # Verb
    elif treebank_tag.startswith('N'):
        return 'n'  # Noun
    elif treebank_tag.startswith('R'):
        return 'r'  # Adverb
    else:
        return 'n'  # Default to noun
    
# Function to remove words preceding bt words
def getImpSentence(question, required_keywords=None):
    # Initialize a list to store modified questions
    modified_questions = []
    
    # Iterate through each question and process it
    words = question.split()
    bloom_keyword_set = {keyword.lower() for keyword in bloom_keywords}
    bloom_keyword_set.update(keyword.lower() for keyword in (required_keywords or []))
    required_keyword_set = {keyword.lower() for keyword in (required_keywords or [])}
    adverb_set = {adverb.lower() for adverb in adverbs}
    matching_required_indices = [
        word_index for word_index, word in enumerate(words)
        if word.lower() in required_keyword_set
    ]
    trigger_indices = matching_required_indices or [
        word_index for word_index, word in enumerate(words)
        if word.lower() in bloom_keyword_set
    ]
    for word_index in trigger_indices:
        word = words[word_index]

        modified_question = ''
        if word_index != 0 and (
            words[word_index - 1].lower() != 'to'
            or word.lower() in required_keyword_set
        ):

            # Check if there is any adverb preceding the trigger word
            preceding_words = words[:word_index]
            adverb_present = ""
            for preceding_word in preceding_words:
                if preceding_word.lower() in adverb_set:
                    adverb_present = preceding_word

            if adverb_present:

                # If there is an adverb, keep it in the modified question
                modified_question = ' '.join(words[preceding_words.index(adverb_present):])
            else:
                # If there is no adverb, remove everything before the trigger word
                modified_question = ' '.join(words[word_index:])

        elif word_index == 0:
            modified_question = ' '.join(words[word_index:])
        else:
            continue

        modified_questions.append(modified_question)
        break  # Stop searching for trigger words in this question

    return modified_questions

# Picking up bloom taxonomy keywords
def bt_keywords(question, worksheet_keywords=None):
    """Return worksheet BT keywords that occur in the original question."""
    keywords = worksheet_keywords
    if keywords is None:
        keywords = bloom_keywords

    return [
        keyword
        for keyword in keywords
        if re.search(
            r'(?<!\w)' + re.escape(keyword) + r'(?!\w)',
            question,
            flags=re.IGNORECASE,
        )
    ]


# Preprocessing is performed lazily by calling `get_preprocessed_questions()`.
# This avoids network/DB access during module import.

# print("\033[4;1;3mPreprocessed Questions:\033[0m")
# # Print the preprocessed questions
# for i, tokens in enumerate(get_preprocessed_questions()):
#     expected_bt = worksheet_bt_keywords[i]
#     detected_bt = bt_verbs[i]
#     matches_worksheet = detected_bt == expected_bt
#     preserved_bt = bt_keywords(' '.join(tokens), expected_bt)
#     keywords_preserved = preserved_bt == detected_bt
#     print(f"Question {i + 1}: {' '.join(tokens)}")
#     print(
#         f"\033[0;0;1mBT keywords:\033[0m \033[0;1;3m{', '.join(expected_bt)}\033[0m"
#     )
#     print(
#         f"Detected BT keywords: {', '.join(detected_bt)} "
#         f"| Worksheet match: {'YES' if matches_worksheet else 'NO'}"
#     )
#     print(
#         f"BT keywords retained after preprocessing: {', '.join(preserved_bt)} "
#         f"| Preserved: {'YES' if keywords_preserved else 'NO'}"
#     )
