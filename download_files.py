import csv
import sys
import os
from fpdf import FPDF

def download_csv(fields, rows, tipo):
    if tipo == 1:
        filename = "historial_visitas.csv"
    elif tipo == 2:
        filename = "historial_pruebas_covid.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

def download_pdf(fields, rows, tipo):
    pdf = FPDF(orientation = 'L')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    header = "| "
    for x in fields:
        header = header + x + ' | '
    pdf.cell(0, 10, txt = header, ln = 1, align = 'C')
    pdf.set_font("Arial", size = 12)
    for l in rows:
        r = "| "
        for x in l:
            r = r + str(x) + ' | '
        pdf.cell(0, 10, txt = r, ln = 1, align = 'C')
    if tipo == 1:
        filename = "historial_visitas.pdf"
    elif tipo == 2:
        filename = "historial_pruebas_covid.pdf"
    pdf.output(filename)
