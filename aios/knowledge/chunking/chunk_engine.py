"""
Chunk Engine
Tutor AIOS — Knowledge Layer

Responsável por:
- transformar páginas em chunks
- manter contexto entre chunks
- preparar dados para embeddings
"""

from typing import List, Dict


class ChunkEngine:
    """
    Divide textos em chunks ideais para embeddings.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        overlap: int = 120
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_pages(self, pages: List[Dict]) -> List[Dict]:
        """
        Recebe páginas do PDFIngestor e retorna chunks estruturados.
        """

        chunks = []

        for page in pages:

            content = page["content"]
            source = page["source"]
            page_number = page["page"]

            text_chunks = self._split_text(content)

            for idx, chunk in enumerate(text_chunks):

                chunks.append(
                    {
                        "source": source,
                        "page": page_number,
                        "chunk_index": idx,
                        "content": chunk
                    }
                )

        return chunks

    def _split_text(self, text: str) -> List[str]:
        """
        Divide texto em pedaços com overlap.
        """

        chunks = []

        start = 0
        length = len(text)

        while start < length:

            end = start + self.chunk_size

            chunk = text[start:end]

            chunks.append(chunk)

            start += self.chunk_size - self.overlap

        return chunks