"""Email Composer Tools for generating PDFs and sending emails."""

from typing import Dict, Optional
from google.adk.tools import ToolContext


def generate_profile_pdf(
    tool_context: ToolContext,
    format: str = "resume"
) -> Dict[str, str]:
    """Generate a PDF version of Bharath's profile.

    Args:
        tool_context: Tool execution context
        format: PDF format type (resume, full_profile, etc.)

    Returns:
        Dict with generation status and PDF path
    """
    try:
        import subprocess
        from datetime import datetime
        import os

        pdf_path = "/tmp/Bharath_Krishna_Profile.pdf"

        try:
            # Try using puppeteer/chromium via Node (if available)
            result = subprocess.run(
                [
                    "npx", "puppeteer", "print-to-pdf",
                    "http://localhost:3000",
                    pdf_path
                ],
                timeout=30,
                capture_output=True
            )

            if result.returncode != 0:
                # Fallback: use reportlab
                from reportlab.lib.pagesizes import letter
                from reportlab.pdfgen import canvas

                c = canvas.Canvas(pdf_path, pagesize=letter)
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, 750, "Bharath Krishna")
                c.setFont("Helvetica", 12)
                c.drawString(50, 730, "Full Stack Engineer & AgenticAI")
                c.drawString(50, 710, "Email: bharath.chakravarthi@gmail.com")
                c.drawString(50, 690, "Phone: +1-857-437-9316")
                c.drawString(50, 670, "Location: California, USA")
                c.drawString(50, 650, "Website: profile.krishb.in")

                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, 600, "Professional Summary")
                c.setFont("Helvetica", 10)
                summary = "Full stack engineer with 15+ years of experience building AgenticAI solutions and HPC clusters for LLM/ML training."
                c.drawString(50, 580, summary)

                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, 530, "Experience")
                c.setFont("Helvetica", 10)
                c.drawString(70, 510, "• Senior Software Engineer @ Rakuten USA (May 2022 - Feb 2026)")
                c.drawString(70, 490, "• Application Engineer @ Rakuten, Inc. Tokyo (Jan 2018 - May 2022)")
                c.drawString(70, 470, "• Application Engineer @ Rakuten India (Sep 2014 - Dec 2018)")

                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, 420, "Skills")
                c.setFont("Helvetica", 10)
                c.drawString(70, 400, "Languages: Python (15y), Golang (7y)")
                c.drawString(70, 380, "Infrastructure: Kubernetes (CKA), Terraform, Ansible, Docker, GCP")
                c.drawString(70, 360, "Backend: FastAPI, Gin Gonic, PostgreSQL, MongoDB")
                c.drawString(70, 340, "Expertise: LLMOps, DevOps, AgenticAI, HA Systems")

                c.save()
        except Exception:
            # Use reportlab as fallback
            try:
                from reportlab.lib.pagesizes import letter
                from reportlab.pdfgen import canvas

                c = canvas.Canvas(pdf_path, pagesize=letter)
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, 750, "Bharath Krishna")
                c.setFont("Helvetica", 12)
                c.drawString(50, 730, "Full Stack Engineer & AgenticAI")
                c.drawString(50, 710, "bharath.chakravarthi@gmail.com | +1-857-437-9316")
                c.drawString(50, 690, "California, USA | profile.krishb.in")
                c.save()
            except ImportError:
                raise Exception("PDF generation libraries (reportlab or puppeteer) not installed")

        return {
            "status": "success",
            "message": f"Profile PDF generated successfully",
            "pdf_path": pdf_path,
            "format": format
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating profile PDF: {str(e)}",
            "error_details": str(e)
        }


def send_email_with_attachment(
    tool_context: ToolContext,
    recipient_email: str,
    pdf_path: str,
    subject: str = "Bharath Krishna - Professional Profile (PDF)",
    custom_message: Optional[str] = None
) -> Dict[str, str]:
    """Send email with PDF attachment to a recipient.

    Args:
        tool_context: Tool execution context
        recipient_email: Email address to send to
        pdf_path: Path to the PDF file to attach
        subject: Email subject line
        custom_message: Optional custom message body

    Returns:
        Dict with email send status
    """
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email.mime.text import MIMEText
        from email import encoders
        import os
        from datetime import datetime

        sender_email = "bharath.krishb@gmail.com"
        sender_password = os.getenv("EMAIL_PASSWORD", "")

        if not sender_password:
            return {
                "status": "pdf_generated",
                "message": f"PDF is ready but email not configured",
                "pdf_path": pdf_path,
                "recipient": recipient_email,
                "note": "Email configuration not set. Configure EMAIL_PASSWORD env var."
            }

        # Create email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        body = custom_message or f"""Hello,

Please find attached Bharath Krishna's professional profile in PDF format.

Contact Information:
- Email: bharath.chakravarthi@gmail.com
- Phone: +1-857-437-9316
- Website: profile.krishb.in

This profile highlights his 15+ years of experience in full-stack engineering,
AgenticAI solutions, and high-availability systems.

Best regards,
Bharath's Assistant
"""
        msg.attach(MIMEText(body, 'plain'))

        # Attach PDF
        with open(pdf_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= "Bharath_Krishna_Profile.pdf"')
            msg.attach(part)

        # Send email via SMTP (Gmail)
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()

            return {
                "status": "success",
                "message": f"Profile PDF emailed successfully to {recipient_email}",
                "pdf_path": pdf_path,
                "recipient": recipient_email,
                "sent_at": datetime.now().isoformat()
            }
        except smtplib.SMTPException as e:
            return {
                "status": "pdf_generated",
                "message": f"PDF generated but email failed: {str(e)}",
                "pdf_path": pdf_path,
                "recipient": recipient_email,
                "note": "PDF is ready. Please configure EMAIL_PASSWORD env var for email sending."
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error sending email: {str(e)}",
            "error_details": str(e)
        }
