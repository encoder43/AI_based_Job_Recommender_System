import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text_from_pdf(pdf_file_bytes: bytes) -> str:
    """Extracts text from a PDF file's bytes."""
    text = ""
    try:
        # Open PDF from bytes
        doc = fitz.open(stream=pdf_file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
    return text

def ask_groq(prompt: str, max_tokens: int = 500) -> str:
    """Sends a prompt to the Groq API and returns the response."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant", # Fast and capable model
            temperature=0.5,
            max_tokens=max_tokens,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "Error: Could not get a response from the AI model."