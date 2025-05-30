import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

#  Pastikan resource NLTK sudah diunduh di luar modul ini (misal di main.py)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text: str) -> str:
    """
    Membersihkan teks: lowercase, hapus simbol, tokenisasi, stopword removal, lemmatization.
    """
    # Lowercaseya, 
    text = text.lower()
    # Hapus karakter non-alfabet
    text = re.sub(r'[^a-z\s]', '', text)
    # Tokenisasi
    tokens = word_tokenize(text)
    # Stopword removal dan lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    # Gabungkan kembali
    return ' '.join(tokens)
