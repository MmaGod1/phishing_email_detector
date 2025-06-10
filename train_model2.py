import pandas as pd
import nltk
import string
import joblib
import os
import glob

from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# Ensure NLTK stopwords are available
nltk.data.path.append("./nltk_data")

# Download stopwords if not already downloaded
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords', download_dir='./nltk_data')

# Preprocessing function
def preprocess_text(text):
    if pd.isnull(text):
        return ""
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)

# Load and combine all valid CSV files
data_dir = './data/cleaned'
all_files = glob.glob(os.path.join(data_dir, '*.csv'))

combined_df = pd.DataFrame()

for file in all_files:
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        if 'body' in df.columns and 'label' in df.columns:
            df = df[['body', 'label']].dropna()
            df['label'] = df['label'].astype(str).str.strip().str.lower()  # ✅ Normalize labels
            combined_df = pd.concat([combined_df, df], ignore_index=True)
            print(f"✅ Loaded: {file} (rows: {len(df)})")
        else:
            print(f"  Skipped: {file} (missing 'body' or 'label')")
    except Exception as e:
        print(f"❌ Failed to load {file}: {e}")

if combined_df.empty:
    print("🚫 No valid data found. Exiting.")
    exit()

# Final normalization (in case)
combined_df['label'] = combined_df['label'].astype(str).str.strip().str.lower()

label_mapping = {
    '1': 'phishing',
    'phishing email': 'phishing',
    '0': 'safe',
    'safe email': 'safe'
}

combined_df['label'] = combined_df['label'].map(label_mapping)
combined_df = combined_df.dropna(subset=['label'])  # remove rows with unmapped labels

print("✅ Final labels:", combined_df['label'].unique())




# Optional: print unique labels to verify consistency
print("🔍 Unique labels:", combined_df['label'].unique())

# Preprocess body text
combined_df['processed_text'] = combined_df['body'].apply(preprocess_text)

# TF-IDF vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(combined_df['processed_text'])
y = combined_df['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("📊 Model Evaluation:")
print(classification_report(y_test, y_pred))

# Save model and vectorizer
os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/phishing_model.pkl')
joblib.dump(vectorizer, 'model/vectorizer.pkl')

print("✅ Model and vectorizer saved to 'model/' directory.")

