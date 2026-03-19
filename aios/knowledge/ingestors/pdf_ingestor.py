"""
PDF Ingestor
Tutor AIOS - Knowledge Layer

Responsavel por:
- Ler arquivos PDF
- Extrair texto por pagina
- Limpar texto
- Preparar conteudo para chunking

Seguranca:
- Valida que o PDF esta dentro do diretorio permitido
"""

from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader


ALLOWED_BASE = Path("sources").resolve()


class PDFIngestor:

    def ingest(self, pdf_path: str) -> List[Dict]:

        path = Path(pdf_path).resolve()

        # Seguranca: bloqueia caminhos fora de sources/
        if not str(path).startswith(str(ALLOWED_BASE)):
            raise PermissionError(
                f"Acesso negado: '{pdf_path}' esta fora do diretorio permitido. "
                f"PDFs devem estar em: {ALLOWED_BASE}"
            )

        if not path.exists():
            raise FileNotFoundError(f"PDF nao encontrado: {pdf_path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Arquivo nao e um PDF: {pdf_path}")

        reader = PdfReader(str(path))
        pages = []

        for page_number, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text:
                continue
            cleaned = self._clean_text(text)
            pages.append({
                "source": str(path),
                "page": page_number + 1,
                "content": cleaned
            })

        return pages

    def _clean_text(self, text: str) -> str:
        text = text.replace("\n", " ").replace("\r", " ")
        while "  " in text:
            text = text.replace("  ", " ")
        return text.strip()
