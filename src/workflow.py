import os
from dotenv import load_dotenv
from google import genai
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

load_dotenv()

class DocumenterAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        # Usamos el modelo ultrarrápido y estable de Gemini
        self.model_name = "gemini-3.8-flash"

    def document_code(self, code_snippet: str, code_type: str) -> str:
        prompt = f"""Eres un Arquitecto de Datos Senior experto en T-SQL y DAX. 
        Analiza el siguiente código de tipo {code_type} y devuelve un informe técnico en Markdown estructurado que explique: 
        1) El propósito de negocio, 2) Las tablas, dimensiones o medidas involucradas, y 3) La lógica de procesamiento o recomendaciones de optimización.

        Código a analizar:
        {code_snippet}"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"# ⚠️ Error de Conexión\nNo se pudo conectar con Gemini: {e}"

def generate_pdf_report(markdown_content: str, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CorporateTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor('#1E3A8A'), spaceAfter=6)
    subtitle_style = ParagraphStyle('CorporateSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#64748B'), spaceAfter=15)
    heading_style = ParagraphStyle('CorporateHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, textColor=colors.HexColor('#0F172A'), spaceBefore=10, spaceAfter=4)
    body_style = ParagraphStyle('CorporateBody', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.5, textColor=colors.HexColor('#334155'), spaceAfter=6, leading=13)

    story = []
    story.append(Paragraph("YATAWEK DATA CORP. — ENTERPRISE BI DIVISION", subtitle_style))
    story.append(Paragraph("Informe Técnico de Auditoría de Código Analítico", title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1E3A8A'), spaceBefore=2, spaceAfter=12))
    
    for line in markdown_content.split('\n'):
        line_clean = line.strip()
        if not line_clean or line_clean.startswith('# '): continue
        if line_clean.startswith('### ') or line_clean.startswith('## '):
            story.append(Paragraph(line_clean.replace('#', '').strip(), heading_style))
        elif line_clean.startswith('- ') or line_clean.startswith('* '):
            story.append(Paragraph("• " + line_clean[2:], body_style))
        else:
            story.append(Paragraph(line_clean, body_style))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=8, spaceAfter=8))
    footer_style = ParagraphStyle('Footer', parent=styles['Italic'], fontSize=8, textColor=colors.HexColor('#94A3B8'))
    story.append(Paragraph("Generado automáticamente por el Copiloto Multiagente de Yatawek Data Corp.", footer_style))

    doc.build(story)

def get_all_inputs():
    """Busca TODOS los archivos SQL y DAX y los devuelve en una lista"""
    files_to_process = []
    if not os.path.exists("inputs"):
        return files_to_process

    for root, dirs, files in os.walk("inputs"):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".sql"):
                with open(file_path, "r", encoding="utf-8") as f:
                    files_to_process.append({"name": file, "path": file_path, "content": f.read(), "type": "T-SQL"})
            elif file.endswith(".dax"):
                with open(file_path, "r", encoding="utf-8") as f:
                    files_to_process.append({"name": file, "path": file_path, "content": f.read(), "type": "DAX (Power BI)"})
    return files_to_process

def main():
    print("🚀 Iniciando el copiloto multiagente de Yatawek Data Corp...")
    
    archivos = get_all_inputs()
    if not archivos:
        print("⚠️ No se encontraron archivos en la carpeta 'inputs/'")
        return

    print(f"📦 Se han detectado {len(archivos)} archivos para procesar en lote.\n")
    documenter = DocumenterAgent()

    # Procesamos TODOS los archivos uno por uno
    for archivo in archivos:
        print(f"🔍 Analizando: {archivo['path']} ({archivo['type']})...")
        report_md = documenter.document_code(archivo['content'], code_type=archivo['type'])
        
        # Generamos un PDF con el nombre del archivo original
        nombre_pdf = f"docs/Informe_{archivo['name']}.pdf"
        generate_pdf_report(report_md, output_path=nombre_pdf)
        print(f"✅ PDF Generado: {nombre_pdf}\n")
    
    print("🎉 ¡Procesamiento por lotes completado con éxito!")

if __name__ == "__main__":
    main()