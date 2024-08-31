from fastapi import FastAPI, File, UploadFile, HTTPException
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from constants import Constants
import pandas as pd
from dotenv import load_dotenv
import os
import shutil
import sqlite3

app = FastAPI()
load_dotenv()

folder_path = os.path.join(Constants.project_path,Constants.folder_name)
def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf.file.seek(0)
        pdf_reader = PdfReader(pdf.file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = Constants.embedding_model)
    # query1 = "SELECT * From USERS"
    # data1 = read_query(query1,"database.db")
    # query2 = "SELECT * From SURVEY"
    # data2 = read_query(query2,"database.db")
    # query3 = "SELECT * From RESPONSES"
    # data3 = read_query(query3,"database.db")
    # data = data1 + data2 + data3
    vector_store = FAISS.from_texts(text_chunks,embedding = embeddings)
    vector_store.save_local(Constants.folder_name)
    # vector_store = FAISS.load_local("pdf_storage", embeddings,allow_dangerous_deserialization=True)
    # data_chunks = get_text_chunks(data)
    # vector_store.add_texts(data_chunks)
    # vector_store.save_local("pdf_storage")
    # TODO: Add SQL Data to vector store so that its questions can also be answered along with pdf data.


def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model=Constants.llm_model, temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


@app.get("/ask-question")
async def user_input(user_question: str):
    if not os.path.exists(folder_path):
        return {"Reply": "Answer is not available in the context."}
    else:
        try:
            embeddings = GoogleGenerativeAIEmbeddings(model = Constants.embedding_model)
            
            new_db = FAISS.load_local(Constants.folder_name, embeddings,allow_dangerous_deserialization=True)
            docs = new_db.similarity_search(user_question)
            chain = get_conversational_chain()

            
            response = chain(
                {"input_documents":docs, "question": user_question}
                , return_only_outputs=True)
            return {"Reply": response["output_text"]}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def read_query(sql,db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(sql,conn)
    data = df.to_string()
    return data

@app.post("/upload-pdfs")
async def upload_pdfs(files: list[UploadFile] = File(...)):
    try:
        raw_text = get_pdf_text(files)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        return {"message": "PDFs processed and vectors saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/check")
async def checker():
    return {"message": "API Working Successfully!"}

@app.on_event("startup")
def startup_event():
    load_dotenv()
    os.environ['GRPC_DNS_RESOLVER'] = 'native'
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)


# def main():
#     st.set_page_config("Chat PDF")
#     st.header("Chat with PDF using Gemini💁")

#     user_question = st.text_input("Ask a Question from the PDF Files")

#     if user_question:
#         user_input(user_question)

#     with st.sidebar:
#         st.title("Menu:")
#         pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
#         if st.button("Submit & Process"):
#             with st.spinner("Processing..."):
#                 raw_text = get_pdf_text(pdf_docs)
#                 text_chunks = get_text_chunks(raw_text)
#                 get_vector_store(text_chunks)
#                 st.success("Done")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host=Constants.host_url,port=Constants.host_port)