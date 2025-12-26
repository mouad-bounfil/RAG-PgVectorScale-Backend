import os
from typing import List, Dict
import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
from google.genai import types
from dotenv import load_dotenv
import io

load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model = "gemini-2.5-flash"


# RecursiveCharacterTextSplitter splits long texts into smaller overlapping chunks.
# Arguments:
#   chunk_size: Maximum number of characters in each chunk (here, 1200 chars per chunk)
#   chunk_overlap: Number of characters that overlap between adjacent chunks (here, 200 chars overlap)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,  # Each chunk will be up to 1200 characters
    chunk_overlap=50,  # 200 characters of overlap between consecutive chunks
)


def pdf_to_text(pdf_path: str) -> List[Dict]:
    """Extract text from PDF using Gemini OCR"""
    images = convert_from_path(pdf_path)
    results = []

    for i in range(len(images)):
        print(f"Processing page {i + 1}/{len(images)}...")

        # Preprocess image for better OCR
        image = np.array(images[i])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
        image = Image.fromarray(thresh)

        # Convert PIL Image to bytes for Gemini
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_bytes = img_byte_arr.getvalue()

        # Use Gemini to extract text
        try:
            response = client.models.generate_content(
                model=model,
                contents=[
                    types.Content(
                        parts=[
                            types.Part(
                                inline_data=types.Blob(
                                    mime_type="image/png", data=img_bytes
                                )
                            ),
                            types.Part(
                                text="Extract all the text from this image. Return only the extracted text, no additional commentary."
                            ),
                        ]
                    )
                ],
            )
            text = response.text
            print(f"✓ Page {i + 1} extracted successfully")
        except Exception as e:
            print(f"✗ Error extracting text from page {i + 1}: {e}")
            text = ""

        results.append({"page": i + 1, "text": text})

    return results


def process_pdf(pdf_path: str) -> None:
    results = pdf_to_text(pdf_path)
    documents = []
    for result in results:
        page = result["page"]
        text = result["text"]
        chunks = splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            doc_id = f"p-{page}-chunk-{i}"
            documents.append(
                {
                    "page_content": chunk,
                    "metadata": {"page": page, "chunk_index": i, "chunk_id": doc_id},
                    "id": doc_id,
                }
            )
    return documents
