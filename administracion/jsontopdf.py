# Python program to create
# a pdf file
import json
import csv
import pandas as pd
import pdfkit




  
from fpdf import FPDF

  
  
# save FPDF() class into a 
# variable pdf
def jsontoPDF():
    pdf = FPDF()
    
# Add a page
    pdf.add_page()
  
# set style and size of font 
# that you want in the pdf
    page_width = pdf.w - 3 * pdf.l_margin
    pdf.set_font("Arial", size = 8)
  
# create a cell
    pdf.cell(200, 10, txt = "Coopresol", 
         ln = 1, align = 'C')
    col_width = page_width/4

    th = pdf.font_size
# add another cell
    with open("data.csv", newline='') as f:
        reader = csv.reader(f)
        for x in reader:
            pdf.cell(col_width, th, str(x[1]), border=1)
            pdf.cell(col_width, th, str(x[2]), border=1)
            pdf.cell(col_width, th, str(x[3]), border=1)
            pdf.cell(col_width, th, str(x[4]), border=1)
            pdf.cell(col_width, th, str(x[5]), border=1)
            pdf.cell(col_width, th, str(x[6]), border=1)
            pdf.cell(col_width, th, str(x[7]), border=1)
            pdf.cell(col_width, th, str(x[8]), border=1)
            pdf.ln(th)
            
  
# save the pdf with name .pdf
    pdf.output("../pdf.pdf")   

def jsontoCSV(json):
 
    jsondata = json
 
    data_file = open('data.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)
 
    count = 0
    for data in jsondata:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
 
    data_file.close()
    CSV = pd.read_excel('data.xlsx' ,encoding='latin-1')  

    CSV.to_html('data.html')  
   

    
