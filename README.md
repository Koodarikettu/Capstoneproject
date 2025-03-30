**Capstoneproject**

# Financial Report Summarizer

This repository contains a tool for summarizing financial reports using AI-based models. It allows users to upload financial reports in PDF or text format and receive a summary in the form of SWOT or PESTEL analysis. This README provides an overview of how the system works, its components, and the technology stack used.

## How It Works

### 1. User Interaction (Frontend) - Streamlit Interface

User Uploads Report:

The user interacts with the frontend built using Streamlit. The interface allows the user to upload a financial report (either as a text or PDF file) and choose the type of analysis they want: SWOT or PESTEL.

Once the form is filled out (with the uploaded report and selected analysis type), the user submits it through a button.

Frontend Workflow:

If the report is uploaded as a PDF, it is handled using file_uploader and sent to the backend API.

If the report is entered directly as text, it is sent as a string to the backend.

After submission, Streamlit sends an HTTP request to the backend server (FastAPI) to perform the analysis.

### 2. Backend - FastAPI Server
Request Handling:

The backend is implemented using FastAPI, which handles incoming HTTP requests for both text-based reports and PDF files. FastAPI acts as an intermediary between the frontend and the AI model.

There are two main routes in the backend:

POST /analyze/report/text - This route processes text-based reports.

POST /analyze/report/pdf - This route processes PDF reports by extracting text first.

API Endpoint Workflow:

Upon receiving the request, FastAPI forwards the report and the analysis type (SWOT or PESTEL) to the perform_analysis function for processing.

### 3. Report Processing (Backend - Text Extraction and Analysis)
PDF to Text Conversion:

If the uploaded file is a PDF, the pdf_to_text function is called using PyPDF2 to extract the text content from the PDF.

Once the text is extracted, it is passed on to the next step for analysis.

Text Splitting:

The extracted text (whether from a PDF or directly entered) is passed to the splitter function, which uses RecursiveCharacterTextSplitter. This tool breaks the text into manageable chunks, which can then be processed by the AI model efficiently.

This step ensures that large reports are split into smaller sections, allowing for parallel processing, preventing timeouts, and handling large files effectively.

### 4. Summarization (Using LLM - Language Model)
AI Model Selection:

The system uses ChatGroq, a large language model (LLM), for the actual report summarization and analysis. The model used is Llama 3.3-70B Versatile, which is hosted and accessed via the Groq API.

The language_model() function configures and returns the model for use in the analysis step.

Prompt Creation:

Depending on the selected analysis type (SWOT or PESTEL), a corresponding prompt template is created. The prompts instruct the AI on how to structure the analysis based on the report content.

There are two distinct prompt types:

SWOT Prompt: Summarizes the report under four headings: Strengths, Weaknesses, Opportunities, and Threats.

PESTEL Prompt: Summarizes the report under six headings: Political, Economic, Social, Technological, Environmental, and Legal.

Analysis Execution:

The load_summarize_chain function orchestrates the summarization. It takes the chunks of text (from the splitting step) and feeds them into the LLM with the correct prompt.

The map_reduce technique is used, where each chunk is summarized individually, then combined into a final summary.

Output Parsing:

The summarization results from the model are parsed using PydanticOutputParser, converting the raw output into structured data (either SWOT or PESTEL).

### 5. Response Handling (Backend to Frontend)
Return Processed Data:

After the analysis is completed, the parsed results are sent back to the frontend as JSON data.

The Streamlit frontend receives the results and displays them to the user in a structured manner (either SWOT or PESTEL), breaking them down into relevant categories (e.g., Strengths, Weaknesses, Opportunities, Threats for SWOT or Political, Economic, Social, etc., for PESTEL).

### 6. API Integration - External Communication

API Endpoints:

The backend exposes the following API routes:

POST /analyze/report/text: Accepts a text report and analysis type (SWOT or PESTEL).

POST /analyze/report/pdf: Accepts a PDF report and analysis type (SWOT or PESTEL).

These endpoints are accessed by Streamlit through HTTP requests using requests.post, either sending a file or JSON data to the appropriate endpoint.

### Technologies Used:

Frontend:

Streamlit – for building the interactive web interface.

Backend:

FastAPI – for handling HTTP requests and managing API interactions.

PyPDF2 – for extracting text from PDF reports.

AI Model:

ChatGroq API – for utilizing Llama 3.3-70B Versatile for summarization and analysis.

Text Processing:

RecursiveCharacterTextSplitter – for splitting large text reports into smaller chunks.

Pydantic – for structured data handling and output parsing.

### How to Run the Application

### 1. Clone the repository:

git clone https://github.com/koodarikettu/Capstoneproject.git

### 2. Install dependencies:

Make sure you have Python 3.8+ installed.

Create a new virtual environment for the first time and activate the virtual environment.

Install required dependencies using pip:

pip install fastapi uvicorn pydantic langchain pypdf requests python-dotenv streamlit transformers langchain-groq dotenv python-multipart

### 3. Set up your environment:

Create a .env file in the project root and add your Groq API key:

GROQ_API_KEY=your_api_key_here

### 4. Run the FastAPI server:

uvicorn main:app --reload

### 5. Run the Streamlit frontend:

In a separate terminal window:

streamlit run app.py

### Testing the Application

The system has been tested both for frontend functionality (Streamlit interface) and backend reliability (FastAPI).

Unit tests have been implemented to ensure that the API endpoints work correctly for both text and PDF reports.

Integration tests were conducted to ensure that Streamlit interacts smoothly with the backend API and that the AI models return accurate summaries.

### Challenges Faced and Solutions Implemented:
Initial Model Limitations: Early on, the model selected was inadequate, and the prompt designs were ineffective, leading to poor results. This was addressed by switching to the ChatGroq Llama model, which provided better performance.

Handling Large Reports: Large reports would time out due to processing limitations. We resolved this by implementing the RecursiveCharacterTextSplitter, which breaks the text into smaller chunks that are processed in parallel.

Limited GPU Resources: There were limitations in GPU resources and time constraints for training a custom model. The solution was to use a pre-trained model from Groq instead of developing and training a custom model.
