from flask import Flask, request, render_template, render_template_string
from flask_caching import Cache
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 300})  # Cache for 5 minutes

SUPPORTED_LANGUAGES = {
    "ar": "arabic", "bg": "bulgarian", "cs": "czech", "de": "german", "el": "greek",
    "en": "english", "es": "spanish", "et": "estonian", "fi": "finnish", "fr": "french",
    "he": "hebrew", "hu": "hungarian", "id": "indonesian", "it": "italian", "ja": "japanese",
    "ko": "korean", "lt": "lithuanian", "lv": "latvian", "nl": "dutch", "pl": "polish",
    "pt": "portuguese", "ro": "romanian", "ru": "russian", "sk": "slovak", "sl": "slovenian",
    "sv": "swedish", "tr": "turkish", "uk": "ukrainian", "zh": "chinese"
}

@app.route('/')
def home():
    return render_template("index.html")

def extract_text(url):
    """Extracts article text and detects language using Newspaper3k."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.title, article.text, article.meta_lang
    except Exception as e:
        return None, None, str(e)

def summarize_text(text, lang, num_sentences):
    """Summarizes extracted text using LexRank."""
    lang_code = SUPPORTED_LANGUAGES.get(lang, "english")
    parser = PlaintextParser.from_string(text, Tokenizer(lang_code))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return [str(sentence) for sentence in summary]

@app.route('/summarize', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def summarize_url():
    url = request.args.get('url')
    if not url:
        return "<h3>Error: URL parameter is required</h3>", 400

    num_sentences = request.args.get("sentences", 3, type=int)
    num_sentences = max(1, min(num_sentences, 10))

    title, text, lang = extract_text(url)
    if not text:
        return "<h3>Error: Failed to extract content</h3>", 500

    summary = summarize_text(text, lang, num_sentences)
    word_count = len(text.split())

    summary_html = """
    <h2>Summary for: <a href="{{ url }}" target="_blank">{{ title }}</a></h2>
    <p><strong>Language:</strong> {{ lang }}</p>
    <p><strong>Word Count:</strong> {{ word_count }}</p>
    <p><strong>Summary Length:</strong> {{ num_sentences }} sentences</p>
    <div class="summary">
        <h3>Summary:</h3>
        <ul>
            {% for sentence in summary %}
                <li>{{ sentence }}</li>
            {% endfor %}
        </ul>
    </div>
    """

    return render_template_string(summary_html, title=title, url=url, lang=lang, summary=summary, word_count=word_count, num_sentences=num_sentences)

if __name__ == '__main__':
    app.run(debug=True)
