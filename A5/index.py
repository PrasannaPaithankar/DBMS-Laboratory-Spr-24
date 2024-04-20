import json
import os

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

path = "data_full"
documents = []
for file in os.listdir(path):
    if file.endswith('.pdf'):
        print(f"Loading {file}")
        pdf_path = os.path.join(path, file)
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)
print(f"Loaded {len(chunked_documents)} documents")

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
embedding = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

doc_Text = [doc.page_content for doc in chunked_documents]
embeddings = embedding.embed_documents(doc_Text)

json_data = []
for i, doc in enumerate(chunked_documents):
    json_data.append({"vector": embeddings[i],
                      "text_t": doc.page_content})

with open("data_for_indexing.json", "w") as f:
    json.dump(json_data, f)
print("Embeddings written to data_for_indexing.json")
