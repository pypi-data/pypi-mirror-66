import sys
import os
import time

from pdfrw import PdfReader, PdfWriter, IndirectPdfDict, PageMerge
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pdfrw
import qrcode

from . import settings

tmp_dir = "/tmp/"

reasons = " ".join(sys.argv[1:]).lower()
if not reasons:
    reasons = settings.reasons
inputs = settings.inputs

all_reasons = {
    'travail': (76, 527, 'x'),
    'courses': (76, 478, 'x'),
    'sante': (76, 436, 'x'),
    'famille': (76, 400, 'x'),
    'sport': (76, 345, 'x'),
    'judiciaire': (76, 298, 'x'),
    'missions': (76, 260, 'x')
}

global_data = settings.global_data
data = settings.data

hour = f"{time.localtime().tm_hour:02}"
minute = f"{time.localtime().tm_min:02}"
date = f"{time.localtime().tm_mday}/{time.localtime().tm_mon:02}/{time.localtime().tm_year}"

def generate_overlay(item):
    c = canvas.Canvas(tmp_dir + f'simple_form_overlay_{item["firstname"]}.pdf')
    c.setFont('Helvetica', 12)
    c.drawString(123, 686, item["firstname"] + " " + item["lastname"])
    c.drawString(123, 661, item["birthday"])
    c.drawString(92, 638, item["town"])
    c.drawString(134, 613, global_data["adresse"])
    c.setFont('Helvetica', 16)
    for reason in all_reasons:
        if reason in reasons:
            c.drawString(*all_reasons[reason])
    c.setFont('Helvetica', 12)
    c.drawString(111, 226, global_data["ville"])
    c.drawString(92, 200, date)
    c.drawString(200, 201, hour)
    c.drawString(220, 201, minute)
    image = generate_qrcode(item)
    c.drawImage(image, 400, 155, width=100, height=100)
    c.save()
    return image

def merge_pdfs(form_pdf, overlay_pdf, output):
    """
    Merge the specified fillable form PDF with the
    overlay PDF and save the output
    """
    form = pdfrw.PdfReader(form_pdf)
    olay = pdfrw.PdfReader(overlay_pdf)

    for form_page, overlay_page in zip(form.pages, olay.pages):
        merge_obj = pdfrw.PageMerge()
        overlay = merge_obj.add(overlay_page)[0]
        pdfrw.PageMerge(form_page).add(overlay).render()

    writer = pdfrw.PdfWriter()
    writer.write(output, form)


def generate_qrcode(item):
    data = "; ".join([
        f'Cree le: {date} a {hour}h{minute}',
        f'Nom: {item["lastname"]}',
        f'Prenom: {item["firstname"]}',
        f'Naissance: {item["birthday"]} a {item["town"]}',
        f'Adresse: {global_data["adresse"]}',
        f'Sortie: {date} a {hour}h{minute}',
        f'Motifs: {reasons}',
    ])
    qrcode_filename = tmp_dir + f"qrcode_{item['firstname']}.png"
    qrcode.make(data).save(tmp_dir + f"qrcode_{item['firstname']}.png")
    c = canvas.Canvas(tmp_dir + f"qrcode_{item['firstname']}.pdf", pagesize=letter)
    c.drawImage(qrcode_filename, 50, 400, width=300, height=300)
    c.save()
    return qrcode_filename

def set_conf(config, time):
    global global_data, data, inputs, hour, minute
    if config:
        global_data = config.global_data
        data = config.data
        inputs = config.inputs
    if time:
        try:
            _time = []
            if "h" in time:
                _time = time.split("h")
            elif ":" in time:
                _time = time.split("h")
            hour = f"{int(_time[0]):02}"
            minute = f"{int(_time[1]):02}"
        except IndexError:
            pass

def main(config=None, time=None, out=None):
    set_conf(config, time)
    for person in data:
        generate_overlay(person)
        merge_pdfs(inputs,
                   tmp_dir + f'simple_form_overlay_{person["firstname"]}.pdf',
                   tmp_dir + f'merged_form_{person["firstname"]}.pdf')
    pages = []
    writer = PdfWriter(out)
    for person in data:
        _pages = pdfrw.PdfReader(tmp_dir + f'merged_form_{person["firstname"]}.pdf')
        qrpdf = pdfrw.PdfReader(tmp_dir + f"qrcode_{person['firstname']}.pdf")
        writer.addpages(_pages.pages)
        writer.addpages(qrpdf.pages)
    writer.write()

if __name__ == '__main__':
    main()
