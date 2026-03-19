"""
Embedding Engine
Tutor AIOS — Knowledge Layer
"""

from typing import List, Dict
from aios.memory.vector_memory import VectorMemory


class EmbeddingEngine:

    def __init__(self):
        self.vector_memory = VectorMemory()

    def embed_chunks(self, chunks: List[Dict]) -> int:

        stored = 0

        for chunk in chunks:

            text = chunk["content"]

            # VectorMemory só aceita texto
            self.vector_memory.store(text)

            stored += 1

        return stored