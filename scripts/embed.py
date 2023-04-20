from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
import os
from pprint import pprint
from dotenv import load_dotenv
from pod_utils import get_podcasts
import json 
from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

api_key = os.environ["QDRANT_API_KEY"]
host = os.environ["QDRANT_HOST"]
collection_name = "thedrive"

client = QdrantClient(url=host, api_key=api_key)
# Load the LangChain.

docsearch = None

#client.delete_collection(collection_name)

podcasts = get_podcasts()

for podcast in podcasts:


  file_path = os.path.join("data/thedrive", podcast["folder"], "chunks.json")
  if not os.path.exists(file_path):
    print("skipping", podcast["title"])
    continue
  print("started embedding", podcast["title"])
  with open(file_path, "r") as file:
    chunks = json.load(file)

  chunks = [chunk for chunk in chunks if "embedded" not in chunk or chunk["embedded"] == False]

  chunk_size = 10  
  for i in range(0, len(chunks), chunk_size):
    text_chunk = chunks[i:i + chunk_size]
    texts = [chunk["text"] for chunk in text_chunk]
    
    metadatas = [{"source": f"{i}", **text_chunk[i]["meta"]} for i in range(len(text_chunk))]
    if docsearch is None:
      docsearch = Qdrant.from_texts(texts=texts, metadatas=metadatas, embedding=OpenAIEmbeddings(
      ), api_key=api_key, url=host,collection_name=collection_name)
    else:
      docsearch.add_texts(texts, metadatas=metadatas)
    
    for chunk in text_chunk:
      chunk["embedded"] = True

    with open(file_path, "w") as file:
      json.dump(chunks, file)
