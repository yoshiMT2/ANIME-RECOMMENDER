from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter


class VectorStoreBuilder:
    def __init__(
        self, csv_path: str, embedding_model='all-MiniLM-L6-v2', persist_dir: str = 'chroma_db'
    ):
        self.csv_path = csv_path
        self.persist_dir = persist_dir
        self.embedding = HuggingFaceEmbeddings(model_name=embedding_model)

    def build_and_save_vectorstore(self, encoding='utf-8', size=1000, overlap=100, metadata=None):
        if metadata is None:
            metadata = []
        loader = CSVLoader(file_path=self.csv_path, encoding=encoding, metadata_columns=metadata)

        data = loader.load()

        splitter = CharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
        texts = splitter.split_documents(data)

        db = Chroma.from_documents(texts, self.embedding, persist_directory=self.persist_dir)
        db.persist()

    def load_vector_store(self):
        return Chroma(persist_directory=self.persist_dir, embedding_function=self.embedding)
