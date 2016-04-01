from collections import defaultdict
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def to_text(filePath):
    '''Read words of a pdf file'''
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    with open(filePath, 'rb') as fp:
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)

    converter.close()
    text = output.getvalue()
    output.close()
    return text



if __name__ == "__main__":
    file_path = r'D:\MyFiles\baiduyun\ITKnowledge\BI\DataWarehouse\Case Study A Data Warehouse for an Academic Medical Center.pdf'
    to_text(file_path)
    a = 'adda'
    a.split()