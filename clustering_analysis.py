import numpy as np
import pandas as pd

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