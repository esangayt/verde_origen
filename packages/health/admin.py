from django.contrib import admin

from packages.health.models import Agrochemical, KindAgrochemical, ChemicalControl
from packages.production.models import Plot
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from io import BytesIO
from django.utils import timezone
from django.contrib import admin
from django.http import HttpResponse

@admin.register(KindAgrochemical)
class KindAgrochemicalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(ChemicalControl)
class ChemicalControlAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'plot', 'agrochemical', 'dosage', 'unit', 'responsible')
    search_fields = ('plot__name', 'agrochemical__name', 'responsible', 'unit')
    list_filter = ('date', 'plot', 'agrochemical')
    ordering = ('-date',)


@admin.register(Agrochemical)
class AgrochemicalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'kind', 'measurement_unit', 'stock')
    search_fields = ('name', 'kind__name')
    list_filter = ('kind', 'measurement_unit', 'kind__name')
    ordering = ('name',)
    actions = ['exportar_a_pdf']

    def marcar_como_aprobado(self, request, queryset):
        self.message_user(request, "Los elementos seleccionados fueron marcados como aprobados.", messages.SUCCESS)

    marcar_como_aprobado.short_description = "Marcar como aprobado"

    # Acción PDF
    def exportar_a_pdf(self, request, queryset):
        """
        Exporta los agroquímicos seleccionados junto con todos sus ChemicalControls relacionados.
        """
        # Prefetch de relaciones para evitar N+1 queries
        qs = queryset.select_related('kind').prefetch_related('chemical_controls__plot')

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margin = 2 * cm

        self._pdf_encabezado(p, width, height)
        y = height - 3 * cm

        for agro in qs:
            # Si no hay espacio suficiente para otro agro, saltamos página
            if y < 5 * cm:
                p.showPage()
                self._pdf_encabezado(p, width, height)
                y = height - 3 * cm

            y = self._draw_agrochemical(p, agro, margin, y, width)
            y -= 10  # Espacio extra entre agroquímicos

        p.save()
        buffer.seek(0)
        return self._download_response(buffer, "agrochemicals.pdf")

    exportar_a_pdf.short_description = "Exportar agroquímicos seleccionados a PDF"

    # -------- Helpers PDF -------- #

    def _pdf_encabezado(self, p, width, height):
        p.setFont("Helvetica-Bold", 14)
        p.drawString(2 * cm, height - 1.5 * cm, "Reporte de Agroquímicos")
        p.setFont("Helvetica", 9)
        p.drawString(2 * cm, height - 2.0 * cm, f"Generado: {timezone.now():%Y-%m-%d %H:%M}")

    def _draw_agrochemical(self, p, agro, x, y, width):
        line_gap = 12
        usable_width = width - 2 * x

        # Encabezado del agroquímico
        p.setFont("Helvetica-Bold", 12)
        p.drawString(x, y, f"{agro.name} (ID {agro.pk})")
        y -= line_gap

        p.setFont("Helvetica", 10)
        y = self._draw_kv(p, x, y, "Tipo", str(agro.kind))
        y = self._draw_kv(p, x, y, "Unidad de medida", agro.get_measurement_unit_display())
        y = self._draw_kv(p, x, y, "Stock", agro.stock)

        # Dibujar ChemicalControls relacionados
        chemical_controls = agro.chemical_controls.all().order_by('-date')
        if chemical_controls:
            p.setFont("Helvetica-Bold", 10)
            p.drawString(x, y, "Controles químicos:")
            y -= line_gap

            p.setFont("Helvetica", 9)
            for control in chemical_controls:
                # Si el espacio en la página se acaba
                if y < 2 * cm:
                    p.showPage()
                    self._pdf_encabezado(p, width, A4[1])
                    y = A4[1] - 3 * cm

                linea = f"- {control.date:%Y-%m-%d}, Parcela: {control.plot}, " \
                        f"Dosis: {control.dosage}{control.unit}, " \
                        f"Resp: {control.responsible}"
                p.drawString(x + 10, y, linea)
                y -= line_gap

                # Observaciones
                if control.observations:
                    p.setFont("Helvetica-Oblique", 8)
                    p.drawString(x + 20, y, f"Obs: {control.observations}")
                    p.setFont("Helvetica", 9)
                    y -= line_gap

        # Separador
        p.setLineWidth(0.2)
        p.line(x, y, x + usable_width, y)
        y -= line_gap
        return y

    def _draw_kv(self, p, x, y, label, value):
        p.setFont("Helvetica-Bold", 10)
        p.drawString(x, y, f"{label}:")
        p.setFont("Helvetica", 10)
        p.drawString(x + 100, y, str(value))
        return y - 12

    def _download_response(self, buffer, filename):
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response