run:
	if [ ! -d ./Solr ]; then (mkdir -p ./Solr && sudo chmod a+rwx ./Solr) fi;sudo docker compose up

clean:
	sudo docker stop $(sudo docker ps -a -q);sudo docker container prune

create-collection:
	curl 'http://localhost:8983/solr/admin/collections?action=CREATE&name=langchain&numShards=1&collection.configName=_default'

create-schema:
	curl http://localhost:8983/solr/langchain/schema -X POST -H 'Content-type:application/json' --data-binary '{ "add-field-type" : { "name":"knn_vector", "class":"solr.DenseVectorField", "vectorDimension":768, "similarityFunction":"euclidean" }, "add-field" : [{ "name":"vector", "type":"knn_vector", "indexed":true, "stored":true }, { "name":"title", "type":"text_general", "indexed":true, "stored":true }] }'

create-index:
	curl http://localhost:8983/solr/langchain/update/json/docs?commit=true -X POST -H 'Content-type:application/json' --data-binary @./data/data_for_indexing.json

delete-collection:
	curl 'http://localhost:8983/solr/admin/collections?action=DELETE&name=langchain'

all:
	bash ./setup.bash