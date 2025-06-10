import sys
import joblib
import nltk
import string
import os

# Add the local nltk_data path (relative to this script)
project_nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
nltk.data.path.append(project_nltk_data_path)

# Try loading stopwords without downloading from the internet
try:
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
except LookupError:
    print("[!] NLTK 'stopwords' resource not found. Make sure it's in ./nltk_data/corpora/stopwords/")
    sys.exit(1)

# Preprocess text
def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens).strip()

def main():
    if len(sys.argv) != 2:
        print("Usage: python phishing_detector.py <path_to_email_text_file>")
        sys.exit(1)

    email_file = sys.argv[1]
    if not os.path.isfile(email_file):
        print(f"❌ Error: File not found -> {email_file}")
        sys.exit(1)

    # Load model and vectorizer
    model = joblib.load('model/phishing_model.pkl')
    vectorizer = joblib.load('model/vectorizer.pkl')

    # Read email content
    with open(email_file, 'r', encoding='utf-8') as file:
        email_content = file.read()

    # Preprocess and vectorize
    processed_text = preprocess_text(email_content)
    features = vectorizer.transform([processed_text])

    # Predict and output
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features)[0]

    print(f"\n📧 The email is classified as: **{prediction.upper()}**")
    print(f"🔎 Confidence - Phishing: {confidence[list(model.classes_).index('phishing')]:.2f}, Safe: {confidence[list(model.classes_).index('safe')]:.2f}")

if __name__ == "__main__":
    main()

