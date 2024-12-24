import os
import google.generativeai as genai
import dotenv
from docx import Document  # To handle DOCX files

dotenv.load_dotenv()

# Configure the Generative AI client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    try:
        document = Document(docx_path)
        return "\n".join([paragraph.text for paragraph in document.paragraphs])
    except Exception as e:
        print("An error occurred while reading the DOCX file:", str(e))
        return None


def main():
    global file_id
    print("📚 Document Chatbot 🤖 (Supports PDF and DOCX)")

    # Prompt the user to upload a document
    doc_path = input("Enter the path to the document file (PDF or DOCX): ").strip()

    # Validate file path and extension
    if not os.path.isfile(doc_path):
        print("Invalid file path. Please try again.")
        return

    if not doc_path.lower().endswith(('.pdf', '.docx')):
        print("Unsupported file format. Please provide a PDF or DOCX file.")
        return

    try:
        if doc_path.lower().endswith('.docx'):
            # Extract text from DOCX and save it to a temporary file
            text_content = extract_text_from_docx(doc_path)
            if not text_content:
                print("Failed to process the DOCX file.")
                return

            # Save extracted text to a temporary text file
            tmp_text_file = "temp_text_file.txt"
            with open(tmp_text_file, "w", encoding="utf-8") as f:
                f.write(text_content)
            file_id = genai.upload_file(path=tmp_text_file)

            # Remove the temporary file after upload
            os.remove(tmp_text_file)

        elif doc_path.lower().endswith('.pdf'):
            # Upload the PDF directly
            file_id = genai.upload_file(path=doc_path)

        while True:
            # Get user input for questions
            user_input = input("\nAsk a question about the document (or type 'exit' to quit): ").strip()

            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            # Generate a response from the model
            response = model.generate_content([file_id, user_input])

            # Display the answer
            print("\nResponse:", response.text)

    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    main()
