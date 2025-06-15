# import re
# from pdfextractor import extractPdfText

# # pattern = r'(?m)^\s(\d+(?:\.\d+)*)\s([A-Z\s,&\-]+)$'
# def findMatches(pattern, filepath):
#   l = []
#   try: 
#     for match in re.finditer(pattern, extractPdfText(filepath)):
#       l.append(match.group(0))
#   except Exception as e:
#     return f"Error processing file {filepath}: {e}"
#   return l


sj = {    "load_chunks": "utility/utilities.load_chunks",
     "load_model": "utility/utilities.load_model",}
print(type(sj))