import fitz
import re
import json
class PDFExtractor:
    def __init__(self, filepath):
        self.filepath = filepath

    def extractPdfText(self, filepath):
        try:
            doc = fitz.open(filepath)
            pageCount = doc.page_count
            print(f"Total Pages: {pageCount}")
            text = ""
            for page in range(pageCount):
                try:
                    page = doc.load_page(page)
                    text += page.get_text("text")
                except Exception as e:
                    print(f"Error processing page {page}: {e}")
                    continue
            doc.close()
            # print(text)
            print("finished extracting")
            return text
        except Exception as e:
            return f"Error Extracting pdf text {filepath}: {e}"
    
    def smart_chunker(self, text):
        try:
            pattern = r'(?m)^\s(\d+(?:\.\d+)*)\s([A-Z\s,&\-]+)$'
            matches = re.finditer(f"{pattern}", text)
            chunks = []
            positions = [match.start() for match in matches]
            positions.append(len(text))  # end boundary

            for i in range(len(positions) - 1):
                chunk = text[positions[i]:positions[i+1]].strip()
                chunks.append(chunk)
            print(f"Total Chunks: {len(chunks)}")
            return chunks
        except Exception as e:
            return f"Error chunking chunk list: {e}"

    def convert_to_json_chunks(self, chunks):
        try:
            json_chunks = []
            i = 1
            for chunk in chunks:
                match = re.match(r'^\s*(\d+(?:\.\d+)*)\s+([A-Z][A-Z\s,&\-]*)', chunk)
                if match:
                    title = match.group(0).strip()
                    content = chunk[len(title):].strip()
                    json_chunks.append({
                        "chunk_id": i,
                        "title": title,
                        "content": content
                    })
                i+=1
                
            print(f"Total JSON Chunks: {len(json_chunks)}")
            return json_chunks
        except Exception as e:
            return f"Error converting chunks to JSON chunks: {e}"
    
    def save_to_json_file(self, json_data, filename):
        try:

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
                print("Saved JSON pdfextractor.pychunks successfully.")
        except Exception as e:
            return f"Error saving JSON data to file {filename}: {e}"
        


