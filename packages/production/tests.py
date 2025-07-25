from reportlab.graphics import renderPDF
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Crear el lienzo PDF
c = canvas.Canvas("grafico_barras_etiquetas.pdf", pagesize=letter)
width, height = letter

# Crear un dibujo
drawing = Drawing(400, 250)

# Crear el gráfico de barras
chart = VerticalBarChart()
chart.x = 50
chart.y = 50
chart.height = 150
chart.width = 300
chart.data = [
    (10, 20, 30, 40),
    (15, 22, 28, 35),
]
chart.categoryAxis.categoryNames = ['Ene', 'Feb', 'Mar', 'Abr']
chart.bars[0].fillColor = colors.blue
chart.bars[1].fillColor = colors.green

# Configurar eje Y
chart.valueAxis.valueMin = 0
chart.valueAxis.valueMax = 50
chart.valueAxis.valueStep = 10
chart.valueAxis.labelTextFormat = '%d'

# ===== Añadir título del gráfico =====
title = String(200, 220, "Ventas mensuales", fontSize=14, textAnchor="middle")

# ===== Añadir etiquetas de los ejes (manualmente con String) =====
x_label = String(200, 20, "Meses", fontSize=10, textAnchor="middle")

# Añadir elementos al dibuj


drawing.add(chart)
drawing.add(title)
drawing.add(x_label)

# Dibujar en el PDF
renderPDF.draw(drawing, c, 50, height - 350)

c.save()
