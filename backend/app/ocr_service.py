import os
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
API_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

if not ENDPOINT or not API_KEY:
    raise ValueError("The environment variables AZURE_FORM_RECOGNIZER_ENDPOINT and AZURE_FORM_RECOGNIZER_KEY are not set")

client = DocumentAnalysisClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(API_KEY)
)

def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extracts text from an image using Azure Form Recognizer.

    Args:
        image_bytes: Bytes of the image to analyze

    Returns:
        Extracted text from the image
    """
    try:
        poller = client.begin_analyze_document(
            "prebuilt-read", document=image_bytes
        )
        result = poller.result()
        
        text = ""
        for page in result.pages:
            for line in page.lines:
                text += line.content + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error analyzing document: {str(e)}")