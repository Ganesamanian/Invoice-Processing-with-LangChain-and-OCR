# Invoice Processing with LangChain and OCR

This repository provides a Python-based solution for extracting structured information from invoices using a combination of LangChain, OCR (Optical Character Recognition), and Google Generative AI models. The script is capable of handling both text-based and scanned PDF invoices, extracting critical information in JSON format for easy integration into downstream systems.

## Features

- **Text and Scanned PDF Support**: Handles both text-based PDFs and scanned images by leveraging PyPDFLoader and Tesseract OCR.
- **Information Extraction**: Extracts the following information:
  - **General Data**: Invoice number, date, period, payment due date, order details.
  - **Supplier & Customer Data**: Name, address, city, postal code, country, VAT and tax numbers.
  - **Item Data**: Product/service description, quantity, net amount, VAT rate, VAT amount, and gross amount.
  - **Total Amount**: Total net amount, VAT details, and gross amount.
- **Customizable Prompt Templates**: Leverages LangChain's prompt templates for structured data extraction.
- **Clean JSON Output**: Ensures extracted data is output in a clean JSON format for easy processing.
- **Flexible LLM Integration**: Uses Google Generative AI (Gemini models) for natural language processing.

## Prerequisites

1. **Python Environment**: Python 3.8+

2. **Dependencies**: Install required libraries by running:

   ```bash
   pip install -r requirements.txt
   ```

3. **API Keys**:

   - `google_api_key`: Your Google API key for Generative AI integration.

4. **Tesseract OCR**: Install Tesseract OCR for text extraction from scanned PDFs. For installation:

   - **Linux**: `sudo apt install tesseract-ocr`
   - **MacOS**: `brew install tesseract`
   - **Windows**: [Download installer](https://github.com/tesseract-ocr/tesseract)

## Directory Structure

```plaintext
.
|-- Invoices/               # Directory containing invoice PDFs
|-- main.py                 # Main script file
|-- requirements.txt        # Python dependencies
|-- README.md               # Project documentation
```

## Usage

1. **Place Invoice Files**: Store your invoice PDFs in the `Invoices/` directory.

2. **Run the Script**: Update the `pdf_file_path` variable in the `langchain_helper` function to the path of your invoice file and execute the script:

   ```bash
   python main.py
   ```

3. **Output**: The extracted data will be returned as a JSON object containing the following keys:

   - `General_data`
   - `Supplier_customer_data`
   - `Item_data`
   - `Total_amount`

## Functionality Overview

### 1. `clean_json_string(json_str)`

Cleans and preprocesses raw JSON strings to ensure proper formatting and decoding.

### 2. `extract_text_from_scanned_pdf(pdf_path)`

Uses Tesseract OCR to extract text from scanned PDF files.

### 3. `langchain_helper(pdf_file_path)`

Main function that:

- Loads the PDF document.
- Applies OCR if the document content is empty.
- Utilizes LangChain prompt templates and Google Generative AI models to extract structured information.
- Returns the result in JSON format.

## Prompt Templates

- General Data Extraction
- Supplier & Customer Data Extraction
- Item Data Extraction
- Total Amount Extraction

Each template ensures consistency and accuracy in extracting relevant invoice details.

## Example Output

```json
{
  "General_data": {
    "Invoice number": "12345",
    "Invoice date": "2024-03-06",
    "Invoice period": "None",
    "Payment due date": "2024-03-20",
    "Order number": "98765",
    "Order date": "2024-03-01"
  },
  "Supplier_customer_data": {
    "Supplier Name": "Modelwerk Modelagentur GmbH",
    "Supplier Address": "Street 123",
    "Supplier City": "Hamburg",
    "Supplier Postal code": "20095",
    "Supplier Country": "Germany",
    "Supplier VAT Number": "DE123456789",
    "Supplier Tax number": "None",
    "Customer Name": "ABC Company",
    "Customer Address": "Avenue 456",
    "Customer City": "Berlin",
    "Customer Postal code": "10115",
    "Customer Country": "Germany",
    "Customer VAT Number": "None",
    "Customer Tax number": "None"
  },
  "Item_data": [
    {
      "Service or product description": "Modeling services",
      "Service or product quantity": "1",
      "Service or product net amount": "120.00",
      "Service or product VAT rate": "19%",
      "Service or product VAT amount": "22.80",
      "Service or product gross amount": "142.80"
    }
  ],
  "Total_amount": {
    "Total net amount": "120.00",
    "Total net amount tax free": "None",
    "Total net amount per each VAT": ["120.00"],
    "Total VAT amount per each VAT": ["22.80"],
    "Total VAT amount": "22.80",
    "Total gross amount": "142.80"
  }
}
```

## Future Improvements

- Explore layout processing
- Add support for multi-language OCR.
- Enhance error handling for edge cases in invoice formatting.
- Introduce database integration for automated storage of extracted data.

## Contributions

Feel free to contribute to this repository by submitting issues or pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

For any queries or assistance, please contact kganesamanianthanu@gmail.com.

