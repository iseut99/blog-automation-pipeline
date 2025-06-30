import pandas as pd
import re
import os

INPUT_PATH = 'data/incoming/titles.csv'
OUTPUT_PATH = 'data/processed/cleaned_titles.csv'

def clean_title(text):
    if not isinstance(text, str):
        return ""
    # Normalize encodings
    text = text.encode('latin1').decode('utf-8', errors='ignore')
    # Replace curly quotes and em-dashes
    text = text.replace('‚Äô', "'").replace('‚Äî', '—')
    # Fix title case for 'AI'
    text = re.sub(r'\bAi\b', 'AI', text)
    # Strip extra spaces and fix any weird unicode remnants
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_titles():
    if not os.path.exists(INPUT_PATH):
        print(f"❌ No input file found at: {INPUT_PATH}")
        return

    df = pd.read_csv(INPUT_PATH)

    if 'title' not in df.columns:
        print("❌ 'title' column missing in input file.")
        return

    df['cleaned_title'] = df['title'].apply(clean_title)
    df['status'] = 'cleaned'

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Cleaned titles written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    process_titles()
