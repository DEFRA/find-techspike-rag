import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering

def chunk_documents(text, n_clusters=8):
    def process_text(text):
        model = SentenceTransformer('all-mpnet-base-v2')
        sentences = text.split(".")
        sentences = [s.strip() for s in sentences if s.strip()]
        embeddings = model.encode(sentences)
        
        clustering = AgglomerativeClustering(n_clusters=n_clusters)
        clustering.fit(embeddings)
        
        chunks = {}
        for idx, cluster_id in enumerate(clustering.labels_):
            if cluster_id not in chunks:
                chunks[cluster_id] = []
            chunks[cluster_id].append(sentences[idx])
            
        return [" ".join(chunk) for chunk in chunks.values()]
    
    return process_text 