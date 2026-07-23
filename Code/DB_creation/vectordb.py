from Code.DB_creation.unified_data import create_unified_data
from Code.DB_creation.embedding_lancedb import embedding_lancedb


def create_db():
    create_unified_data()
    embedding_lancedb()
