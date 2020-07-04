import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
from matplotlib.backends.backend_pdf import PdfPages  # type: ignore


def test_pie_chart_with_matplotlib():
    labels = "Python", "C++", "Ruby", "Java"
    sizes = [215, 130, 245, 210]
    colors = ["gold", "yellowgreen", "lightcoral", "lightskyblue"]
    explode = (0.1, 0, 0, 0)  # explode 1st slice

    plt.pie(
        sizes, explode=explode, labels=labels, colors=colors, autopct="%1.1f%%", shadow=True, startangle=140,
    )

    plt.axis("equal")
    plt.show()


def test_table_with_matplotlib():
    fig, ax = plt.subplots()
    cell_text = [
        ["A", 1],
        ["B", 2],
        ["C", 3],
        ["D", 4],
        ["E", 5],
    ]
    column_labels = ["Letter", "Number"]
    loc = "center"  # top, center
    edges = "closed"  # open, closed, horizontal, vertical
    table = ax.table(cellText=cell_text, colLabels=column_labels, loc=loc, edges=edges)
    # table.set_fontsize(14)
    table.scale(0.5, 1.5)  # adjust row height to match font size
    ax.axis("off")
    # plt.tight_layout()
    plt.show()


def test_create_table_with_matplotlib():
    data = [
        [66386, 174296, 75131, 577908, 32015],
        [58230, 381139, 78045, 99308, 160454],
        [89135, 80552, 152558, 497981, 603535],
        [78415, 81858, 150656, 193263, 69638],
        [139361, 331509, 343164, 781380, 52269],
    ]

    columns = ("Freeze", "Wind", "Flood", "Quake", "Hail")
    rows = ["%d year" % x for x in (100, 50, 20, 10, 5)]

    values = np.arange(0, 2500, 500)
    value_increment = 1000

    # Get some pastel shades for the colors
    colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
    n_rows = len(data)

    index = np.arange(len(columns)) + 0.3
    bar_width = 0.4

    # Initialize the vertical-offset for the stacked bar chart.
    y_offset = np.zeros(len(columns))

    # Plot bars and create text labels for the table
    cell_text = []
    for row in range(n_rows):
        plt.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
        y_offset = y_offset + data[row]
        cell_text.append(["%1.1f" % (x / 1000.0) for x in y_offset])
    # Reverse colors and text labels to display the last value at the top.
    colors = colors[::-1]
    cell_text.reverse()

    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text, rowLabels=rows, rowColours=colors, colLabels=columns, loc="bottom", )

    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.2, bottom=0.2)

    plt.ylabel("Loss in ${0}'s".format(value_increment))
    plt.yticks(values * value_increment, ["%d" % val for val in values])
    plt.xticks([])
    plt.title("Loss by Disaster")

    plt.show()


def test_create_table_with_matplotlib_2():
    import numpy as np_
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.DataFrame(np_.random.randint(1, 50, size=(8, 4)), columns=list("ABCD"))
    df.index.name = "Name"

    fig, ax = plt.subplots()
    table = ax.table(
        cellText=df.values,
        rowLabels=df.index,
        cellLoc="center",
        colColours=["gainsboro"] * len(df),
        colLabels=df.columns,
        loc="center",
        colWidths=[0.12] * (len(df.columns)),
    )
    w, h = table[0, 1].get_width(), table[0, 1].get_height()
    table.add_cell(0, -1, w, h, text=df.index.name)
    plt.show()


def test_save_chart_to_pdf_with_matplotlib(tmp_path):
    with PdfPages(str(tmp_path / "pie_chart_matplotlib.pdf")) as pdf:
        labels = "Python", "C++", "Ruby", "Java"
        sizes = [215, 130, 245, 210]
        colors = ["gold", "yellowgreen", "lightcoral", "lightskyblue"]
        explode = (0.1, 0, 0, 0)  # explode 1st slice
        plt.pie(
            sizes, explode=explode, labels=labels, colors=colors, autopct="%1.1f%%", shadow=True, startangle=140,
        )
        pdf.savefig()
        plt.close()
