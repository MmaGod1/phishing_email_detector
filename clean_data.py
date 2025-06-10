import os
import re
import pandas as pd
from pathlib import Path
import csv
import sys

# Allow very large fields in CSV
csv.field_size_limit(sys.maxsize)

DATA_DIR = Path("./data")
OUTPUT_DIR = DATA_DIR / "cleaned"
OUTPUT_DIR.mkdir(exist_ok=True)

url_pattern = re.compile(r'https?://\S+')

def clean_email_body(text):
    if pd.isnull(text):
        return "", ""
    urls = url_pattern.findall(text)
    text_no_urls = url_pattern.sub('', text)
    clean_text = ' '.join(text_no_urls.split())
    return clean_text, ', '.join(urls)

def get_column_mapping(df):
    text_col = None
    label_col = None
    
    for col in df.columns:
        lower = col.lower().strip()
        if lower in ['body', 'email text', 'message', 'text_combined']:
            text_col = col
        if lower in ['label', 'email type', 'category', 'type']:
            label_col = col
    return text_col, label_col

def process_file(filepath):
    try:
        df = pd.read_csv(filepath, encoding='utf-8', engine='python')
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding='latin1', engine='python')
        return

    text_col, label_col = get_column_mapping(df)
    
    if not text_col or not label_col:
        print(f"⚠️ Skipping {filepath.name} (no text/label column)")
        return

    df = df[[text_col, label_col]].copy()
    df.columns = ['body', 'label']  # Standardize names

    # Clean body and extract URLs
    df['body_clean'], df['urls_extracted'] = zip(*df['body'].map(clean_email_body))

    output_file = OUTPUT_DIR / filepath.name.replace(".csv", "_cleaned.csv")
    df.to_csv(output_file, index=False)
    print(f"✅ Cleaned: {filepath.name} → {output_file.name}")

# Process all CSVs in ./data
for csv_file in DATA_DIR.glob("*.csv"):
    process_file(csv_file)
