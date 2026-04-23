#!/usr/bin/env python3
"""Generate a sample PDF with a table for testing pdf_to_csv.py."""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def create_sample():
    doc = SimpleDocTemplate("sample.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Sales Report - April 2026", styles["Title"]))
    elements.append(Spacer(1, 20))

    data = [
        ["Product Code", "Product Name", "Unit Price", "Qty", "Amount"],
        ["A001", "Laptop PC", "120,000", "5", "600,000"],
        ["A002", "Mouse", "3,500", "20", "70,000"],
        ["A003", "Keyboard", "8,000", "15", "120,000"],
        ["A004", "Monitor", "45,000", "8", "360,000"],
        ["A005", "USB Hub", "2,500", "30", "75,000"],
        ["", "Total", "", "", "1,225,000"],
    ]

    table = Table(data, colWidths=[90, 120, 80, 50, 90])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
                ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
                ("ALIGN", (0, 0), (1, -1), "CENTER"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
                ("BACKGROUND", (0, -1), (-1, -1), colors.beige),
                ("FONTSIZE", (0, -1), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    elements.append(table)
    doc.build(elements)
    print("sample.pdf created.")


if __name__ == "__main__":
    create_sample()
