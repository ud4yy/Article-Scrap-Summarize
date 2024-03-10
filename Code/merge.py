from Scrapper import scrap
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

article_list = scrap()

## Initialize the SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Extract titles from article_list
titles = [article['Title'] for article in article_list]

# Encode title embeddings
title_embeddings = model.encode(titles)

# Set a similarity threshold
similarity_threshold = 0.8

# List to store indices of articles to be removed
indices_to_remove = []

# Compare each pair of titles
for i in range(len(titles)):P
    for j in range(i + 1, len(titles)):
        similarity_score = cosine_similarity([title_embeddings[i]], [title_embeddings[j]])[0][0]

        # Check if similarity is above the threshold
        if similarity_score > similarity_threshold:
            # Merge 'Description' of the second article into the first article
            article_list[i]['Description'] += '\n' + article_list[j]['Description']

            # Add the index of the second article to the list of indices to be removed
            indices_to_remove.append(j)

# Remove articles with indices in reverse order to avoid index errors
for index in sorted(indices_to_remove, reverse=True):
    if 0 <= index < len(article_list):
        del article_list[index]
# Now, article_list contains merged descriptions based on title similarity
# Convert the list of dictionaries to a JSON object
json_object = json.dumps(article_list, indent=2)

# Save the JSON object to a file
with open('newarticles2.json', 'w') as json_file:
    json_file.write(json_object)

print('JSON file saved as articles.json')
