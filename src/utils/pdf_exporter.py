import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_report(markdown_content: str, output_path: str = "docs/Informe_Arquitectura_Yatawek.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Estilos corporativos personalizados
    title_style = ParagraphStyle(
        'CorporateTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#1E3A8A'), # Azul corporativo
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'CorporateSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )
    
    heading_style = ParagraphStyle(
        'CorporateHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'CorporateBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8,
        leading=14
    )

    story = []
    
    # Cabecera Corporativa
    story.append(Paragraph("YATAWEK DATA CORP. — ENTERPRISE BI DIVISION", subtitle_style))
    story.append(Paragraph("Informe Técnico de Arquitectura de Datos", title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1E3A8A'), spaceBefore=2, spaceAfter=15))
    
    # Procesar línea a línea el Markdown recibido de la IA para adaptarlo limpiamente al PDF
    lines = markdown_content.split('\n')
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        
        if line_clean.startswith('# '):
            continue # Ya ponemos el título principal arriba
        elif line_clean.startswith('### '):
            story.append(Paragraph(line_clean.replace('### ', ''), heading_style))
        elif line_clean.startswith('## '):
            story.append(Paragraph(line_clean.replace('## ', ''), heading_style))
        elif line_clean.startswith('- ') or line_clean.startswith('* '):
            bullet_text = "• " + line_clean[2:]
            story.append(Paragraph(bullet_text, body_style))
        else:
            story.append(Paragraph(line_clean, body_style))

    # Pie de página / Firma
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=10, spaceAfter=10))
    footer_style = ParagraphStyle('Footer', parent=styles['Italic'], fontSize=8, textColor=colors.HexColor('#94A3B8'))
    story.append(Paragraph("Documento generado automáticamente por el Copiloto Multiagente de BI — Yatawek Data Corp.", footer_style))

    doc.build(story)
    print(f"📄 [PDF Generado con éxito]: {output_path}")