import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import umap

data = pd.read_csv('data_with_embeddings.csv')
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# Extract Key Phrases Column
key_phrase_embeddings = data['key_phrase_embeddings'].tolist()
# Saved in string format, so converting to numpy ndarray with np floats
cleaned_embeddings = []
for embedding in key_phrase_embeddings:
    string_embedding = embedding.strip('][').split(', ')[0].split(' ')
    embed = []
    for element in string_embedding:
        if element:
            embed.append(np.float(element.rstrip().strip()))
    embed = np.array(embed)
    cleaned_embeddings.append(embed)

# Rewrite column since it is now in the correct format
data['key_phrase_embeddings'] = cleaned_embeddings

# Extract rows with unique case IDs for TensorFlow Projector
unique_rows = data.drop_duplicates(subset=['Incident Number'])
print(unique_rows.columns)

# Save Embeddings
string_embeddings = []
for row in unique_rows.itertuples():
    embedding = row.key_phrase_embeddings
    embedding_str = ''
    for element in embedding:
        embedding_str += str(element)+"\t"
    embedding_str.rstrip().strip()
    string_embeddings.append(embedding_str)

# Write embeddings TSV to file
with open('embeddings.tsv','w+') as embeddings_file:
    for row in string_embeddings:
        embeddings_file.write(row+"\n")
    embeddings_file.close()

# Save Embeddings Metadata
string_metadata = []
for index, row in unique_rows.iterrows():
    string_ = str(row['Incident Number']) + "\t" + \
                str(row['Rank']) + "\t" + \
                str(row['Officer Race']) + "\t" + \
                str(row['Officer Gender']) + "\t" + \
                str(row['Years of SPD Service']) + "\t" + \
                str(row['Type of Weapon']) + "\t" + \
                str(row['Subject Gender']) + "\t" + \
                str(row['Subject Race']) + "\t" + \
                str(row['Subject Age']) + "\t" + \
                str(row['Fatal']) + "\t" + \
                str(row['On-duty']) + "\t" + \
                str(row['Disposition']) + "\t" + \
                str(row['Officer Disciplined?']) + "\t"
    summary = row['Summary'].split(' ')
    summary = " ".join([x.strip().rstrip() for x in summary]).rstrip().strip()
    string_ += summary
    string_metadata.append(string_)

# Write embeddings metadata TSV to file
with open('embeddings_labels.tsv','w+') as embeddings_file:
    embeddings_file.write("IncidentNumber\tRank\tOfficerRace\tOfficerGender\tYearsOfSPDService\tTypeOfWeapon\tSubjectGender\tSubjectRace\tSubjectAge\tFatal\tOn-duty\tDisposition\tOfficerDisciplined?\tSummary" + "\n")
    for row in string_metadata:
        embeddings_file.write(row+"\n")
    embeddings_file.close()

# Create UMAP for dimensionality reduction
reducer = umap.UMAP()

# Fit UMAP to embedding data
umap_embedding = reducer.fit_transform(cleaned_embeddings)

plt.scatter(umap_embedding[:, 0], umap_embedding[:, 1])
plt.gca().set_aspect('equal', 'datalim')
plt.title('UMAP projection of OIS', fontsize=24)

plt.show()

def draw_umap(n_neighbors=15, min_dist=0.1, n_components=2, metric='euclidean', title=''):
    fit = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=n_components,
        metric=metric
    )
    u = fit.fit_transform(cleaned_embeddings)
    fig = plt.figure()
    if n_components == 1:
        ax = fig.add_subplot(111)
        ax.scatter(u[:,0], range(len(u)))
    if n_components == 2:
        ax = fig.add_subplot(111)
        ax.scatter(u[:,0], u[:,1])
    if n_components == 3:
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(u[:,0], u[:,1], u[:,2], s=100)
    plt.title(title, fontsize=18)
    plt.show()

draw_umap(n_neighbors=20, title='UMap Projection of OIS')

from sklearn.cluster import KMeans

