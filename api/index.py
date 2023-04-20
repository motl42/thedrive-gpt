"""Main entrypoint for the app."""
""" from langchain.embeddings.openai import OpenAIEmbeddings
from .qa_chain import load_qa_chain
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
from langchain.vectorstores import VectorStore, Qdrant
from fastapi.templating import Jinja2Templates
from typing import Optional
from pathlib import Path
import logging
import os """
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect

""" openai.log = "debug" """

app = FastAPI()

""" app.add_middleware(
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
    docsearch = Qdrant(client=QdrantClient(url=host, api_key=api_key),
                       embedding_function=OpenAIEmbeddings().embed_query, collection_name="thedrive")
    global chain
    chain = load_qa_chain(docsearch)


class Question(BaseModel):
    question: str


@app.post("/")
async def post(question: Question):
    return chain({"question": question.question}) """


@app.get("/", tags=["Root"])
async def read_root():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }

@app.get("/hello/")
async def get():
    return {"question": "hello?"}
