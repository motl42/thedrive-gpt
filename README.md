
# TheDrive-GPT

About
TheDrive-GPT is a vector db augmented question-answering system for Peter Attias podcast [thedrive] (https://peterattiamd.com/podcast/). It implements scripts to download, transcribe, diarize and embed all the episodes of thedrive via whisper, pyannote and openai embeddings. The app then utilizes qdrant for search functionality and GPT-3.5 to generate answers. The api is build via python (langchain) and the app is built using Next.js. It is deployed under https://thedrive-gpt.vercel.app/.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Usage](#usage)
4. [License](#license)

## Features

- download, transcribe, diarize and embed all episodes of [thedrive](https://peterattiamd.com/podcast/)
- ask questions about the podcast
- efficient search functionality using qdrant
- utilizes state-of-the-art GPT-3.5 model for answer generation
- modern and responsive user interface built with Next.js and Chakra UI

## Requirements
- OpenAI API key (https://platform.openai.com/account/api-keys)
- Qdrant instance and API key (https://qdrant.tech/)

## Usage

### Processing podcasts
To set up process podcasts on your local machine, follow these steps:

    pip install -r scripts/requirements.txt
    

Copy env.example and add your env variables.

    cp env.example env

Run all scripts (download, transcribe, diarize and embed)

    python scripts/run_all.py

### Running the app

Install requirements
    yarn install && pip install -r requirements.txt

Copy env.example and add your env variables.

    cp env.example env

Run the application (needed to be started via vercel cli because it uses python serverless functions)

    vercel dev

## License
Herold-GPT is released under the [MIT License](https://opensource.org/licenses/MIT).
