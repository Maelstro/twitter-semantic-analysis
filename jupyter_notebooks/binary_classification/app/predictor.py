import re
import pickle
import nltk
nltk.download('wordnet')
import gensim
from nltk.stem import WordNetLemmatizer

class ArchetypePredictor(object):
    def __init__(self):
        # Models
        self._artist_model = self._load_pickle("../models/artist_svm.pickle")
        self._caregiver_model = self._load_pickle("../models/caregiver_svm.pickle")
        self._everyman_model = self._load_pickle("../models/everyman_svm.pickle")
        self._explorer_model = self._load_pickle("../models/explorer_svm.pickle")
        self._guru_model = self._load_pickle("../models/guru_svm.pickle")
        self._hero_model = self._load_pickle("../models/hero_svm.pickle")
        self._innocent_model = self._load_pickle("../models/innocent_svm.pickle")
        self._jester_model = self._load_pickle("../models/jester_svm.pickle")
        self._magician_model = self._load_pickle("../models/magician_svm.pickle")
        self._rebel_model = self._load_pickle("../models/rebel_svm.pickle")
        self._ruler_model = self._load_pickle("../models/ruler_svm.pickle")
        self._seducer_model = self._load_pickle("../models/seducer_svm.pickle")

        # Vectorizer
        self._vectorizer = self._load_pickle("../models/tfidf_vectorizer.pickle")

    def _lemmatize(self, text: str) -> str:
        """Lemmatizes a given text."""
        return WordNetLemmatizer().lemmatize(text, pos='v')

    def _preprocess_single_tweet(self, text: str) -> list:
        # Lowercase the tweets
        lc_text = text.lower()

        # Regex patterns
        url_pattern = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
        user_pattern = '@[^\s]+'
        alpha_pattern = "[^a-zA-Z]"
        sequence_pattern = r"(.)\1\1+"
        seq_replace_pattern = r"\1\1"

        # Remove URLs from the tweet text
        lc_text = re.sub(url_pattern, ' ', lc_text)

        # Remove username from the tweet text
        lc_text = re.sub(user_pattern, ' ', lc_text)

        # Remove all non-alphanumeric symbols
        lc_text = re.sub(alpha_pattern, ' ', lc_text)

        # Replace all 3 or more consecutive letters with 2 letters
        lc_text = re.sub(sequence_pattern, seq_replace_pattern, lc_text)

        processed_text = []
        for word in lc_text.split():
            word = self._lemmatize(word)
            processed_text.append(word)

        return processed_text

    def _load_pickle(self, file_path: str):
        """
        Loads a pickled object.

        :param file_path: Path to file to load
        :return: Unpickled model
        """
        with open(file_path, "rb") as f:
            obj = pickle.load(f)
        return obj

    def _vectorize_input(self, preprocessed_text: list):
        transformed_text = self._vectorizer.transform(preprocessed_text)
        return transformed_text

    def _predict_with_probability(self, text, archetype_name: str):
        # Select an archetype
        case = {
            "artist": self._artist_model,
            "caregiver": self._caregiver_model,
            "everyman": self._everyman_model,
            "explorer": self._explorer_model,
            "guru": self._guru_model,
            "hero": self._hero_model,
            "innocent": self._innocent_model,
            "jester": self._jester_model,
            "magician": self._magician_model,
            "rebel": self._rebel_model,
            "ruler": self._ruler_model,
            "seducer": self._seducer_model
        }
        pred = case[archetype_name].predict(text)
        class_prob = case[archetype_name].predict_proba(text)[int(pred)]

        return (int(pred), class_prob[int(pred)])

    def classify_to_archetype(self, text: str, archetype: str):
        # Text preprocessing and vectorization
        processed_text = self._preprocess_single_tweet(text)
        transformed_text = self._vectorize_input(processed_text)

        return self._predict_with_probability(transformed_text, archetype)

    def classify_all(self, text):
        archetype_list = ['artist',
                          'caregiver',
                          'everyman',
                          'explorer',
                          'guru',
                          'hero',
                          'innocent',
                          'jester',
                          'magician',
                          'rebel',
                          'ruler',
                          'seducer']

        # Text preprocessing and vectorization
        processed_text = self._preprocess_single_tweet(text)
        transformed_text = self._vectorize_input(processed_text)
        archetype_preds = {}

        for archetype in archetype_list:
            (pred, pred_prob) = self._predict_with_probability(transformed_text, archetype)
            archetype_preds.update({archetype: {f"is_{archetype}": pred, "probability": pred_prob}})

        return archetype_preds