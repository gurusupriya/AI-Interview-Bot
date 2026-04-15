from PyPDF2 import PdfReader

def extract_resume_text(uploaded_file):
    if not uploaded_file:
        return ""

    # If file is PDF
    if uploaded_file.name.lower().endswith(".pdf"):
        try:
            reader = PdfReader(uploaded_file)
            resume_text = ""
            for page in reader.pages:
                resume_text += page.extract_text() or ""
            return resume_text.strip()
        except:
            return ""

    # If file is TXT
    try:
        return uploaded_file.read().decode("utf-8", errors="ignore").strip()
    except:
        return ""
