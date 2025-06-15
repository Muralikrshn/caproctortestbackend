import fitz
import re
import json

filepath = r"C:\Users\murha\OneDrive\Desktop\CA foundation material\cpu1-2merged.pdf"
def extractPdfText(filepath):
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

def smart_chunker(text):
  pattern = r'(?m)^\s(\d+(?:\.\d+)*)\s([A-Z\s,&\-]+)$'
  matches = re.finditer(f"{pattern}", text)
  chunks = []
  positions = [match.start() for match in matches]
  positions.append(len(text))  # end boundary

  for i in range(len(positions) - 1):
      chunk = text[positions[i]:positions[i+1]].strip()
      chunks.append(chunk)
  
  return chunks

text = extractPdfText(filepath)
chunks = smart_chunker(text)
print("Length:",len(chunks))

with open("output.txt", "w", encoding="utf-8") as f:
    f.write("".join(text))

with open("chunk.txt","w", encoding="utf-8") as f:
    f.write(chunks[6])

# Step 3: Convert chunks into JSON-friendly format
def convert_to_json_chunks(chunks):
    json_chunks = []
    for chunk in chunks:
        match = re.match(r'^\s*(\d+(?:\.\d+)*)\s+([A-Z][A-Z\s,&\-]*)', chunk)
        if match:
            title = match.group(0).strip()
            content = chunk[len(title):].strip()
            json_chunks.append({
                "title": title,
                "content": content
            })
    return json_chunks

# Convert to JSON and store
json_chunks = convert_to_json_chunks(chunks)

def save_to_json_file(json_data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print("Saved JSON pdfextractor.pychunks successfully.")
