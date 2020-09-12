import pandas as pd
import numpy as np
from bert_serving.client import BertClient

data = pd.read_csv('updated_police_dataset.csv')

# Extract Key Phrases Column
key_phrases = data['key_phrases'].tolist()
# Saved in string format, so converting to list
cleaned_phrases = []
for phrase in key_phrases:
    cleaned_phrases.append(phrase.strip('][').split(', '))

# Initialize an instance of a BERT client to query the 
# optimized instance of the model deployed on the server
bc = BertClient()

# For each record, pass in the list of key phrases and get 
# embedding for each phrase
embeddings = []
for row in cleaned_phrases:
    phrases_embeddings = bc.encode(row)
    # Initialize empty embedding of 768 dimensions (same as BERT)
    embed = np.array([0]*768)
    # Sum embedding for each key phrase for this row of data
    for embedding in phrases_embeddings:
        embed = np.add(embed, embedding)
    # Average the embedding
    embed = embed/len(phrases_embeddings)
    # Add it to the embeddings array so that it can be merged 
    # into the dataframe
    embeddings.append(embed)

# Merge into dataframe
data['key_phrase_embeddings'] = [0]*data.shape[0]
data['key_phrase_embeddings'] = data['key_phrase_embeddings'].astype('object')
data['key_phrase_embeddings'] = embeddings

# Print output
print(data.head(3))

# Write CSV
data.to_csv('data_with_embeddings.csv')