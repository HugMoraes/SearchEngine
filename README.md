# Search Engine
This project is a search engine implementation using elasticsearch and Information Retrival techniques with a small database provided by Jusbrasil with jurical documents.

## Requirements

- Make sure you have docker installed

- Make sure you have all python dependencies instaled, use requirements.txt:

```bash
pip install -r requirements.txt
```

- Make sure to insert **"baseDocumentos"** file into /data

### Windows
- Make sure you have elasticsearch running as a service (Windows) or a process, and check on config/elasticsearch.yaml file if xpack.security.enabled is set to false, if not, change it and restart elasticsearch.

## How to run elasticSearch container
Make sure you have docker installed, then execute the following command to get the elasticSearch docker image:

```bash
docker pull elasticsearch:9.0.2
```

Create a network for the docker container:

```bash
docker network create somenetwork
```

Finally start the container:

```bash
docker run -d --name elasticsearch --net somenetwork -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:9.0.2
```

Wait about one minute for elastic search to start.

## How it works
The `pipelineReader.py` file is responsible for managing the  `baseDocumentos` file, it can load to memory and generate a list of documents with the index format compatible with the elastic search bulk api, and the index schema defined in schema.py