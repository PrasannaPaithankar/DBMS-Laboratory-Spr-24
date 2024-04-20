# Assignment 5 - Utilizing Hadoop Ecosystem to Implement RAG for Chain of Thought Reasoning in Language Models

### [Final Project Report](./Utilizing%20Hadoop%20Ecosystem%20to%20Implement%20RAG%20for%20Chain%20of%20Thought%20Reasoning%20in%20Language%20Models.pdf)
### [Presentation](./A5%20PPT.pdf)

### Local setup
```bash
sudo python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### Some necessary changes in eurelis_langchain_solr_vectorstore package
- Locate the package in the venv directory
- In the `solr_core.py` file, in function `vector_search` comment out the following line:
```python
for solr_field,  in doc.items():
    metadata_key = SolrCore.metadata_key_for_field_name(solr_field)
    if not metadata_key or not isinstance(value, (str, int, float, bool)):
        continue
    metadata[metadata_key] = value
```
- In the `types.py` file, redefine the function `_results_to_docs_and_scores` as follows:
```python
def _results_to_docs_and_scores(results: Any) -> List[Tuple[Document, float]]:
    return [
        (Document(page_content=str(results["documents"][0][i][0]), metadata=results["metadatas"][0][i] or {}), results["distances"][0][i])
        for i in range(len(results["documents"][0]))
    ]
```
### Run
```bash
make all
source venv/bin/activate
flask --app WebInterface run --host=0.0.0.0 --port=20000
```

### Contribute
```bash
git checkout -b <branch-name>
git rm -r --cached .
git add .
git commit -m "commit message"
git push origin <branch-name>
```
***