import json
import os

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

path = "data"
documents = []
for file in os.listdir(path):
    if file.endswith('.pdf'):
        print(f"Loading {file}")
        pdf_path = os.path.join(path, file)
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)
print(f"Loaded {len(chunked_documents)} documents")

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

doc_Text = [doc.page_content for doc in chunked_documents]
embeddings = embedding.embed_documents(doc_Text)

# store embeddings to a file for future use
with open("data/embeddings_pre.json", "w") as f:
    json.dump(embeddings, f)

# each json entry is a dictionary with keys 'vector' and 'title'
json_data = []
for i, doc in enumerate(chunked_documents):
    json_data.append({"vector": embeddings[i],
                      "title": doc.metadata["source"]})

with open("data/data_for_indexing.json", "w") as f:
    json.dump(json_data, f)
print("Embeddings written to data/data_for_indexing.json")