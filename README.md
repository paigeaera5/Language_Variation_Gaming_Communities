# Exploring Language Variation in Gaming Communities

The purpose of this code is to conduct an experiment to address the following research question:

> *Do gaming communities on Reddit develop distinct linguistic patterns that are independent of traditional geographic dialects?*

## Data

The data this project works with are gaming and geographically-based communities. Specifically, these communities are made up of the following subreddits:

- Gaming: r/Pokemon_comments, r/Minecraft_comments, and r/leagueoflegends_comments

- Geographic: r/florida_comments, r/California_comments, r/london_comments, r/Birmingham_comments, r/sydney_comments, and r/melbourne_comments

The geographic subreddits were selected for the 3 main English dialects: American, British, and Australian. Each is provided with two different geographically-based subreddits to account for variation.

### How to download

To get the data, which will be zst files, you can follow [this guide](https://www.reddit.com/r/pushshift/comments/1itme1k/separate_dump_files_for_the_top_40k_subreddits/). Here are the basic steps that can be found in this guide:

1. Go to the [torrent link](https://academictorrents.com/details/1614740ac8c94505e4ecb9d88be8bed7b6afddd4) and click download.
2. Before opening the torrent file, you will need to download a [torrent client](https://transmissionbt.com/download). This client will allow you to only download the subreddit data required, rather than all 3.28 TB.
   > Note: If you are downloading the Windows version, I recommend downloading the qt version.
3. Now, open the torrent file you downloaded. This should launch in the torrent client. From here, deselect all files and go through checking off only the required subreddits.

After this, you will have the necessary zst files to continue this experiment.

## Running the Code

This code is compiled of my own code, along with a github repository dependency.

### Using the PushshiftDumps dependency

This experiment utilizes 2 files from this [dependency](https://github.com/Watchful1/PushshiftDumps.git), ***filter_file.py*** and ***to_csv.py***

1. ```filter_file.py```
   - This is used to gather more current comments from each subreddit given a specific time window (January 2022 to December 2024). This is done by changing the following variables to match the time window:
     ```
     from_date = datetime.strptime("2022-01-01", "%Y-%m-%d")
     to_date = datetime.strptime("2030-12-31", "%Y-%m-%d")
     ```
   - The `output_format` variable also needs to be changed from `'csv'` to `'zst'`
   - This file needs to run independently for each subreddit data. For each change the following variables need to be updated accordingly:
     ```
     input_file = r"\\MYCLOUDPR4100\Public\reddit\subreddits23\wallstreetbets_submissions.zst"
     output_file = r"\\MYCLOUDPR4100\Public\output"
     ```
2. `to_csv.py`
   - This is used to covert the time constricted data saved from `filter_file.py`
   - This file also needs to run independently for each zst file. For each run, change the following variables accordingly:
     ```
     input_file_path = r"\\MYCLOUDPR4100\Public\tools\PushshiftDumps\Straight-Wrap-172_submissions.zst"
     output_file_path = r"\\MYCLOUDPR4100\Public\Straight-Wrap-172_submissions.csv"
     ```
### Using the files in script
The purpose of these files, as well as the order it should be ran in is as follows:

1. `create_corpora.py`: Create a corpus for each gaming subreddit and English dialect. These dialectal corpora are the concatination between the two geographically-based subreddits.
   - The following line of code will need to be updated based on where you saved the csv files:
     ```root = r".\data_full"```
     
2. `preprocess.py`: Apply standard preprocessing techniques to each corpora to ensure consistency.
3. `create_vocab.py`: Create a vocabulary to be used for all cosine distance measurements. This vocabulary consists of words shared between all corpora.
   > Note: Vocab counts are printed for each corpus as a dictionary. After this, the shared vocabulary size is printed.
4. 'create_embeddings.py`: 5 independent models are created for each subreddit. These models are used to build an average embedding for words in the shared vocabulary.
   > Note: Corpus baselines are also measured and saved in this file by finding the average cosine distance between the 5 models.
5. `measure_distance.py`: Cosine differences are found both between (game vs game) and across (game vs geo) community types.
   > Note: Scatterplots are created and saved to display the distances measured within, between, and across community types.
