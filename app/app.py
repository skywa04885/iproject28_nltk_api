import nltk
import string
from flask import Flask, request, jsonify
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


def nltk_pos_tagger(nltk_tag: str) -> str:
    """
    Gets the position of the word in a sentence based on a previously given tag.
    """

    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


# All of the following dependencies are required for the proper preparation steps.
nltk_dependencies = [
    'punkt',
    'wordnet',
    'averaged_perceptron_tagger',
    'stopwords',
]

# Downloads all the NLTK dependencies.
for dependency in nltk_dependencies:
    nltk.download(dependency)

# Loads the stopwords for the english language.
stopwords = nltk.corpus.stopwords.words('english'),

# Creates the word net lemmatizer.
lemmatizer = WordNetLemmatizer()

# Creates the flask app.
app = Flask(__name__)


@app.route("/prepare")
def prepare():
    """
    Prepares the text present in the request query and sends the counted tokens as response.
    """

    # Gets the query text and makes sure the text has been specified in the query.
    text = request.args.get("text")
    if text is None:
        return "Text argument has to be specified!", 400

    # Makes the text lowercase, since the case doesn't really matter.
    text = text.lower()

    # Removes all the punctuation from the string since this has little meaning.
    text = "".join([c for c in text if c not in string.punctuation])

    # Tokenizes all the words.
    tokens = nltk.word_tokenize(text)

    # Tags all the tokens with their position in the sentence.
    tokens = nltk.pos_tag(tokens)

    # Transforms the tagged tokens so that the tag gets turned into a sentence position
    #  for the wordnet lemmatizer.
    tokens = [(word, nltk_pos_tagger(tag)) for word, tag in tokens]

    # Lemmatizes all the tokens if possible.
    tokens = [lemmatizer.lemmatize(
        word, pos=pos) if pos is not None else word for word, pos in tokens]

    # Remove all the stopwords from the tokens since these add little to nothing to
    #  the meaning of the sentence.
    tokens = [
        token for token in tokens if token not in stopwords and len(token) > 2]

    # Removes all the duplicate words, but count them so we know how many we have.
    counted_tokens = Counter(tokens)

    # Returns the JSON response of the counted tokens.
    return jsonify(
        counted_tokens
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
