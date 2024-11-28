from docx2pdf import convert
import PyPDF2
import sys
import os
from PIL import Image, ImageEnhance
from pdf2image import convert_from_path


def add_background_to_pdf(input_pdf, background_image, output_pdf, coeff):
    # Open the input PDF file
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)

        # Create a PDF writer
        pdf_writer = PyPDF2.PdfWriter()
        page = pdf_reader.pages[0]
        img = Image.open(background_image)
        img = img.resize((page.mediabox[2], page.mediabox[3]))
        img = img.convert("HSV")
        # enhance color
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(coeff)
        img = img.convert("RGB")
        # enhance brightness
        enhancer = ImageEnhance.Brightness(img)
        br_coeff = 1
        if(coeff > 1):
            br_coeff = (coeff - 1) / 2 + 1
        elif(coeff < 1):
            br_coeff = 1 + ((1 - coeff) / 2)
        img = enhancer.enhance(br_coeff)
        img.save("temporary_pdf.pdf")
        # Iterate over the input PDF pages and layer them on top of the background
        for page_num in range(total_pages):
            with open("temporary_pdf.pdf", 'rb') as bg_file:  # pointers are used (if you dont open the file each time, you overwrite the pages)
                page = PyPDF2.PdfReader(bg_file).pages[0]
                page.merge_page(pdf_reader.pages[page_num])
                pdf_writer.add_page(page)

        # Write the output PDF file
        with open(output_pdf, 'wb') as output:
            pdf_writer.write(output)
        os.remove("temporary_pdf.pdf")
#######################################################################################################################################

# MAIN:
## arguments: input pdf name, output pdf name, background image name, scaling coeff 
if(len(sys.argv) < 5):
    print("Please provide the input pdf file and backgroung image as arguments.")
    exit(1)


input_pdf = sys.argv[1]  # Replace with the path to your input pdf document
output_pdf = sys.argv[2] # output name
bg_image = sys.argv[3] # background name

dir_path = os.path.dirname(input_pdf)
output_pdf = os.path.join(dir_path, output_pdf)

add_background_to_pdf(input_pdf, bg_image, output_pdf, float(sys.argv[4]))

pages = convert_from_path(output_pdf)

for pageNum in range(len(pages)):
    pathNamePNG = os.path.join(dir_path, str(pageNum + 1) + "_page.png")
    pages[pageNum].save(pathNamePNG, "PNG")