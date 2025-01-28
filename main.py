#!/usr/bin/env python
# coding: utf-8

import re
import os
import json
from pytesseract import image_to_string
from pdf2image import convert_from_path
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI


# Define a function to clean the JSON string
def clean_json_string(json_str):
    try:
        # Replace problematic escape sequences
        json_str = json_str.replace('\xa0', ' ')  # Handle non-breaking spaces
        json_str = re.sub(r'^```json|```$', '', json_str, flags=re.MULTILINE)
        # json_str = json_str.encode('utf-8').decode('raw_unicode_escape')  # Decode escape sequences
        # return json_str
        return json_str.strip()
    except Exception as e:
        raise ValueError(f"Error cleaning JSON string: {e}")

# Custom JSON output parser
class CleanJsonOutputParser(JsonOutputParser):
    def parse(self, text: str):
        try:
            text = clean_json_string(text)
            return super().parse(text)
        except Exception as e:
            raise ValueError(f"Error parsing JSON: {e}")


# OCR method for scanned pdf
def extract_text_from_scanned_pdf(pdf_path):
    try:
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        extracted_text = []
        for img in images:
            # Use Tesseract OCR to extract text from image
            text = image_to_string(img, lang='eng')#lang='deu'
            extracted_text.append(text)
        return "\n".join(extracted_text)
    except Exception as e:
        raise ValueError(f"Error extracting text from scanned PDF: {e}")

# Main function
def langchain_helper(pdf_file_path):
    
    # Initialize the PyPDFLoader with the file path
    loader = PyPDFLoader(pdf_file_path)
    
    try:
        # Load documents from the PDF
        documents = loader.load()
        if not documents or not documents[0].page_content.strip():  # Check if page_content is empty
            raise ValueError("Page content is empty")
    except ValueError:
        # If text extraction fails, check OCR
        print("Trying OCR")
        documents = extract_text_from_scanned_pdf(pdf_file_path)

    
    google_api_key = os.getenv("google_api_key")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b")

    prompt_general = PromptTemplate.from_template(
        """
        ### INVOICE:
        {page_data}

        ### INSTRUCTION:
        Extract the following general data from the invoice:
        General data:
        - Invoice number
        - Invoice date
        - Invoice period (not available on all invoices)
        - Payment due date (not available on all invoices)
        - Order number (not available on all invoices)
        - Order date (not available on all invoices)

        If data are not available, the data should be "None"
        if there is multiple invoices then provide details for all
        Output the information in JSON format with the above mentioned keys.        
        No PREAMBLE
        """
    )
    chain_general = prompt_general | llm
    response_general = chain_general.invoke(input={'page_data': documents})
    

    prompt_customer_supplier = PromptTemplate.from_template(
        """
        ### INVOICE:
        {page_data}

        ### INSTRUCTION:
        Extract the following supplier data from the invoice:
        Supplier data:
        - Supplier Name
        - Supplier Address 
        - Supplier City
        - Supplier Postal code
        - Supplier Country (not available on all invoices)            
        - Supplier VAT Number (not available on all invoices)
        - Supplier Tax number (not available on all invoices)

        Extract the following customer data from the invoice:
        Customer data:
        - Customer Name (not available on all invoices)
        - Customer Address (not available on all invoices)
        - Customer City (not available on all invoices)
        - Customer Postal code (not available on all invoices)
        - Customer Country (not available on all invoices)            
        - Customer VAT Number (not available on all invoices)
        - Customer Tax number (not available on all invoices)

        If the shipping address is available then extract as follows
        Customer Shipping data:
        - Customer Shipping Name (not available on all invoices)
        - Customer Shipping Address (not available on all invoices)
        - Customer Shipping City (not available on all invoices)
        - Customer Shipping Postal code (not available on all invoices)
        - Customer Shipping Country (not available on all invoices)            
        - Customer Shipping VAT Number (not available on all invoices)
        - Customer Shipping Tax number (not available on all invoices)

        If data are not available, the data should be "None"
        Output the information in JSON format with the above mentioned keys.        
        No PREAMBLE
        """
    )
    chain_customer_supplier = prompt_customer_supplier | llm
    response_customer_supplier = chain_customer_supplier.invoke(input={'page_data': documents})
    

    prompt_item = PromptTemplate.from_template(
        """
        ### INVOICE:
        {page_data}

        ### INSTRUCTION:
        Extract the following each item data from the invoice:
        Item data:
        - Service or product description
        - Service or product quantity
        - Service or product net amount 
        - Service or product VAT rate 
        - Service or product VAT amount
        - Service or product gross amount

        If data are not available, the data should be "None"
        use values only from the invoice, should not make up any values on your own
        Output the information in JSON format with the above mentioned keys.        
        No PREAMBLE
        """
    )
    chain_item = prompt_item | ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
    response_item = chain_item.invoke(input={'page_data': documents})
    

    prompt_total = PromptTemplate.from_template(
        """
        ### INVOICE:
        {page_data}

        ### INSTRUCTION:
        Extract the following total amomut data from the invoice:
        Total invoice amount:
        - Total net amount # Provide the amount before inclusion of tax
        - Total net amount tax free (not available on all invoices)
        - Total net amount per each VAT # provide each product/service amount as list before tax
        - Total VAT amount per each VAT # provide each product/service tax value as list
        - Total VAT amount # Give total VAT amount
        - Total gross amount # Provide the amount after inclusion of tax

       
        Statement from the invoice (usually available below the Total gross amount) 
        where VAT has not been charged, Total VAT amount = 0  (not available on all invoices)
        use values only from the invoice, should not make up any values on your own
        If data are not available, the data should be "None"
        Output the information in JSON format with the above mentioned keys.        
        No PREAMBLE
        """
    )
    chain_total = prompt_total | ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
    response_total = chain_total.invoke(input={'page_data': documents})
   

    json_parser = CleanJsonOutputParser()
    merged_result = {
        "General_data": json_parser.parse(response_general.content),
        "Supplier_customer_data": json_parser.parse(response_customer_supplier.content),
        "Item_data": json_parser.parse(response_item.content),
        "Total_amount": json_parser.parse(response_total.content)
    }
    
    
    return merged_result

pdf_file_path = "Invoices/BA85351306"
result = langchain_helper(pdf_file_path)
print(result)

