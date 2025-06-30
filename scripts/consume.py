import os
import fitz  # PyMuPDF
# import google.generativeai as genai
from google.cloud import aiplatform
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# --- Configuration ---
# Replace with your actual credentials and IDs
GEMINI_API_KEY = "AIzaSyCeh5HfOX0i691vQILMKiWrX14Q4CxnLxE"
GOOGLE_CLOUD_PROJECT = "agents-stg"
LOCATION = "us-central1"  # e.g., "us-central1"
CORPUS_ID = "YOUR_CORPUS_ID"
LOCAL_FOLDER_PATH = "./data"

# --- Initialize Google Cloud and Gemini ---
# genai.configure(api_key=GEMINI_API_KEY)
aiplatform.init(project=GOOGLE_CLOUD_PROJECT, location=LOCATION)

def create_pdf_from_text(text, output_filename):
    """Creates a PDF file from a given text string."""
    c = canvas.Canvas(output_filename, pagesize=letter)
    _width, height = letter
    text_object = c.beginText(40, height - 40)
    text_object.setFont("Times-Roman", 12)
    for line in text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    c.save()
    print(f"Created PDF: {output_filename}")

def upload_to_vertex_rag(file_path, corpus_id):
    """Uploads a file to the specified Vertex AI RAG corpus."""
    try:
        # Implementation for Vertex AI RAG upload would go here.
        # As of the current Gemini and Vertex AI SDKs, a direct 'upload_file'
        # to a RAG corpus is managed differently, often through associating
        # a storage bucket. For this example, we'll simulate the upload.
        print(f"Uploading {file_path} to Vertex AI RAG Corpus ID: {corpus_id}")
        # In a real scenario, you would use the Vertex AI SDK to manage
        # resources in your RAG corpus. This might involve uploading to
        # a GCS bucket that is connected to your RAG engine.
    except Exception as e:
        print(f"Error uploading to Vertex AI RAG: {e}")

def process_image(image_bytes, corpus_id):
    """Uses Gemini API to understand an image and uploads the response as a PDF."""
    print('processing image...')
    # try:
    #     image_part = {"mime_type": "image/png", "data": image_bytes}
    #     model = genai.GenerativeModel('gemini-pro-vision')
    #     response = model.generate_content(["Describe the image.", image_part])

    #     if response.text:
    #         output_pdf_path = "processed_image_description.pdf"
    #         create_pdf_from_text(response.text, output_pdf_path)
    #         upload_to_vertex_rag(output_pdf_path, corpus_id)
    #         os.remove(output_pdf_path)
    # except Exception as e:
    #     print(f"Error processing image with Gemini: {e}")

def process_pdf(file_path, corpus_id):
    """Extracts text and images from a PDF, processes images, and uploads the PDF."""
    try:
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                print(f"Processing image {img_index+1} from page {page.number + 1}...")
                process_image(image_bytes, corpus_id)

        # In this example, we are not creating a new PDF from the extracted text.
        # The original PDF is uploaded directly.
        upload_to_vertex_rag(file_path, corpus_id)

    except Exception as e:
        print(f"Error processing PDF {file_path}: {e}")

# def process_media(file_path, corpus_id, media_type):
#     """Uses Gemini API for audio/video understanding and uploads the response as a PDF."""
#     try:
#         print(f"Uploading {media_type} file for processing: {file_path}")
#         media_file = genai.upload_file(path=file_path)
#         model = genai.GenerativeModel('gemini-pro-vision' if media_type == "video" else "gemini-pro")
#         prompt = f"Summarize this {media_type}."
#         response = model.generate_content([prompt, media_file])

#         if response.text:
#             output_pdf_path = f"processed_{media_type}_description.pdf"
#             create_pdf_from_text(response.text, output_pdf_path)
#             upload_to_vertex_rag(output_pdf_path, corpus_id)
#             os.remove(output_pdf_path)

#     except Exception as e:
#         print(f"Error processing {media_type} file {file_path}: {e}")

def main():
    """Main function to iterate through the local folder and process files."""
    for filename in os.listdir(LOCAL_FOLDER_PATH):
        file_path = os.path.join(LOCAL_FOLDER_PATH, filename)
        if os.path.isfile(file_path):
            if filename.lower().endswith(".pdf"):
                print(f"--- Processing PDF: {filename} ---")
                process_pdf(file_path, CORPUS_ID)
            elif filename.lower().endswith(".mp3"):
                print(f"--- Processing MP3: {filename} ---")
                process_media(file_path, CORPUS_ID, "audio")
            elif filename.lower().endswith(".mp4"):
                print(f"--- Processing MP4: {filename} ---")
                process_media(file_path, CORPUS_ID, "video")
            else:
                print(f"--- Skipping unsupported file: {filename} ---")

if __name__ == "__main__":
    main()