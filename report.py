from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

def create_pdf(questions, answers, scores, feedbacks, avg):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            leftMargin=40, rightMargin=40,
                            topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    heading = styles["Heading2"]

    story = []

    # Title
    story.append(Paragraph("<b>Final Interview Report</b>", heading))
    story.append(Spacer(1, 12))

    # Loop all Q&A
    for i, (q, a, s, fb) in enumerate(zip(questions, answers, scores, feedbacks)):
        story.append(Paragraph(f"<b>Q{i+1}:</b> {q}", normal))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"<b>Your Answer:</b> {a}", normal))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"<b>Score:</b> {s}/10", normal))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"<b>Feedback:</b> {fb}", normal))
        story.append(Spacer(1, 14))

    # Final Overall Score
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b> Overall Score:</b> {avg:.2f}/10", normal))

    doc.build(story)
    buffer.seek(0)
    return buffer
