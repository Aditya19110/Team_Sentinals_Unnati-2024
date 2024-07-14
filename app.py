import flask
from flask import Flask, request, jsonify, render_template
import os
from langchain import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

app = Flask(__name__)

local_llm = "neural-chat-7b-v3-1.Q4_K_M.gguf"

config = {
    'max_new_tokens': 1024,
    'repetition_penalty': 1.1,
    'temperature': 0.2,
    'top_k': 50,
    'top_p': 0.9,
    'stream': True,
    'threads': int(os.cpu_count() / 2)
}

llm = CTransformers(
    model=local_llm,
    model_type="mistral",
    lib="avx2",
    **config
)

print("LLM Initialized...")

prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

prompt = PromptTemplate(template=prompt_template,
                        input_variable=['context', 'question'])
load_vector_store = Chroma(
    persist_directory="stores/medical_cosine", embedding_function=embeddings)
retriever = load_vector_store.as_retriever(search_kwargs={"k": 1})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_responses():
    query = request.form.get('query')
    chain_type_kwargs = {"prompt": prompt}
    
    try:
        if not query or len(query.strip()) < 2:
            raise ValueError("Query is empty or too short.")
        
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,  
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs,
            verbose=True
        )

        response = qa.invoke(query)
        
        if 'result' in response:
            answer = response['result']
        else:
            answer = 'No answer found'
        
        if 'source_documents' in response and response['source_documents']:
            source_document = response['source_documents'][0].page_content
            doc = response['source_documents'][0].metadata.get('source', 'Unknown')
        else:
            source_document = 'No source document found'
            doc = 'Unknown'
        
        response_data = {
            "answer": answer,
            "source_document": source_document,
            "doc": doc
        }
    
    except Exception as e:
        
        app.logger.error(f"Error processing request: {str(e)}")
        
        error_message = f"Error processing request: {str(e)}"
        response_data = {
            "answer": "Error",
            "source_document": error_message,
            "doc": "Unknown"
        }
    
    return jsonify(response_data)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
