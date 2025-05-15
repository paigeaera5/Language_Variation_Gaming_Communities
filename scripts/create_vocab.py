import os
import pandas as pd
from ast import literal_eval
import gensim

min_count = 100
max_count = 10000

def trim_rule(word, count, min_count):
    return count > max_count  # Remove words with count greater than max_count

if __name__ == "__main__":
    root = r".\preprocessed"
    files = [file for file in os.listdir(root) if file.endswith(".csv")]

    vocabs = []
    limited_counts = {}

    for file in files:
        df = pd.read_csv(os.path.join(root,file),sep='\t',names=['text'],converters={'text': literal_eval})
        tokens = df['text'].to_list()

        model = gensim.models.Word2Vec(min_count=min_count)
        model.build_vocab(tokens, trim_rule=trim_rule)
        limited_counts[file] = len(model.wv.index_to_key)
        print(len((model.wv.index_to_key)),file)

        vocabs.append(set(model.wv.index_to_key))

    shared_vocab = vocabs[0]

    for vocab in vocabs[1:]:
        shared_vocab = shared_vocab & vocab
    
    print('Limited vocab counts:\n',limited_counts)
    print('Shared vocab:', len(shared_vocab))
    
    with open("vocab.txt", "w", encoding="utf-8") as f:
        for word in shared_vocab:
            f.write(word + "\n")