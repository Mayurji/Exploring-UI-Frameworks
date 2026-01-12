import pypdf
from sentence_transformers import SentenceTransformer

class EmbeddingManager:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, text):
        """Generate embeddings for a given text."""
        if isinstance(text, str):
            text = [text]
        return self.model.encode(text).tolist()

    def extract_text_from_pdf(self, pdf_file):
        """Extract text from a PDF file, such that words are not joined together, keep the spacing"""
        reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text(extraction_mode="layout") + "\n"
        return text.strip()
