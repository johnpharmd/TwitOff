#!/usr/bin/env python 3

import basilica
from scipy import spatial

sentences = [
    "This is a sentence!",
    "This is a similar sentence!",
    "I don't think this sentence is very similar at all...",
]

with basilica.Connection('06764615-5183-dfa3-e2f1-4f7e3f2c7590') as c:
    embeddings = list(c.embed_sentences(sentences))

print('Embeddings:', embeddings, '\n')
print(spatial.distance.cosine(embeddings[0], embeddings[1]), '\n')
print(spatial.distance.cosine(embeddings[0], embeddings[2]))

