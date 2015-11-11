from pdfminer.pdfparser import PDFParser, PDFDocument

__author__ = 'M.Y'
from io import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    parser = PDFParser(fp)
    # Create a PDF document object that stores the document structure.
    doc = PDFDocument(caching=caching)
    # Connect the parser and document objects.
    parser.set_document(doc)
    doc.set_parser(parser)
    # Supply the document password for initialization.
    # (If no password is set, give an empty string.)
    doc.initialize(password)
    # Check if the document allows text extraction. If not, abort.
    # if check_extractable and not doc.is_extractable:
    #     raise PDFTextExtractionNotAllowed('Text extraction is not allowed: %r' % fp)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    # for (pageno,page) in enumerate(doc.get_pages()):
    #     if pagenos and (pageno not in pagenos): continue
    #     interpreter.process_page(page)
    #     if maxpages and maxpages <= pageno+1: break


    for page in doc.get_pages():
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def fnPDF_FindText(xFile, xString):
    # xfile : the PDF file in which to look
    # xString : the string to look for
    import PyPDF2, re

    PageFound = -1
    pdfDoc = PyPDF2.PdfFileReader(open(xFile, "rb"))
    for i in range(0, pdfDoc.getNumPages()):
        content = pdfDoc.getPage(i).extractText() + "\n"
        # content1 = content.encode('ascii', 'ignore').lower()
        ResSearch = re.search(xString, content)
        if bool(ResSearch) is True:
            PageFound = i
            break
    return PageFound
