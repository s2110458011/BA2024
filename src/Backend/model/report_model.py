from fpdf import FPDF
from backend.model.report_item_model import ReportItem

class PDFReport():
    def __init__(self, title: str) -> None:
        self.title = title
        self.report_items = []
        return None
    
    def add_report_item(self, item: ReportItem) -> None:
        self.report_items.append(item)
        return None
    
    def print_report_as_pdf(self) -> None:
        pdf = FPDF()
        pdf.add_page()
        
        return None