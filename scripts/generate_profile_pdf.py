"""Generate a professional PDF resume for Bharath Krishna."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)


# Colors
NAVY = HexColor("#4A6FA5")
DARK_BLUE = HexColor("#5B7DB8")
ACCENT = HexColor("#60A5FA")
PILL_BG = HexColor("#F0F4FF")
DARK_GRAY = HexColor("#4A4A4A")
MED_GRAY = HexColor("#6B6B6B")
LIGHT_GRAY = HexColor("#9CA3AF")
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
style_emp_id = ParagraphStyle("EmpId", fontSize=9, leading=13, textColor=LIGHT_GRAY, fontName="Helvetica", alignment=TA_LEFT)


def section_header(text):
    return KeepTogether([
        Paragraph(text.upper(), style_section),
        HRFlowable(width="100%", thickness=2, color=ACCENT, spaceBefore=0, spaceAfter=8),
    ])


def build_header():
    name = Paragraph("BHARATH KRISHNA", style_name)
    title = Paragraph("Full Stack Engineer &amp; AgenticAI Specialist", style_title)
    contact_left = Paragraph('<font size="9">+1-857-437-9316&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;bharath.chakravarthi@gmail.com</font>', style_contact)
    contact_right = Paragraph('<font size="9">https://profile.krishb.in&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;California, USA</font>', style_contact)

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
    style_comp = ParagraphStyle("Competency", fontSize=9, leading=13, textColor=DARK_GRAY, fontName="Helvetica")
    items = [
        "LLMOps & DevOps Pipelines",
        "AgenticAI (A2A, MCP, n8n)",
        "GPU Cluster Administration",
        "Kubernetes (CKA certified)",
        "Infrastructure-as-Code",
        "REST API Development",
        "Agile / Scrum Leadership",
        "Full Stack (React + FastAPI)",
        "Team Leadership & Mentoring",
    ]
    # Arrange as 3 columns x 4 rows
    cols = 3
    rows = []
    for i in range(0, len(items), cols):
        row = []
        for j in range(cols):
            idx = i + j
            if idx < len(items):
                row.append(Paragraph(f"\u2022&nbsp;&nbsp;{items[idx]}", style_comp))
            else:
                row.append(Paragraph("", style_comp))
        rows.append(row)
    col_width = 7.0 * inch / cols
    t = Table(rows, colWidths=[col_width] * cols)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def build_skills():
    skills = [
        ("Programming", "Python (15 yrs), Golang (7 yrs)"),
        ("Frontend", "React, NextJS, ChakraUI"),
        ("Infrastructure", "Kubernetes (CKA), Ansible, Terraform, GCP, Docker"),
        ("Backend", "FastAPI, Gin Gonic, PostgreSQL, MongoDB"),
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

    story.append(section_header("Professional Summary"))
    story.append(Paragraph(
        "Full stack engineer with 15+ years of experience building AgenticAI solutions "
        "and managing HPC clusters for ML/LLM operations. Expertise spans LLMOps pipelines, "
        "model serving infrastructure, and API development with proven Kubernetes and "
        "Infrastructure-as-Code competency.", style_summary))
    story.append(Spacer(1, 4))
    story.append(build_competencies())
    story.append(Spacer(1, 4))

    story.append(section_header("Technical Skills"))
    story.append(build_skills())
    story.append(Spacer(1, 3))

    story.append(section_header("Work Experience"))
    experiences = [
        ("Senior Software Engineer", "Rakuten USA", "May 2022 \u2013 Feb 2026", [
            "Building AgenticAI apps and workflows using n8n, A2A and MCP protocols with CopilotKit",
            "Managing storage and compute at on-prem and public cloud infrastructures",
            "GPU Cluster administration and optimization for LLM training and inferencing workloads",
            "Deploying LLMs for inferencing via vllm, sglang and hyperparameter tuning for resiliency",
            "Developing UI/API/CLI tools for HPC cluster training job submission",
            "MLOps and GitOps setup and high-performance Kubernetes cluster maintenance (SRE/Admin role)",
            "IAM for humans and agents to access cloud resources and on-prem services",
            "Custom Kubernetes operator development and team leadership",
        ]),
        ("Application Engineer", "Rakuten, Inc. \u2014 Tokyo", "Jan 2018 \u2013 May 2022", [
            "Infrastructure-as-Code development with Terraform/Ansible",
            "Custom Terraform plugin and GoLang SDK development",
            "REST API toolkit development (FastAPI/Gin) and authentication services",
            "Load testing and test case implementation",
        ]),
        ("Application Engineer", "Rakuten India", "Sep 2014 \u2013 Dec 2018", [
            "API development for IaaS (VMware), DNS (Nominum), and Load Balancers (BigIP)",
            "Led small team as Scrum Master",
            "Job automation via Apache Airflow",
        ]),
        ("Associate IT Consultant", "ITC Infotech / Bosch", "Jan 2014 \u2013 Sep 2014", [
            "SCM tools automation (MKS/ClearQuest)",
            "PERL synchronization script development",
        ]),
        ("Software Engineer", "eHover Systems", "Apr 2013 \u2013 Jan 2014", [
            "Cloud-based surveillance system development (AWS S3/EC2/ZoneMinder)",
            "Web interface for surveillance data access using PHP and CodeIgniter",
        ]),
        ("Project Assistant", "Kuvempu University", "Apr 2011 \u2013 Apr 2013", [
            "Perl module development for molecular dynamic simulations",
            "SBML file analysis web application using Python/LibSBML bindings",
            "Technologies: BioPython, BioPerl, LibSBML, Gromacs",
        ]),
        ("Software Developer Intern", "IBAB", "Sep 2010 \u2013 Feb 2011", [
            "Mammalian Gene Expression Database development",
            "Bio-curator data web application using Perl, MySQL, JavaScript",
        ]),
    ]
    for title, company, date, bullets in experiences:
        story.append(build_experience_entry(title, company, date, bullets))

    story.append(section_header("Education"))
    story.append(Paragraph("<b>M.Sc in Bioinformatics</b> &mdash; Kuvempu University, Karnataka", style_body))
    story.append(Paragraph("Focus: Genomics, Drug Discovery, Protein Engineering", style_body_italic))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>B.Sc in Biotechnology</b> &mdash; Kuvempu University, Karnataka", style_body))
    story.append(Paragraph("Majors: Biotechnology, Botany, Computer Science", style_body_italic))
    story.append(Spacer(1, 10))

    story.append(section_header("Certifications"))
    story.append(Paragraph("\u2022&nbsp;&nbsp;Certified Kubernetes Administrator (CKA)", style_body))
    story.append(Spacer(1, 10))

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
    build_pdf("/home/bharath/workspace/profile_agent/Bharath_Krishna_Profile.pdf")
