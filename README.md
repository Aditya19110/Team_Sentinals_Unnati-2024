# Team Sentinals: Cancer-Related Chatbot

Welcome to the official repository of **Team Sentinals** from **MGMs College of Engineering, Nanded**! We are excited to present our chatbot designed to answer basic questions related to cancer. Our chatbot provides accurate and concise responses to your inquiries.

## Problem Statement
**"Introduction to GenAI and Simple LLM Inference on CPU and finetuning of LLM Model to create a Custom Chatbot"**

## Project Overview
Our solution leverages Intel's Neural Chat LLM for local inference on CPU, making it highly accessible and efficient without requiring GPU resources. The chatbot ingests data from PDF files, converts the text into embeddings using BGE Embeddings, and implements Retrieval-Augmented Generation (RAG) using an open-source stack.

### Key Components
- **Intel's Neural Chat LLM:** Chosen for its capability to run independently on CPUs.
- **BGE Embeddings:** Utilized for text embedding.
- **Chroma DB:** Serves as the vector store.
- **Langchain & CTransformers:** Frameworks used for orchestration.

## Getting Started

### Prerequisites
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Team_Sentinals_Unnati-2024/new/main?filename=README.md
   cd Team_Sentinals_Unnati-2024
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Additional Dependency:**
   ```bash
   pip install protobuf==3.20.0
   ```

### Download the LLM
Due to space constraints, the LLM is not included in this repository. Please download the Intel Neural Chat LLM from [Hugging Face](https://huggingface.co/TheBloke/neural-chat-7B-v3-1-GGUF/blob/main/neural-chat-7b-v3-1.Q4_K_M.gguf) and place it in the appropriate directory.

### Data Preparation
Convert the data to embeddings by running:
```bash
python ingest.py
```
*Note: This process might take some time as it converts the data into embeddings.*

### Running the Chatbot
Start the Flask application:
```bash
python app.py
```

Visit the provided URL in your browser to interact with the chatbot and ask any cancer-related questions.

## Conclusion
Thank you for exploring our project! We hope our chatbot provides valuable assistance in answering your cancer-related queries.