from gensim.models import Word2Vec
import pandas as pd
import numpy as np
from ast import literal_eval
from itertools import combinations
from scipy.spatial.distance import cosine
import os
import pickle

# Compute average pairwise cosine distance for a list of embeddings
def average_pairwise_distance(embeddings):
    # Get all 10 combinations of 5 embeddings taken 2 at a time
    pairs = list(combinations(embeddings, 2))
    distances = [cosine(e1, e2) for e1, e2 in pairs]
    return np.mean(distances)

# Compute instability score for a subreddit
def compute_instability(models, name):
    embeddings = [model.wv[word] for model in models]
    avg_distance = average_pairwise_distance(embeddings)
    return [avg_distance, '_'.join(sorted([name,name]))]

# Load vocabulary from file
with open("vocab.txt", "r", encoding="utf-8") as f:
    vocab_words = set(line.strip() for line in f)

#Set data directory
root = os.path.join(".", "preprocessed")
save = os.path.join(".", "embeddings")
basline_dir = os.path.join(".", "baseline")

for file in os.listdir(root):
    path = os.path.join(root, file)
    out = os.path.join(save, file) + '.bin'

    models = []

    df = pd.read_csv(os.path.join(root,file),sep='\t',names=['text'],converters={'text': literal_eval})
    tokens = df['text'].to_list()

    # Create 5 independent models for each subreddit
    for i in range(5):
        model = Word2Vec(sentences=tokens,vector_size=100,window=5,min_count=10,sg=1,seed=42)
        models.append(model)
    
    avg_embeddings = {}

    # Build averaged embedding for words in shared vocabulary
    for word in vocab_words:
        embeddings = [model.wv[word] for model in models]
        avg_vector = np.mean(embeddings, axis=0)
        avg_embeddings[word] = avg_vector
    
    with open(os.path.join(save,file) + '.pkl', "wb") as f:
        pickle.dump(avg_embeddings, f)
    
    corpus_baseline = []
    for word in vocab_words:
        corpus_baseline.append(compute_instability(models, file.split('.')[0].lower()))
    df = pd.DataFrame(corpus_baseline, columns = ["Distance", "Compared"])
    df.to_csv(os.path.join(basline_dir,file),index=False,header=True)
    with open(os.path.join(basline_dir,file) + '.pkl',"wb") as f:
        pickle.dump(corpus_baseline, f)
