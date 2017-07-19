# -*- encoding:utf-8 -*-

#  for pdfminer3k
# from pdfminer.pdfinterp import PDFResourceManager, process_pdf
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from io import StringIO
# from io import open as io_open

# for pdfminer.six
from io import StringIO
from io import open as io_open
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter

import os
import signal
import logging





class TimeOutException(Exception):
    pass

def setTimeout(num):
    def wrape(func):
        def handle(signum, frame):
            raise TimeOutException("PDF解析超时！")

        def toDo(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)
                signal.alarm(num)
                ret = func(*args, **kwargs)
                signal.alarm(0)
                return ret
            except TimeOutException as e:
                logging.info('pdf parse time out')
                return False

        return toDo

    return wrape

@setTimeout(60)
def readPDF(path):

    logging.propagate = False
    logging.getLogger().setLevel(logging.ERROR)

    ret = False
    retstr = StringIO()
    laparams = LAParams()

    # Open a PDF file.
    fp = open(path, 'rb')
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)
    # Create a PDF document object that stores the document structure.
    # Supply the password for initialization.
    document = PDFDocument(parser)
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    # device = PDFDevice(rsrcmgr)
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
    fp.close()

    content = retstr.getvalue()
    retstr.close()

    filename = path.replace('.pdf', '.txt')
    with open(filename, 'w') as f:
        f.write(content)
    if os.path.exists(filename):
        with open(filename) as f:
            num_lines = sum(1 for line in f)
            if num_lines > 10:
                ret = True
    return ret