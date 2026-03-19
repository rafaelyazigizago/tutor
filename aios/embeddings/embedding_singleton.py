"""
Embedding Singleton
Tutor AIOS

Carrega o modelo de embedding UMA única vez
para todo o sistema.
"""

from sentence_transformers import SentenceTransformer


class EmbeddingSingleton:

    _instance = None
    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print("Loading embedding model (singleton)...")

            cls._model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

        return cls._model
