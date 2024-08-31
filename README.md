# PDF ChatBot - Gemini Pro - Backend

## Description

Backend application for a chatbot powered by Google's Gemini Pro AI model. It can take in multiple PDF Files and answer any query on the data present in the pdf's contents. It also has an sql database on which queries can be asked in human conversational manner and data from the SQL database will be returned to the end user. The SQL query part is yet to be implemented.

### Tech Stack Used

- Python FastAPI
- LangChain
- SQLite
- Google's Gemini Pro Model
- FAISS

## Installation

To install the project on your local machine, follow these steps:
1. Clone the repository on your machine using the following command:
```bash
git clone https://github.com/sshikhar09/chatbot-backend.git
```

2. Open your terminal and navigate to the project root directory.

3. In the .env file, replace the value of GOOGLE_API_KEY with your own API Key which can be generated from [here](https://aistudio.google.com/).

4. Create a virtual environment using the following command:
```bash
python3 -m venv venv
```
5. Activate the Virtual environment using the following command:
```bash
source venv/bin/activate
```
6. Install the dependcies listed in the requirements.txt file using the following command:
```bash
pip install -r requirements.txt
```
7. Run the sql.py file to populate the database with the static data values with the following command:
```bash
python sql.py
```
8. Run the project using the following command:
```bash
uvicorn app:app --reload
```

## API Endpoints

Following are the API Endpoints available to access the application and its features:

1. /check:

To check whether the app is running properly or not. Once the app is run, if any data is previously stored in the vector store, it will be erased so as to clear the previous session and reset the vector store.

cURL:
```
curl --location 'http://127.0.0.1:8000/check'
```

2. /upload-pdfs:

To upload pdf files to the vector store so that the AI can answer questions on them. Multiple files can be uploaded at once, all files should uploaded with the key as 'files'.

cURL:
```
curl --location 'http://127.0.0.1:8000/upload-pdfs' \
--form 'files=@"/Users/path_to_file/file_name.pdf"'
```

3. /ask-question:

To ask questions on the pdf uploaded and the sql data run initially. Question should include as many keywords as possible about the query topic to optimize similarity search. Questions should be included as parameter key-value pairs with key being 'user_question'.

cURL:
```
curl --location 'http://127.0.0.1:8000/ask-question?user_question=What%20is%20Lorem%20Ipsum%3F'
```

## TODOS and Future steps

Code to upload SQL data to vector store is already present in the commented code in app.py file. However, as of now, when both pdfs and sql data is uploaded to vector store, questions are answered on neither pdfs nor sql data. Thus, that code is commented to show that the implementation is almost complete. It will be included as the bug is resolved.

Contextual conversation is not included in this version. It will be included in future updates.

## Contact

For questions or comments, please contact [Shikhar Srivastava](https://www.linkedin.com/in/shikhar-srivastava-518598218/).