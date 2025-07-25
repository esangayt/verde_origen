from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from packages.production.models import Plot, Tree
from packages.sales.models import SaleDistribution
from packages.farming.models import Harvest, Distribution
from collections import defaultdict


@staff_member_required
def plot_sales_pdf(request, plot_id):
    # Filtros por fecha
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    try:
        plot = get_object_or_404(Plot, pk=plot_id)
    except Plot.DoesNotExist:
        raise Http404(_('Plot not found'))

    # Detalle por parcela - a futuro se puede agregar más información
    # trees = Tree.objects.filter(plot=plot)
    # tree_ids = trees.values_list('id', flat=True)

    harvests = Harvest.objects.filter(plot=plot)
    distributions = Distribution.objects.filter(harvest__in=harvests, type=Distribution.Type.SALE)
    sale_distributions = SaleDistribution.objects.filter(distribution__in=distributions)

    if start_date:
        sale_distributions = sale_distributions.filter(sale__date__gte=start_date)
    if end_date:
        sale_distributions = sale_distributions.filter(sale__date__lte=end_date)

    # Resumen general
    total_ventas = sum(float(dist.total_price) for dist in sale_distributions)

    # PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"ventas_parcela_{plot.name}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    p = canvas.Canvas(response, pagesize=A4)
    p.setTitle(_("Resumen de Ventas - ") + plot.name)

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

    ventas_por_fecha = defaultdict(float)

    # Gráfico de barras: ventas por fecha
    if sale_distributions.exists():
        for dist in sale_distributions:
            fecha = dist.sale.date.strftime('%Y-%m-%d')
            ventas_por_fecha[fecha] += float(dist.total_price)

        fechas = sorted(ventas_por_fecha.keys())
        data = [[ventas_por_fecha[f] for f in fechas]]

        # Ajustar ancho y separación según cantidad de fechas
        n_fechas = len(fechas)
        chart_width = max(60 * n_fechas, 300)  # mínimo 300, 60px por fecha
        chart_height = 150

        d = Drawing(chart_width + 100, chart_height + 80)
        bc = VerticalBarChart()

        # Posición y tamaño del gráfico, a 50 px del borde izquierdo y 30 px del borde superior
        bc.x = 50
        bc.y = 30
        bc.height = chart_height
        bc.width = chart_width

        bc.data = data
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = max(data[0]) * 1.2 if data[0] else 1
        bc.valueAxis.valueStep = max(data[0]) / 5 if max(data[0]) > 0 else 1

        bc.categoryAxis.categoryNames = fechas

        bc.bars[0].fillColor = colors.HexColor('#4e73df')

        bc.barLabels.nudge = 7
        bc.barLabels.fontSize = 8
        bc.barLabels.angle = 0 if n_fechas <= 10 else 45  # rotar si hay muchas fechas
        bc.barLabels.fillColor = colors.black
        bc.barLabelFormat = '%0.2f'
        bc.barLabels.dy = 5
        bc.barLabels.visible = True
        d.add(bc)

        # Labels y título
        title = String(chart_width // 2 + 50, chart_height + 40, "Resumen de Ventas por Fecha", fontSize=14,
                       textAnchor="middle")
        x_label = String(chart_width // 2 + 50, 0, "Fechas", fontSize=10, textAnchor="middle")

        y_label = Label()
        y_label.setOrigin(bc.x - 40, chart_height // 2 + 30)
        y_label.textAnchor = "middle"
        y_label.fontName = "Helvetica"
        y_label.fontSize = 10
        y_label.angle = 90
        y_label.setText(_("Ventas (S/)"))

        d.add(y_label)
        d.add(x_label)
        d.add(title)

        # Centrar la gráfica si es más angosta que la página
        # Ubica al centro horizontalmente menos la mitad del ancho del gráfico
        render_x = width // 2 - (chart_width + 100) // 2
        render_y = y - (chart_height + 40)

        d.drawOn(p, render_x, render_y)
        y = render_y - 20

    # Detalle por árbol
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, _("Detalle de ventas:"))
    y -= 20
    p.setFont("Helvetica", 9)

    # from collections import defaultdict
    ventas_por_fecha = defaultdict(list)

    for dist in sale_distributions.order_by('sale__date'):
        fecha = dist.sale.date.strftime('%Y-%m-%d')
        ventas_por_fecha[fecha].append(dist)

    for fecha in sorted(ventas_por_fecha.keys()):
        items = ventas_por_fecha[fecha]
        total_fecha = sum(float(d.total_price) for d in items)

        if y < 100:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, y, _(f"Detalle de ventas (cont.):"))
            y -= 20

        p.setFont("Helvetica-Bold", 10)
        p.drawString(60, y, f"Fecha: {fecha} | Total: ${total_fecha:.2f}")
        y -= 15
        p.setFont("Helvetica", 9)

        for dist in items:
            if y < 100:
                p.showPage()
                y = height - 50
                p.setFont("Helvetica-Bold", 12)
                p.drawString(50, y, _(f"Detalle de ventas (cont.):"))
                y -= 20

            cantidad = dist.distribution.quantity
            precio = float(dist.total_price)
            p.drawString(80, y, f"Cantidad: {cantidad} | Precio: ${precio:.2f}")
            y -= 13
    p.save()
    return response
