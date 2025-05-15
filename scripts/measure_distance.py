import os
import random
import pickle
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from sklearn.metrics.pairwise import cosine_distances
from scipy.spatial.distance import cosine

def load_pkl(file):
    with open(file, "rb") as f:
        return pickle.load(f)

def calculate_average_cosine_distance(word, embeddings_1, embeddings_2, vocab):
    word_distances = []
    embeddings_1, type1 = embeddings_1
    embeddings_2, type2 = embeddings_2
    #print(type1,type2)

    if word in embeddings_1 and word in embeddings_2:
        # Get the embeddings from both corpora
        vec_1 = embeddings_1[word]
        vec_2 = embeddings_2[word]
        # Calculate cosine distance
        distance = cosine(vec_1, vec_2)
        word_distances.append(distance)
    
    return [distance,'_'.join([type1.lower(),type2.lower()])]

def same_type_distances(embeddings, vocab):
    distances = []

    for i in range(len(embeddings)-1):
        for j in range(i+1,len(embeddings)):
            for word in vocab:
                distances.append(calculate_average_cosine_distance(word,embeddings[i],embeddings[j],vocab))
    
    return distances

def cross_type_distances(main_embedding, embeddings, vocab):
    distances = []

    for i in range(len(embeddings)):
        for word in vocab:
            distances.append(calculate_average_cosine_distance(word,main_embedding,embeddings[i],vocab))
    
    return distances

if __name__ == "__main__":
    root = os.path.join('.','embeddings')
    files = [file for file in os.listdir(root) if file.endswith(".pkl")]

    save = os.path.join('.','distances')

    # Separate subreddits into types
    gaming = ['leagueoflegends','Minecraft','pokemon']
    geo = ['au','uk','us']

    # Retrieve vocabulary
    with open("vocab.txt", "r", encoding="utf-8") as f:
        vocab_words = set(line.strip() for line in f)
    
    # Retrieve all averaged embeddings from pickle files
    gaming_embeddings = []
    geo_embeddings = []

    # List to hold all DataFrames created to use for plotting
    dist_dfs = []

    for file in files:
        #with open(os.path.join(root,file), "rb") as f:
            embedding = load_pkl(os.path.join(root,file))
            if file.startswith(tuple(gaming)):
                print(file)
                gaming_embeddings.append((embedding,file.split('.')[0]))
            else:
                geo_embeddings.append((embedding,file.split('.')[0]))

    # Retrieve basline distances
    baselines = [file for file in os.listdir(os.path.join('.','baseline')) if file.endswith(".csv")]
    gaming_base = []
    geo_base = []
    for file in baselines:
        embedding = pd.read_csv(os.path.join('.','baseline',file))
        if file.startswith(tuple(gaming)):
            print(file)
            gaming_base.append(embedding)
        else:
            geo_base.append(embedding)

    # Calculate distance between community type
    gaming_dists = same_type_distances(gaming_embeddings,vocab_words)
    gaming_df = pd.DataFrame(gaming_dists, columns = ["Distance", "Compared"])
    gaming_df = gaming_df.assign(Color='blue')
    gaming_base_df = pd.concat(gaming_base)
    gaming_base_df = gaming_base_df.assign(Color='orange')
    dist_dfs.append(pd.concat([gaming_df, gaming_base_df]))

    geo_dists = same_type_distances(geo_embeddings,vocab_words)
    geo_df = pd.DataFrame(geo_dists, columns = ["Distance", "Compared"])
    geo_df = geo_df.assign(Color='blue')
    geo_base_df = pd.concat(geo_base)
    geo_base_df = geo_base_df.assign(Color='orange')
    dist_dfs.append(pd.concat([geo_df, geo_base_df]))

    # Calculate distances across community types
    # League vs geo
    league_embeddings = gaming_embeddings[0]
    assert league_embeddings[1].startswith('league')
    league_dists = cross_type_distances(league_embeddings, geo_embeddings, vocab_words)
    league_df = pd.DataFrame(league_dists, columns = ["Distance", "Compared"])
    league_df = league_df.assign(Color='green')
    dist_dfs.append(league_df)
    with open(os.path.join(save,'league') + '.pkl', "wb") as f:
        pickle.dump(league_dists, f)

    # Minecraft vs geo
    minecraft_embeddings = gaming_embeddings[1]
    assert minecraft_embeddings[1].lower().startswith('minecraft')
    minecraft_dists = cross_type_distances(minecraft_embeddings, geo_embeddings, vocab_words)
    minecraft_df = pd.DataFrame(minecraft_dists, columns = ["Distance", "Compared"])
    minecraft_df = minecraft_df.assign(Color='green')
    dist_dfs.append(minecraft_df)
    with open(os.path.join(save,'minecraft') + '.pkl', "wb") as f:
        pickle.dump(minecraft_dists, f)

    # Pokemon vs geo
    pokemon_embeddings = gaming_embeddings[2]
    assert pokemon_embeddings[1].lower().startswith('pokemon')
    pokemon_dists = cross_type_distances(pokemon_embeddings, geo_embeddings, vocab_words)
    pokemon_df = pd.DataFrame(pokemon_dists, columns = ["Distance", "Compared"])
    pokemon_df = pokemon_df.assign(Color='green')
    dist_dfs.append(pokemon_df)
    with open(os.path.join(save,'pokemon') + '.pkl', "wb") as f:
        pickle.dump(pokemon_dists, f)

    # Plot distances
    names = ['gaming','geo','league','minecraft','pokemon']

    for i in range(len(dist_dfs)):
        df = dist_dfs[i].dropna()
        figure(figsize=(10,5)) 
        ax = sns.stripplot(data=df, x="Compared", y="Distance", hue = "Color", jitter = True, size = 3)
        plt.xticks(rotation=45)
        ax.set_ylim([0, 1])
        plt.savefig(os.path.join('.','figs',names[i])+".png", bbox_inches = "tight")
        plt.clf()
