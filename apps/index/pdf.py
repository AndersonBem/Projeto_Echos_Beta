from tkinter import *
from tkinter import ttk
from tkinter import messagebox


from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import A4

import os 

pastaApp=os.path.dirname(__file__)


def criarPDF():
    cnv = canvas.Canvas(pastaApp+"\\cbfcursos.pdf", pagesize=A4)
    cnv.drawString(100,100,"CBF Cursos")
    
    cnv.save()

app=Tk()
app.title("CFB Cursos")
app.geometry("600x450")


btn_criarPDF= Button(app, text='Criar PDF', command=criarPDF)
btn_criarPDF.pack(side="left",padx=10)

app.mainloop()

