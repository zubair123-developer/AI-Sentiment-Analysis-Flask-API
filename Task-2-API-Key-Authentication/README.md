
# Task 2 - API Key Generation and Sharing

## Software Engineering Assignment 1

**Project:** RootSoftware Text Processing API

## Objective
Develop a secure Flask API that processes text and allows
three different consumers to access it using unique API keys.

## Technologies
- Python
- Flask
- python-dotenv
- Python secrets module
- cURL

## Features
- POST /process endpoint
- Converts text to uppercase
- Three unique API keys
- Authentication using X-API-Key header
- HTTP 200 for successful requests
- HTTP 401 for invalid or missing API keys
- API keys stored in environment variables

## API Endpoint

POST http://127.0.0.1:5002/process

Example JSON input:

{
  "text": "hello world"
}

Example successful response:

{
  "consumer": "Consumer 1",
  "original_text": "hello world",
  "processed_text": "HELLO WORLD"
}

## Setup

1. Install required libraries:

   pip install -r requirements.txt

2. Create a .env file using .env.example.

3. Generate three unique keys using Python's secrets module.

4. Configure API_KEY_1, API_KEY_2 and API_KEY_3.

5. Start the Flask API:

   python app.py

## Testing

Tested using cURL:

- Consumer 1: HTTP 200
- Consumer 2: HTTP 200
- Consumer 3: HTTP 200
- Invalid API key: HTTP 401
- Missing API key: HTTP 401

Actual API keys are not included in this repository.

## Demonstration Video

Add public video link here.
