"""Generate a professional PDF resume for Bharath Krishna – AI Architect profile."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)


# Colors
NAVY = HexColor("#1B2A4A")
DARK_BLUE = HexColor("#2C3E6B")
ACCENT = HexColor("#3B82F6")
PILL_BG = HexColor("#EEF2FF")
DARK_GRAY = HexColor("#333333")
MED_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
WHITE = HexColor("#FFFFFF")

# Styles
style_name = ParagraphStyle("Name", fontSize=26, leading=32, textColor=WHITE, fontName="Helvetica-Bold")
style_title = ParagraphStyle("Title", fontSize=13, leading=18, textColor=HexColor("#A8C4F0"), fontName="Helvetica")
style_contact = ParagraphStyle("Contact", fontSize=9, leading=14, textColor=HexColor("#C8D8F0"), fontName="Helvetica")
style_section = ParagraphStyle("Section", fontSize=13, leading=18, textColor=NAVY, fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=4)
style_body = ParagraphStyle("Body", fontSize=9.5, leading=14, textColor=DARK_GRAY, fontName="Helvetica")
style_body_italic = ParagraphStyle("BodyItalic", fontSize=9.5, leading=14, textColor=MED_GRAY, fontName="Helvetica-Oblique")
style_job_title = ParagraphStyle("JobTitle", fontSize=10.5, leading=15, textColor=DARK_BLUE, fontName="Helvetica-Bold")
style_job_company = ParagraphStyle("JobCompany", fontSize=9.5, leading=13, textColor=ACCENT, fontName="Helvetica-Bold")
style_job_date = ParagraphStyle("JobDate", fontSize=8.5, leading=12, textColor=LIGHT_GRAY, fontName="Helvetica-Oblique")
style_bullet = ParagraphStyle("Bullet", fontSize=9, leading=13, textColor=MED_GRAY, fontName="Helvetica", leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
style_skill_cat = ParagraphStyle("SkillCat", fontSize=9, leading=13, textColor=NAVY, fontName="Helvetica-Bold")
style_skill_val = ParagraphStyle("SkillVal", fontSize=9, leading=13, textColor=MED_GRAY, fontName="Helvetica")
style_summary = ParagraphStyle("Summary", fontSize=10, leading=15, textColor=DARK_GRAY, fontName="Helvetica", spaceAfter=6)


def section_header(text):
    return KeepTogether([
        Paragraph(text.upper(), style_section),
        HRFlowable(width="100%", thickness=2, color=ACCENT, spaceBefore=0, spaceAfter=8),
    ])


def build_header():
    name = Paragraph("BHARATH KRISHNA", style_name)
    title = Paragraph("AI Architect &amp; Full Stack Engineer", style_title)
    contact_left = Paragraph('<font size="9">+1-857-437-9316&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;bharath.chakravarthi@gmail.com</font>', style_contact)
    contact_right = Paragraph('<font size="9">profile.krishb.in&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;California, USA</font>', style_contact)

    inner = Table([[name], [title], [Spacer(1, 4)], [contact_left], [contact_right]], colWidths=["100%"])
    inner.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    header_table = Table([[inner]], colWidths=[7.5 * inch])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 20), ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("TOPPADDING", (0, 0), (-1, -1), 18), ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [6, 6, 6, 6]),
    ]))
    return header_table


def build_competencies():
    pills = ["AI Architecture", "LLMOps", "MLOps", "AgenticAI", "Kubernetes"]
    cells = [Paragraph(f'<font color="{DARK_BLUE.hexval()}" size="9"><b>{p}</b></font>',
             ParagraphStyle("pill", alignment=TA_CENTER, leading=14)) for p in pills]
    t = Table([cells], colWidths=[1.4 * inch] * len(pills))
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PILL_BG),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [4, 4, 4, 4]),
    ]))
    return t


def build_skills():
    skills = [
        ("AI / ML", "PyTorch, LLM Deployment, AgenticAI Protocols, NLP, Model Serving"),
        ("Programming", "Python (15 yrs), Golang (7 yrs)"),
        ("MLOps & Infra", "Kubernetes (CKA), Docker, Ansible, Terraform, GCP"),
        ("Data & Backend", "PostgreSQL, MongoDB, FastAPI, Gin Gonic, Apache Airflow"),
        ("Frontend", "React, NextJS, ChakraUI"),
    ]
    rows = [[Paragraph(cat, style_skill_cat), Paragraph(val, style_skill_val)] for cat, val in skills]
    t = Table(rows, colWidths=[1.4 * inch, 5.6 * inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, HexColor("#E0E0E0")),
    ]))
    return t


def build_experience_entry(title, company, date, bullets):
    elements = [
        Paragraph(title, style_job_title),
        Paragraph(company, style_job_company),
        Paragraph(date, style_job_date),
        Spacer(1, 3),
    ]
    for b in bullets:
        elements.append(Paragraph(f"\u2022&nbsp;&nbsp;{b}", style_bullet))
    elements.append(Spacer(1, 8))
    return KeepTogether(elements)


def build_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
        leftMargin=0.5*inch, rightMargin=0.5*inch,
        topMargin=0.4*inch, bottomMargin=0.4*inch)
    story = []

    story.append(build_header())
    story.append(Spacer(1, 12))

    # Professional Summary – tailored for AI Architect
    story.append(section_header("Professional Summary"))
    story.append(Paragraph(
        "AI-focused architect and full stack engineer with 15+ years of experience designing and deploying "
        "enterprise-scale AI/ML systems. Currently leading AgenticAI solution development and LLM deployment "
        "infrastructure on high-performance Kubernetes clusters. Deep expertise in MLOps pipelines, model "
        "serving LLMs via vllm, sglang, and end-to-end AI solution architecture spanning GenAI and AgenticAI "
        "frameworks and protocols, and production model monitoring.", style_summary))
    story.append(Spacer(1, 4))
    story.append(build_competencies())
    story.append(Spacer(1, 12))

    # Technical Skills – AI/ML first
    story.append(section_header("Technical Skills"))
    story.append(build_skills())
    story.append(Spacer(1, 6))

    # Work Experience – bullets reframed for AI architecture
    story.append(section_header("Work Experience"))
    experiences = [
        ("Senior Software Engineer", "Rakuten USA", "May 2022 \u2013 Feb 2026", [
            "Architecting and deploying AgenticAI solutions and LLM-based systems at enterprise scale",
            "Developing agentic applications using A2A and MCP protocols with CopilotKit",
            "Designing MLOps pipelines for model training, serving, and monitoring on HPC clusters",
            "Managing high-performance Kubernetes clusters for distributed ML workloads",
            "Developing UI/API/CLI tools for HPC cluster training job submission and orchestration",
            "Infrastructure automation using Terraform/Ansible; model deployment lifecycle management",
            "Custom Kubernetes operator development for AI workload scheduling; team leadership",
        ]),
        ("Application Engineer", "Rakuten, Inc. \u2014 Tokyo", "Jan 2018 \u2013 May 2022", [
            "Designed Infrastructure-as-Code solutions with Terraform/Ansible for scalable compute",
            "Developed custom Terraform plugins and GoLang SDKs for platform automation",
            "Built REST API toolkits (FastAPI/Gin) powering internal AI platform services",
            "Implemented authentication services and load testing frameworks",
        ]),
        ("Application Engineer", "Rakuten India", "Sep 2014 \u2013 Dec 2018", [
            "API development for IaaS (VMware), DNS, and Load Balancer infrastructure",
            "Led 3-member team as Scrum Master; Agile delivery of platform services",
            "Workflow automation and job orchestration via Apache Airflow",
        ]),
        ("Associate IT Consultant", "ITC Infotech / Bosch", "Jan 2014 \u2013 Sep 2014", [
            "SCM tools automation and integration (MKS/ClearQuest)",
            "Data synchronization script development",
        ]),
        ("Software Engineer", "eHover Systems", "Apr 2013 \u2013 Jan 2014", [
            "Cloud-based surveillance system architecture (AWS S3/EC2)",
            "Computer vision data pipeline and web interface development",
        ]),
        ("Project Assistant", "Kuvempu University", "Apr 2011 \u2013 Apr 2013", [
            "Developed Python modules for molecular dynamic simulations and data analysis",
            "Built SBML file analysis web application using Python/LibSBML bindings",
            "Applied computational biology techniques: BioPython, BioPerl, Gromacs",
        ]),
        ("Software Developer Intern", "IBAB", "Sep 2010 \u2013 Feb 2011", [
            "Mammalian Gene Expression Database development",
            "Data curation web application using Perl, MySQL, JavaScript",
        ]),
    ]
    for title, company, date, bullets in experiences:
        story.append(build_experience_entry(title, company, date, bullets))

    # Education
    story.append(section_header("Education"))
    story.append(Paragraph("<b>M.Sc in Bioinformatics</b> &mdash; Kuvempu University, Karnataka", style_body))
    story.append(Paragraph("Focus: Genomics, Drug Discovery, Protein Engineering", style_body_italic))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>B.Sc in Biotechnology</b> &mdash; Kuvempu University, Karnataka", style_body))
    story.append(Paragraph("Majors: Biotechnology, Botany, Computer Science", style_body_italic))
    story.append(Spacer(1, 10))

    # Certifications
    story.append(section_header("Certifications"))
    story.append(Paragraph("\u2022&nbsp;&nbsp;Certified Kubernetes Administrator (CKA)", style_body))
    story.append(Spacer(1, 10))

    # Additional
    story.append(section_header("Additional"))
    t = Table([[
        Paragraph("<b>Languages:</b> English, Hindi, Kannada, Telugu", style_body),
        Paragraph("<b>Interests:</b> Gardening, Movies", style_body),
    ]], colWidths=[3.5*inch, 3.5*inch])
    t.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 0)]))
    story.append(t)

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    build_pdf("/home/bharath/workspace/profile_agent/Bharath_Krishna_AI_Architect.pdf")
