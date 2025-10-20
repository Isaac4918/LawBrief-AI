# LawBrief-AI

## Overview
**LawBrief-AI** is an application developed as part of a technical interview project. Its primary purpose is to process legal documents and extract meaningful insights, including concise summaries and key financial data. The system is designed to assist legal professionals in quickly understanding the essential information within law proceedings.

## Key Features
- **Document Analysis:** Ingest and process law proceedings' documents.  
- **Automatic Summarization:** Generate clear and concise summaries of legal texts.  
- **Financial Insights Extraction:** Identify and extract relevant economic data from legal documents.  

## Purpose
The application aims to streamline the review of legal documents, enabling faster decision-making and reducing manual workload for legal practitioners.

## Previous Requirements
- Python programming language install
- Node and npm installed
- Azure Account Storage, Azure Form Recognizer and Azure AI Foundry services running in the Azure Platform.

## Installation
### Backend
1. Clone the repository:
   ```bash
   git clone https://github.com/isaac4918/LawBrief-AI.git
   ```
2. Go to the backend directory
   ```bash
   cd LawBrief-AI/backend
   ```
3. Create the .env file and put this variables with the correct information

   #### Azure OpenAI
   AZURE_OPENAI_KEY=XXXXXXXXXXXXXXXXXXXXXX
   AZURE_OPENAI_ENDPOINT=XXXXXXXXXXXXXXXX
   AZURE_OPENAI_API_VERSION=XXXXXXXXXXX
   AZURE_OPENAI_DEPLOYMENT=XXXXXXXXXXX
   #### Azure Blob Storage
   AZURE_BLOB_CONN_STRING=XXXXXXXXXXXXXXXXX
   BLOB_CONTAINER_NAME=XXXXXXXXXXXX
   #### Azure Form Recognizer
   AZURE_FORM_RECOGNIZER_ENDPOINT=XXXXXXXXXXXXX
   AZURE_FORM_RECOGNIZER_KEY=XXXXXXXXX

4. Install the necessary dependencies
   ```bash
   pip install -r requirements.txt
   ```
5. Execute the backend application
   ```bash
   uvicorn main:app --reload
   ```

### Frontend
1. Clone the repository:
   ```bash
   git clone https://github.com/isaac4918/LawBrief-AI.git
   ```
2. Go to the frontend directory
   ```bash
   cd LawBrief-AI/frontend
   ```
3. Create the .env file and put this variables with the correct information

   VITE_API_URL=XXXXXX

4. Install the necessary dependencies
   ```bash
   npm install
   ```
5. Build the application
   ```bash
   npm run build
   ```
6. Install the server executer
   ```bash
   npm install -g serve
   ```
7. Execute the application
   ```bash
   serve -s dist
   ```

⚠️ **Important:** Don't forget you must use two different terminals to execute the frontend and the backend and both must be running at the same time!
