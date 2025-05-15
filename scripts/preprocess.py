import os
import re
import pandas as pd
from nltk.corpus import stopwords
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize

# Preprocessed using standard techniques: tokenization, lowercasing, and removal of usernames, URLs, and subreddit-specific markup

def preprocess(text):
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Remove usernames and subreddit references
    text = re.sub(r'u\/\w+', '', text)         # user mentions
    text = re.sub(r'r\/\w+', '', text)         # subreddit mentions

    # Remove Reddit markup
    text = re.sub(r'>.*\n?', '', text)         # blockquotes
    text = re.sub(r'\*{1,2}|\_{1,2}|\~{2}', '', text)  # bold, italics, strikethrough

    # Remove non-alphanumeric chars (keep basic punctuation)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Lowercase
    text = text.lower()

    # Remove stopwords
    stopwords_list = set(stopwords.words('english'))
    text = " ".join([word for word in str(text).split() if word not in stopwords_list])

    text = text.strip()

    # Tokenize using spaCy
    tokens = word_tokenize(text)

    return tokens

if __name__ == "__main__":
    root = r".\data"
    files = [file for file in os.listdir(root) if file.endswith(".csv")]

    output_dir = r".\preprocessed"

    for file in files:
        print(file)
        df = pd.read_csv(os.path.join(root,file),sep='\t',names=['text'])
        df['text'] = df['text'].apply(preprocess)
        df.to_csv(os.path.join(output_dir,file),index=False,header=False)