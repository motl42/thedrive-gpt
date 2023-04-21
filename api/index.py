"""Main entrypoint for the app."""
from langchain.embeddings.openai import OpenAIEmbeddings
from .qa_chain import load_qa_chain
from pydantic import BaseModel
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
import os
import logging
from fastapi import FastAPI

""" openai.log = "debug" """

app = FastAPI()


async def init():
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


class Question(BaseModel):
    question: str


@app.post("/api")
async def post(question: Question):
    await init()
    return chain({"question": question.question})
