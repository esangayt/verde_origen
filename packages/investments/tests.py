# from matplotlib.backends.backend_pdf import PdfPages
# import matplotlib.pyplot as plt
#
# with PdfPages("grafico_matplotlib.pdf") as pdf:
#     plt.bar(["Ene", "Feb", "Mar", "Abr"], [10, 20, 30, 40])
#     plt.xlabel("Meses")
#     plt.ylabel("Valores")
#     plt.title("Ventas mensuales")
#     pdf.savefig()
#     plt.close()

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np

# Datos
categorias = ['Ene', 'Feb', 'Mar', 'Abr']
serie1 = [10, 20, 30, 40]
serie2 = [15, 22, 28, 35]
x = np.arange(len(categorias))  # posiciones en eje X
bar_width = 0.35

# Crear PDF
with PdfPages("grafico_matplotlib.pdf") as pdf:
    fig, ax = plt.subplots(figsize=(8.5, 5.5))  # Tamaño carta aproximado en pulgadas

    # Barras
    bars1 = ax.bar(x - bar_width/2, serie1, bar_width, label='Serie 1', color='blue')
    bars2 = ax.bar(x + bar_width/2, serie2, bar_width, label='Serie 2', color='green')

    # Título y etiquetas de ejes
    ax.set_title("Ventas mensuales")
    ax.set_xlabel("Meses")
    ax.set_ylabel("Valores")
    ax.set_xticks(x)
    ax.set_xticklabels(categorias)
    ax.set_ylim(0, 50)
    ax.legend()

    # Añadir etiquetas de valor encima de cada barra (opcional)
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # separación del texto
                        textcoords="offset points",
                        ha='center', va='bottom')

    add_labels(bars1)
    add_labels(bars2)

    # Guardar página en PDF
    pdf.savefig()
    plt.close()

