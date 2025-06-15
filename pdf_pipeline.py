import pdfextractorcopy
import json
import os # Import os for file path checks

def process_pdf_to_chunks(pdf_path: str, json_output_path: str):
    # It's good practice to ensure the directory exists before trying to save
    # the JSON file. You might also want to check if json_output_path exists
    # instead of hardcoding 'chunks.json' for reading.

    # Let's refactor to use json_output_path for both reading and writing,
    # assuming it's the target file for chunks.
    target_json_file = json_output_path

    # Check if the target JSON file exists and has content
    if os.path.exists(target_json_file) and os.path.getsize(target_json_file) > 0:
        try:
            with open(target_json_file, "r", encoding="utf-8") as f: # Specify UTF-8 encoding
                data = json.load(f)
                if data:
                    print(f"Chunks already exist in {target_json_file}. Skipping PDF processing.")
                    return # Exit the function if data is found
                else:
                    print(f"File {target_json_file} exists but is empty. Proceeding with extraction.")
        except json.JSONDecodeError:
            print(f"Warning: {target_json_file} is malformed or empty, proceeding with extraction.")
        except UnicodeDecodeError:
            print(f"Warning: {target_json_file} has encoding issues, proceeding with extraction.")
        except Exception as e:
            print(f"An unexpected error occurred while reading {target_json_file}: {e}")
    else:
        print(f"File {target_json_file} does not exist or is empty. Proceeding with extraction.")

    # If we reached here, it means the file was either empty, didn't exist,
    # or had issues, so we proceed with extraction.
    try:
        extractor = pdfextractorcopy.PDFExtractor(pdf_path)
        text = extractor.extractPdfText(pdf_path)
        chunks = extractor.smart_chunker(text)
        json_chunks = extractor.convert_to_json_chunks(chunks)

        # Ensure the directory for json_output_path exists
        os.makedirs(os.path.dirname(json_output_path), exist_ok=True)

        extractor.save_to_json_file(json_chunks, json_output_path)
        print(f"Chunks saved to {json_output_path}")
    except Exception as e:
        print(f"Error during PDF processing and chunking: {e}")

# Example usage (assuming these variables are defined in your main.py)
# pdf_path = r"C:\Users\murha\OneDrive\Desktop\cahelpertest\your_document.pdf"
# json_path = r"C:\Users\murha\OneDrive\Desktop\cahelpertest\chunks.json"
# process_pdf_to_chunks(pdf_path, json_path)