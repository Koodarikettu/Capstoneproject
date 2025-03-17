from bs4 import BeautifulSoup
import pandas as pd
import json
import bs4
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain_groq import ChatGroq
from typing import List
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()


class SWOTAnalysis(BaseModel):
    strengths: List[str] = Field(..., description="List of strengths")
    weaknesses: List[str] = Field(..., description="List of weaknesses")
    opportunities: List[str] = Field(..., description="List of opportunities")
    threats: List[str] = Field(..., description="List of threats")

parser = PydanticOutputParser(pydantic_object=SWOTAnalysis)


def splitter(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    chunks = text_splitter.create_documents([text])
    return chunks

def map_prompt():
    map_prompt = """
    ### Instruction:
    Your job is to summarize the report that is given to you. Make comprehensive summary and do SWOT analysis.

    {format_instructions}


    ### Report:
    {text}
    """

    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"], partial_variables={"format_instructions": parser.get_format_instructions()})


    return map_prompt_template

def combine_prompt():
    combine_prompt = """
    ### Instruction:
    Summarize Report's key points under SWOT-analysis four distinct headings: Sternghts, Weakneses, Opportunities and Threats

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

    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"], partial_variables={"format_instructions": parser.get_format_instructions()})


    return combine_prompt_template



def language_model():
    llm = ChatGroq(
    api_key= os.getenv("GROQ_API_KEY"),
    model_name="llama-3.2-90b-vision-preview",
    temperature=0.7
)
    return llm
    
def perform_swot_analysis(report):
    summary_chain = load_summarize_chain(llm=language_model(), chain_type='map_reduce',
                                        map_prompt=map_prompt(),
                                        combine_prompt=combine_prompt(),
                                        verbose=True)


    output = summary_chain.run(splitter(report))

    result_value = parser.parse(output)

    result_value = result_value

    return result_value


