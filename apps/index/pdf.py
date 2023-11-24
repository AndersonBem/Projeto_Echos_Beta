

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors



def mp(mm):
    return mm/0.352777

caminho_imagem = "C:\\Anderson\\Alura\\Projeto Echos Em Uso\\setup\\static\\assets\\not-found.png"

pdf = canvas.Canvas("teste.pdf")

pdf.setPageSize(A4)
pdf.setStrokeColor(colors.green)
pdf.setFillColor(colors.green)
pdf.rect(mp(55),mp(143),mp(100),mp(10),stroke=1,fill=0)
pdf.drawImage(caminho_imagem,mp(0),mp(0))
pdf.circle(mp(105),mp(147),mp(50))

pdf.save()

