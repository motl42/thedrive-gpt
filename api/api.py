"""Main entrypoint for the app."""
import os

os.environ['LANGCHAIN_HANDLER'] = 'langchain'
os.environ["LANGCHAIN_SESSION"] = "thedrive"

import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from langchain.vectorstores import VectorStore, Qdrant
from qdrant_client import QdrantClient
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel

from qa_chain import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

""" openai.log = "debug" """

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logging.info("loading vectorstore")
    api_key = os.environ.get("QDRANT_API_KEY")
    host = os.environ.get("QDRANT_HOST")
    global docsearch
    docsearch = Qdrant(client=QdrantClient(url=host, api_key=api_key),embedding_function=OpenAIEmbeddings().embed_query, collection_name="thedrive")
    global chain
    chain = load_qa_chain(docsearch)



class Question(BaseModel):
    question: str

@app.post("/")
async def get(question: Question):
    return chain({"question": question.question})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)