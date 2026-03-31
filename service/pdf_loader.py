from PyPDF2 import PdfReader

def load_pdf(path):
    reader = PdfReader(path)
    text=""

    for page in reader.pages:
        text+=page.extract_text()
    return text 

if __name__ == "__main__":
    print(load_pdf(r"C:\\Users\\HP\\Downloads\\1.pdf"))