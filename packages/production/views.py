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
    print(sale_distributions)
    if sale_distributions.exists():
        from collections import defaultdict
        import datetime
        ventas_por_fecha = defaultdict(float)
        for dist in sale_distributions:
            fecha = dist.sale.date.strftime('%Y-%m-%d')
            ventas_por_fecha[fecha] += float(dist.total_price)
        fechas = sorted(ventas_por_fecha.keys())
        data = [[ventas_por_fecha[f] for f in fechas]]
        # Ajustar ancho y separación según cantidad de fechas
        n_fechas = len(fechas)
        chart_width = max(60 * n_fechas, 300)  # mínimo 300, 60px por fecha
        chart_height = 120
        d = Drawing(chart_width + 100, chart_height + 80)
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 30
        bc.height = chart_height
        bc.width = chart_width
        bc.data = data
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = max(data[0]) * 1.2 if data[0] else 1
        bc.valueAxis.valueStep = max(data[0]) / 5 if max(data[0]) > 0 else 1
        bc.categoryAxis.labels.boxAnchor = 'ne'
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
        # Centrar la gráfica si es más angosta que la página
        render_x = 50
        render_y = y - (chart_height + 80)
        d.drawOn(p, render_x, render_y)
        y = render_y - 20

    # Detalle por árbol
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, _("Detalle de ventas:"))
    y -= 20
    p.setFont("Helvetica", 9)
    from collections import defaultdict
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
    # show a message in the frontend
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'

    return response
