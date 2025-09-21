import pandas as pd
from io import BytesIO
import docx
from PyPDF2 import PdfReader

def load_data(file):
    """
    Loads data from a supported file type into a Pandas DataFrame.
    """
    file_extension = file.name.split('.')[-1].lower()

    if file_extension == 'csv':
        return pd.read_csv(file)
    elif file_extension in ['xls', 'xlsx']:
        return pd.read_excel(file, engine='openpyxl')
    elif file_extension == 'txt':
        # Reads the entire text content and creates a single-column DataFrame
        text_content = file.read().decode('utf-8')
        return pd.DataFrame({"content": [text_content]})
    elif file_extension == 'docx':
        doc = docx.Document(BytesIO(file.read()))
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        # Create a single-column DataFrame from all paragraphs
        return pd.DataFrame({"content": ["\n".join(full_text)]})
    elif file_extension == 'pdf':
        reader = PdfReader(BytesIO(file.read()))
        text_content = ""
        # Loop through all pages and extract text
        for page in reader.pages:
            text_content += page.extract_text() + "\n"  # Add a newline for readability

        # Create a single-column DataFrame with all the extracted text
        return pd.DataFrame({"content": [text_content]})
    else:
        raise ValueError("Unsupported file type")