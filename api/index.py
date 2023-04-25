"""Main entrypoint for the app."""
import json
from http.server import BaseHTTPRequestHandler
from langchain.embeddings.openai import OpenAIEmbeddings
from .qa_chain import load_qa_chain
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
import os
import logging

""" openai.log = "debug" """


def init():
    if "docsearch" in globals():
        return
    logging.info("loading vectorstore")
    api_key = os.environ.get("QDRANT_API_KEY")
    host = os.environ.get("QDRANT_HOST")
    global docsearch
    docsearch = Qdrant(client=QdrantClient(url=host, api_key=api_key),
                       embedding_function=OpenAIEmbeddings().embed_query, collection_name="thedrive")
    global chain
    chain = load_qa_chain(docsearch)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("seas 1")
        content_length = int(self.headers['Content-Length'])
        print("seas 2")
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data)

            print("seas 3")
            init()
            print("seas 4")
            response = chain({"question": data["question"]})
            self.send_response(200)
        except json.JSONDecodeError:
            response = {
                'error': 'Invalid JSON data'
            }
            self.send_response(400)

        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
