from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib.units import cm
from packages.production.models import Plot, Tree
from packages.sales.models import SaleV2, SaleDistribution
from datetime import datetime

@staff_member_required
def plot_sales_pdf(request, plot_id):
    print(_("primera opción"))

    # Filtros por fecha
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    try:
        plot = get_object_or_404(Plot, pk=plot_id)
    except Plot.DoesNotExist:
        raise Http404(_('Plot not found'))
    print(_("PDF generado exitosamente."))

    # Árboles del plot
    trees = Tree.objects.filter(plot=plot)
    tree_ids = trees.values_list('id', flat=True)
    print(_("PDF generado exitosamente."))

    # Filtrar SaleDistribution por plot y fechas
    # Obtener los harvests del plot
    from packages.farming.models import Harvest, Distribution
    harvests = Harvest.objects.filter(plot=plot)
    distributions = Distribution.objects.filter(harvest__in=harvests, type=Distribution.Type.SALE)
    sale_distributions = SaleDistribution.objects.filter(distribution__in=distributions)
    if start_date:
        sale_distributions = sale_distributions.filter(sale__date__gte=start_date)
    if end_date:
        sale_distributions = sale_distributions.filter(sale__date__lte=end_date)

    # Resumen general
    total_ventas = sum(float(dist.total_price) for dist in sale_distributions)
    print(_("PDF generado exitosamente."))

    # PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"ventas_plot_{plot.id}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50

    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, _(f"Resumen de Ventas - {plot.name}"))
    y -= 30
    p.setFont("Helvetica", 10)
    p.drawString(50, y, _(f"Ubicación: {plot.location or '-'} | Área: {plot.area_m2 or '-'} m²"))
    y -= 20
    if start_date or end_date:
        p.drawString(50, y, _(f"Filtro de fechas: {start_date or '-'} a {end_date or '-'}"))
        y -= 20
    p.drawString(50, y, _(f"Total ventas: ${total_ventas:.2f}"))
    y -= 30
    print(_("PDF generado exitosamente."))

    # Gráfico de barras: ventas por fecha
    fechas = []
    ventas_por_fecha = {}
    ventas_detalle = {}
    if sale_distributions.exists():
        from collections import defaultdict
        ventas_por_fecha = defaultdict(float)
        ventas_detalle = defaultdict(list)
        for dist in sale_distributions:
            fecha = dist.sale.date.strftime('%Y-%m-%d')
            ventas_por_fecha[fecha] += float(dist.total_price)
            ventas_detalle[fecha].append(dist)
        fechas = sorted(ventas_por_fecha.keys())
        data = [[ventas_por_fecha[f] for f in fechas]]
        d = Drawing(400, 200)
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 30
        bc.height = 120
        bc.width = 300
        bc.data = data
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = max(data[0]) * 1.2 if data[0] else 1
        bc.valueAxis.valueStep = max(data[0]) / 5 if max(data[0]) > 0 else 1
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.categoryNames = fechas
        bc.bars[0].fillColor = colors.HexColor('#4e73df')
        # Mostrar el total encima de cada barra
        for i, valor in enumerate(data[0]):
            label = Label()
            label.setOrigin(bc.x + bc.groupSpacing/2 + i*(bc.barWidth+bc.groupSpacing) + bc.barWidth/2, bc.y + bc.height + 5)
            label.boxAnchor = 's'
            label.angle = 0
            label.fontName = 'Helvetica-Bold'
            label.fontSize = 8
            label.fillColor = colors.black
            label.setText(f"${valor:.2f}")
            d.add(label)
        render_y = y - 200
        d.drawOn(p, 50, render_y)
        y = render_y - 20
    else:
        ventas_detalle = {}
        fechas = []

    # Detalle de ventas agrupado por fecha
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, _("Detalle de ventas por fecha:"))
    y -= 20
    p.setFont("Helvetica", 9)
    for fecha in fechas:
        if y < 100:
            p.showPage()
            y = height - 50
        total_fecha = ventas_por_fecha[fecha]
        p.setFont("Helvetica-Bold", 10)
        p.drawString(60, y, _(f"Fecha: {fecha} | Total: ${total_fecha:.2f}"))
        y -= 15
        p.setFont("Helvetica", 9)
        for dist in ventas_detalle[fecha]:
            if y < 80:
                p.showPage()
                y = height - 50
            p.drawString(80, y, _(f"Cantidad: {dist.distribution.quantity} | Precio: ${dist.total_price:.2f}"))
            y -= 12
        y -= 5

    p.showPage()
    p.save()
    return response



from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib.units import cm
from packages.production.models import Plot, Tree
from packages.sales.models import SaleV2, SaleDistribution
from datetime import datetime
from reportlab.graphics.charts.textlabels import Label

@staff_member_required
def plot_sales_pdf(request, plot_id):

    # Filtros por fecha
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    try:
        plot = get_object_or_404(Plot, pk=plot_id)
    except Plot.DoesNotExist:
        raise Http404(_('Plot not found'))

    # Árboles del plot
    trees = Tree.objects.filter(plot=plot)
    tree_ids = trees.values_list('id', flat=True)

    # Filtrar SaleDistribution por plot y fechas
    # Obtener los harvests del plot
    from packages.farming.models import Harvest, Distribution
    harvests = Harvest.objects.filter(plot=plot)
    distributions = Distribution.objects.filter(harvest__in=harvests, type=Distribution.Type.SALE)
    sale_distributions = SaleDistribution.objects.filter(distribution__in=distributions)
    if start_date:
        sale_distributions = sale_distributions.filter(sale__date__gte=start_date)
    if end_date:
        sale_distributions = sale_distributions.filter(sale__date__lte=end_date)

    # Resumen general
    total_ventas = sum(float(dist.total_price) for dist in sale_distributions)
    print(_("PDF generado exitosamente."))

    # PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"ventas_plot_{plot.id}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50

    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, _(f"Resumen de Ventas - {plot.name}"))
    y -= 30
    p.setFont("Helvetica", 10)
    p.drawString(50, y, _(f"Ubicación: {plot.location or '-'} | Área: {plot.area_m2 or '-'} m²"))
    y -= 20
    if start_date or end_date:
        p.drawString(50, y, _(f"Filtro de fechas: {start_date or '-'} a {end_date or '-'}"))
        y -= 20
    p.drawString(50, y, _(f"Total ventas: ${total_ventas:.2f}"))
    y -= 30
    print(_("PDF generado exitosamente."))

    # Gráfico de barras: ventas por fecha
    fechas = []
    if sale_distributions.exists():
        from collections import defaultdict
        import datetime
        ventas_por_fecha = defaultdict(float)
        for dist in sale_distributions:
            fecha = dist.sale.date.strftime('%Y-%m-%d')
            ventas_por_fecha[fecha] += float(dist.total_price)
        fechas = sorted(ventas_por_fecha.keys())
        data = [[ventas_por_fecha[f] for f in fechas]]
        d = Drawing(400, 200)
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 30
        bc.height = 120
        bc.width = 300
        bc.data = data
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = max(data[0]) * 1.2 if data[0] else 1
        bc.valueAxis.valueStep = max(data[0]) / 5 if max(data[0]) > 0 else 1
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.categoryNames = fechas
        bc.bars[0].fillColor = colors.HexColor('#4e73df')

        bc.barLabels.nudge = 7  # separación vertical
        bc.barLabels.fontSize = 8
        bc.barLabels.angle = 0  # etiquetas horizontales
        bc.barLabels.fillColor = colors.black
        bc.barLabelFormat = '%0.2f'  # formato del número, ajusta según tu necesidad
        bc.barLabels.dy = 5  # posición vertical del texto

        # activar etiquetas por barra
        bc.barLabels.visible = True

        d.add(bc)
        render_y = y - 200
        d.drawOn(p, 50, render_y)
        y = render_y - 20

    # Detalle por árbol
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, _("Detalle de ventas:"))
    y -= 20
    p.setFont("Helvetica", 9)
    # for dist in sale_distributions.order_by('sale__date'):
    #     if y < 100:
    #         p.showPage()
    #         y = height - 50
    #     p.drawString(60, y, _(f"Fecha: {dist.sale.date} | Cantidad: {dist.distribution.quantity} | Precio: ${dist.total_price:.2f}"))
    #     y -= 15

    from collections import defaultdict
    from django.utils.formats import date_format

    # Agrupar distribuciones por fecha
    ventas_por_fecha = defaultdict(list)
    for dist in sale_distributions.order_by('sale__date'):
        fecha = dist.sale.date.strftime('%Y-%m-%d')
        ventas_por_fecha[fecha].append(dist)

    # Iterar por fecha ordenada
    for fecha in sorted(ventas_por_fecha.keys()):
        items = ventas_por_fecha[fecha]
        total_fecha = sum(float(d.total_price) for d in items)

        if y < 100:
            p.showPage()
            y = height - 50

        # Mostrar encabezado con fecha y total
        p.setFont("Helvetica-Bold", 10)
        p.drawString(60, y, f"Fecha: {fecha} | Total: ${total_fecha:.2f}")
        y -= 15

        # Mostrar detalle por item (cantidad y precio)
        p.setFont("Helvetica", 9)
        for dist in items:
            if y < 100:
                p.showPage()
                y = height - 50

            cantidad = dist.distribution.quantity
            precio = float(dist.total_price)
            p.drawString(80, y, f"Cantidad: {cantidad} | Precio: ${precio:.2f}")
            y -= 13
    p.showPage()
    p.save()
    return HttpResponse("PDF generado exitosamente.", content_type='application/pdf')
