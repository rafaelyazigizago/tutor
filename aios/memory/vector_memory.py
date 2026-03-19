import hashlib
import chromadb
from aios.embeddings.embedding_singleton import EmbeddingSingleton


class VectorMemory:
    """
    Memoria semantica baseada em embeddings.
    CORRECOES APLICADAS:
      - PersistentClient: memoria sobrevive entre sessoes
      - hash MD5 determinisitco: IDs estaveis
      - Protecao contra colecao vazia no search()
      - Protecao contra duplicatas no store()
      - EmbeddingSingleton: modelo carrega uma unica vez
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorMemory, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.client = chromadb.PersistentClient(path="./data/chroma")
        self.collection = self.client.get_or_create_collection(
            name="tutor_memory"
        )
        self.embedder = EmbeddingSingleton.get_model()

    def store(self, text: str):
        doc_id = hashlib.md5(text.encode("utf-8")).hexdigest()
        embedding = self.embedder.encode(text).tolist()
        existing = self.collection.get(ids=[doc_id])
        if not existing["ids"]:
            self.collection.add(
                documents=[text],
                embeddings=[embedding],
                ids=[doc_id]
            )

    def search(self, query: str, limit: int = 3):
        count = self.collection.count()
        if count == 0:
            return []
        embedding = self.embedder.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=min(limit, count)
        )
        return results["documents"][0]

    def count(self):
        return self.collection.count()
