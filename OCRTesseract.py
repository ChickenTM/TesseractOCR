from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from tempfile import TemporaryDirectory
from pathlib import Path
from fpdf import FPDF
import fitz
from pypdf import PdfMerger
import os


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\mithun\AppData\Local\Programs\Tesseract-OCR\tesseract"
)
path_to_poppler_exe = Path(
    r"C:\Users\mithun\AppData\Local\Programs\poppler-23.01.0\Library\bin"
)
out_directory = Path(
    r"C:\Users\mithun\Desktop\project\pdf scripts\Outputs"
).expanduser()

PDF_file = Path(r"sample.pdf")


image_file_list = []

text_file = out_directory / Path("OCRop.txt")

# pdf = FPDF()


with TemporaryDirectory() as tempdir:
    pdf_pages = convert_from_path(
        PDF_file, 500, first_page=1, last_page=5, poppler_path=path_to_poppler_exe
    )

    for page_enumeration, page in enumerate(pdf_pages, start=1):
        filename = f"{tempdir}\page_{page_enumeration:03}.png"

        page.save(filename, "PNG")
        image_file_list.append(filename)

    # image_file_list = [f"{tempdir}\page_001.png", f"{tempdir}\page_002.png"]

    merger = PdfMerger()
    with open(f"{tempdir}\\temppdf.pdf", "wb") as file:
        for image_file in image_file_list:
            pdf = pytesseract.image_to_pdf_or_hocr(
                Image.open(image_file), extension="pdf"
            )
            file.write(pdf)
            merger.append(f"{tempdir}\\temppdf.pdf")  # tesseracttest.pdf")
        if os.path.exists(out_directory / Path("output.pdf")):
            os.remove(out_directory / Path("output.pdf"))

        merger.write(out_directory / Path("output.pdf"))
        merger.close()

    with fitz.open("output.pdf") as doc:
        for page in doc:
            # print(page)

            for block in page.get_text("dict", sort=True)[
                "blocks"
            ]:  # dictionary of block width,block height,block blocks
                # print(page)
                # print("block",block)
                lines = block.get("lines")  # get lines from blocks
                # print(lines)
                block_text = ""
                if lines:
                    for line in lines:
                        line_1 = line["bbox"]  # line bbox extraction
                        # print("line_1:",line_1)
                        # getText = line['']
                        # print(getText)
                        spans = line.get("spans")
                        # print(line["text"])
                        # print("spans:",spans)

                        """if spans:
                            for span in spans:
                                characters = span.get('chars')
                                if characters:
                                    for ch in characters:
                                        print(ch.c)
                                    #print(i, ":", span["chars"])"""

                        line_text = ""
                        for span in spans:
                            line_text += span["text"]

                        block_text += line_text
                    print("block text : ", block_text)

                    # print(span["text"], end = " ")
                    # span_text = " ".join(span["text"])#.split())
                    # print(span_text)
                    # print("span_text:",span_text)
                    # line_text += " "+span_text
                    # print("line_text:", line_text)

    """    
    with open(text_file, "a") as output_file:
        for image_file in image_file_list:
            text = str(((pytesseract.image_to_string(Image.open(image_file))))) 
            text = text.replace("-\n", "")
            converted_text = text.encode('latin-1', 'replace').decode('latin-1')
            print(converted_text)
            pdf.add_page()
            pdf.set_font("Arial", size = 12)
            pdf.multi_cell(200, 10, txt = converted_text)
            #output_file.write(text)
        
    pdf.output("tesspdfop.pdf")    
        """

    """for image_file in image_file_list:
            text = str(((pytesseract.image_to_string(Image.open(image_file))))) 
            text = text.replace("-\n", "")
            output_file.write(text)     """
