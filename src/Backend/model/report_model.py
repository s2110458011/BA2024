from fpdf import FPDF
from fpdf.enums import XPos, YPos
from backend.model.report_item_model import ReportItem
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from customtkinter import CTkLabel

class PDFReport():
    def __init__(self, title: str) -> None:
        self.title: str = title
        self.report_items: list[ReportItem | str] = []
        self.preview_labels: list[Type['CTkLabel']] = []
        return None
    
    def add_report_item(self, item: ReportItem | str, label: Type['CTkLabel']) -> None:
        self.report_items.append(item)
        self.preview_labels.append(label)
        return None
    
    def update_title(self, title: str) -> None:
        self.title = title
        return None
    
    def print_report_as_pdf(self, file_path: str) -> FPDF:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font(family='arial', style='BU', size=20)
        pdf.cell(0, 20, text=self.title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        for item in self.report_items:
            if isinstance(item, str):
                pdf.set_font(family='arial', style='B', size=15)
                pdf.cell(0, 10, text=item, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            elif isinstance(item, ReportItem):
                pdf.set_font(family='arial', style='', size=10)
                img = item.get_image()
                pdf.image(img, w=((pdf.epw/4)*3))
                pdf.multi_cell(0, 5, item.get_description())
        pdf.output(file_path)
        return None