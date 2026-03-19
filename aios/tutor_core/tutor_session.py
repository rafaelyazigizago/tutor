"""
Tutor Session
Tutor AIOS - Tutor Core

Responsavel por:
- orquestrar o pipeline completo de uma sessao de ensino
- conectar Knowledge Layer com Tutor Core
- registrar progresso ao final de cada aula
"""

from aios.knowledge.ingestors.pdf_ingestor import PDFIngestor
from aios.knowledge.chunking.chunk_engine import ChunkEngine
from aios.knowledge.embeddings.embedding_engine import EmbeddingEngine
from aios.knowledge.knowledge_search import KnowledgeSearch
from aios.tutor_core.curriculum_engine import CurriculumEngine
from aios.tutor_core.lesson_generator import LessonGenerator
from aios.tutor_core.progress_tracker import ProgressTracker


class TutorSession:

    def __init__(self):
        self.pdf_ingestor = PDFIngestor()
        self.chunk_engine = ChunkEngine()
        self.embedding_engine = EmbeddingEngine()
        self.curriculum_engine = CurriculumEngine()
        self.lesson_generator = LessonGenerator()
        self.progress_tracker = ProgressTracker()

    def ingest_pdf(self, pdf_path: str) -> int:
        """
        Ingere um PDF no VectorMemory.
        Retorna o numero de chunks armazenados.
        """
        print(f"\n[1/3] Lendo PDF: {pdf_path}")
        pages = self.pdf_ingestor.ingest(pdf_path)
        print(f"      Paginas extraidas: {len(pages)}")

        print(f"\n[2/3] Dividindo em chunks...")
        chunks = self.chunk_engine.chunk_pages(pages)
        print(f"      Chunks gerados: {len(chunks)}")

        print(f"\n[3/3] Gerando embeddings e armazenando...")
        stored = self.embedding_engine.embed_chunks(chunks)
        print(f"      Chunks armazenados: {stored}")

        return stored

    def generate_curriculum(self, topic: str) -> str:
        """
        Gera um curriculo baseado no conhecimento ingerido.
        """
        print(f"\n[Curriculo] Analisando conhecimento sobre: {topic}")
        curriculum = self.curriculum_engine.generate_curriculum(topic)
        print(f"      Curriculo gerado.")
        return curriculum

    def run_lesson(self, course_id: str, module: str, topic: str) -> str:
        """
        Gera uma aula completa e registra o progresso.
        """
        print(f"\n[Aula] Gerando aula sobre: {topic}")
        lesson = self.lesson_generator.generate_lesson(topic)

        print(f"\n[Progresso] Registrando aula concluida...")
        self.progress_tracker.record_lesson(course_id, module, topic)

        return lesson

    def get_progress(self, course_id: str) -> str:
        """
        Retorna resumo do progresso do aluno.
        """
        return self.progress_tracker.summary(course_id)
