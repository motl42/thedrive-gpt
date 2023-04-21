"""Main entrypoint for the app."""
from langchain.embeddings.openai import OpenAIEmbeddings
from .qa_chain import load_qa_chain
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
from langchain.vectorstores import VectorStore, Qdrant
from fastapi.templating import Jinja2Templates
from typing import Optional
from pathlib import Path
import os
import logging
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect

""" openai.log = "debug" """

app = FastAPI()

# add middleware which logs every request
from fastapi import FastAPI, Request

app = FastAPI()

# define your middleware function to log request
async def log_request(request: Request, call_next):
    print(f"request middleware: {request.method} {request.url} {request.url.path}")
    #print the href of the request

    response = await call_next(request)
    return response

# add the middleware to the application
app.middleware("http")(log_request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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
    init()
    return chain({"question": question.question})

@app.get("/api/hello")
async def get():
    return {"question": "hello?"}

@app.get("/api/index/hello")
async def get():
    return {"question": "hello?"}