    
from langchain_community.embeddings import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="all-minilm:33m")


sentence = input("Hi my name is Aadit ")

print(f"\nGenerating embeddings for: '{sentence}'\n")

embedding_vector = embeddings.embed_query(sentence)


print("=" * 60)
print(f"Embedding Vector (Length: {len(embedding_vector)} dimensions)")
print("=" * 60)
print(embedding_vector)
print("=" * 60)

