import os
import pandas as pd

root = r".\data_full"
output_dir = r".\data"
files = [file for file in os.listdir(root) if file.endswith(".csv")]

min_score = 10  # minimum number of upvotes

# Get correct number of comments from each subreddit
for file in files:
    name, _ = file.split('.')
    df = pd.read_csv(os.path.join(root,file))
    print('\n',name,len(df['body']))
    df = df[df['score'] >= min_score]
    df = df.dropna()
    print(len(df))

    count = 50000 if name.lower().startswith(('league','minecraft','pokemon')) else 25000
    print(name.lower().startswith(('league','minecraft','pokemon')),name)
    selected_df = df['body'].sample(count)
    print(file,len(df['body']))
    selected_df.to_csv(os.path.join(output_dir,file),index=False,header=False,sep='\t')

# Combine geographically-based subreddits to create English dialect corpora
# Replace file names with the geographically-based data files
#   Format: ([city1, city2], output_file)
file_pairs = [(['Birmingham.csv', 'london.csv'], 'uk.csv'),
              (['California.csv', 'florida.csv'], 'us.csv'),
              (['melbourne.csv', 'sydney.csv'], 'au.csv')]

for files, output_file in file_pairs:
    first = os.path.join(output_dir,files[0])
    combined_df = pd.read_csv(first,sep='\t',header=None)
    print(len(combined_df))
    os.remove(first)

    for file in files[1:]:
        file = os.path.join(output_dir,file)
        next_df =pd.read_csv(file,sep='\t',header=None)
        os.remove(file)
        combined_df = pd.concat([combined_df, next_df])
    combined_df.to_csv(os.path.join(output_dir, output_file),index=False,header=False,sep='\t')
