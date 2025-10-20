import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

client = AzureOpenAI(
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY
)

def analyze_acta(texto: str) -> str:
    """
    Sends the text of the act (including OCR from images) to Azure OpenAI for analysis
    """
    prompt = f"""
    Analiza el siguiente texto de un acta legislativa.
    1. Indica si trata temas financieros (bancos, cooperativas, financieras, BAC, etc.)
    2. Genera un resumen general.
    3. Si hay temas financieros, genera un resumen específico de esas partes.

    Establece claramente las secciones en tu respuesta: 
    - Resumen General
    - Temas Financieros (indicar si los hay, en caso afirmativo, incluye tambien el resumen). El resumen
    financiero debe ser claro, detallado y específico de las secciones relevantes.

    Responde en formato json con las claves: "resumen_general", "temas_financieros" (booleano), "resumen_financiero" (si aplica)
    pero no pongas json ''', solo el contenido en un formato que pueda ser formateado por un parser de json de javascript. 

    La respuesta debe ser detallada y extensa en el resumen general y en el financiero debe ser claro, detallado y específico.

    Texto:
    {texto[:10000]}  # límite por tokens
    """

    print("=================================")
    print("Prompt:", prompt)
    print("Azure OpenAI Endpoint:", AZURE_OPENAI_ENDPOINT)
    print("Azure OpenAI Key:", AZURE_OPENAI_KEY)
    print("Azure OpenAI Deployment:", AZURE_OPENAI_DEPLOYMENT)
    print("Azure OpenAI API Version:", AZURE_OPENAI_API_VERSION)

    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "Eres un asistente especializado en análisis de actas legislativas y temas financieros."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,
            temperature=0.7,
            top_p=1.0
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error in analyze_acta: {e}")
        return f"Error analyzing act: {e}"