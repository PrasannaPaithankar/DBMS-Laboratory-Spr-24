from langchain_community.embeddings import HuggingFaceEmbeddings
from eurelis_langchain_solr_vectorstore import Solr


def initSolr(path):
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    vector_store = Solr(embeddings,
                        core_kwargs={'page_content_field': 'text_t',
                                     'vector_field': 'vector',
                                     'core_name': 'langchain',
                                     'url_base': 'http://localhost:8983/solr'})

    return vector_store
