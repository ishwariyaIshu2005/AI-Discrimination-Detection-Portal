from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(
    filename,
    text,
    result,
    severity
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Discrimination Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1,20)
    )

    content.append(
        Paragraph(
            f"Input Text: {text}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Result: {result}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Severity Score: {severity}",
            styles["BodyText"]
        )
    )

    doc.build(content)

    return filename