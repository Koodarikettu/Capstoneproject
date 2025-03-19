
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain_groq import ChatGroq
from typing import List
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()


class SWOTAnalysis(BaseModel):
    strengths: List[str] = Field(..., description="List of strengths")
    weaknesses: List[str] = Field(..., description="List of weaknesses")
    opportunities: List[str] = Field(..., description="List of opportunities")
    threats: List[str] = Field(..., description="List of threats")

class PESTELAnalysis(BaseModel):
    political: List[str] = Field(..., description="List of Political factors")
    economic: List[str] = Field(..., description="List of Economic factors")
    social: List[str] = Field(..., description="List of Social factors")
    technological: List[str] = Field(..., description="List of Tehcnological factors")
    environmental: List[str] = Field(..., description="List of Environmental factors")
    legal: List[str] = Field(..., description="List of Legal factors")

parserSWOT = PydanticOutputParser(pydantic_object=SWOTAnalysis)
parserPESTEL = PydanticOutputParser(pydantic_object=PESTELAnalysis)


def pdf_to_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def splitter(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    chunks = text_splitter.create_documents([text])
    return chunks

def map_prompt(summarization_type):
    if summarization_type == "SWOT":
        map_prompt = """
        ### Instruction:
        Your job is to summarize the report that is given to you. Make comprehensive summary and do SWOT analysis.
        Do not include any explanatory text before or after the JSON.

        {format_instructions}


        ### Report:
        {text}
        """

        map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"], partial_variables={"format_instructions": parserSWOT.get_format_instructions()})

    else:
        map_prompt = """
        ### Instruction:
        Your job is to summarize the report that is given to you. Make comprehensive summary and do PESTEL analysis.
        Do not include any explanatory text before or after the JSON.

        {format_instructions}


        ### Report:
        {text}
        """

        map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"], partial_variables={"format_instructions": parserPESTEL.get_format_instructions()})        

    return map_prompt_template

def combine_prompt(summarization_type):
    if summarization_type == "SWOT":
        combine_prompt = """
        ### Instruction:
        Summarize Report's key points under SWOT-analysis four distinct headings: Sternghts, Weakneses, Opportunities and Threats
        Do not include any explanatory text before or after the JSON.

        {format_instructions}

        ### Report:
        {text}

        ### strengths:
        -

        ### weaknesses:
        - 

        ### opportunities:
        - 

        ### threats:
        - 
        """

        combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"], partial_variables={"format_instructions": parserSWOT.get_format_instructions()})

    else:
        combine_prompt = """
        ### Instruction:
        Summarize Report's key points under PESTEL-analysis five distinct headings: Political, Economic, Social, Tehcnological, Environmental, and Legal.
        Do not include any explanatory text before or after the JSON.

        {format_instructions}

        ### Report:
        {text}

        ### Political:
        -

        ### Economic:
        - 

        ### Social:
        - 

        ### Tehcnological:
        - 

        ### Environmental:
        -

        ### Legal:
        - 
        """

        combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"], partial_variables={"format_instructions": parserPESTEL.get_format_instructions()})

    return combine_prompt_template


def language_model():
    llm = ChatGroq(
    api_key= os.getenv("GROQ_API_KEY"),
    model_name="llama-3.2-90b-vision-preview",
    temperature=0.7
)
    return llm

    
def perform_analysis(report, summarization_type):

    try:
        if report.type == "application/pdf":
            report = pdf_to_text(report)
    except:
        pass

    summary_chain = load_summarize_chain(llm=language_model(), chain_type='map_reduce',
                                        map_prompt=map_prompt(summarization_type),
                                        combine_prompt=combine_prompt(summarization_type),
                                        verbose=True)


    splitted_text = splitter(report)
    output = summary_chain.run(splitted_text)

    if summarization_type == "SWOT":
        result_value = parserSWOT.parse(output)
    else:
        result_value = parserPESTEL.parse(output)

    return result_value