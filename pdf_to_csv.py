#!/usr/bin/env python3
"""
PDF to CSV extractor.
Extracts tables and text data from PDF files and writes them to CSV.
"""

import argparse
import csv
import sys
from pathlib import Path

import pdfplumber


def extract_tables(pdf_path: str) -> list[list[list[str | None]]]:
    """Extract all tables from every page of the PDF."""
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)
    return tables


def extract_text_as_rows(pdf_path: str) -> list[list[str]]:
    """Fallback: extract text lines as single-column CSV rows."""
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.splitlines():
                    line = line.strip()
                    if line:
                        rows.append([line])
    return rows


def tables_to_csv(tables: list[list[list[str | None]]], output_path: str) -> int:
    """Write extracted tables to CSV. Returns total row count written."""
    total_rows = 0
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for i, table in enumerate(tables):
            if i > 0:
                writer.writerow([])  # blank separator between tables
            for row in table:
                cleaned = [cell if cell is not None else "" for cell in row]
                writer.writerow(cleaned)
                total_rows += 1
    return total_rows


def text_rows_to_csv(rows: list[list[str]], output_path: str) -> int:
    """Write text rows to CSV. Returns total row count written."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return len(rows)


def convert(pdf_path: str, output_path: str) -> None:
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading: {pdf_path}")
    tables = extract_tables(pdf_path)

    if tables:
        print(f"Found {len(tables)} table(s). Extracting to CSV...")
        count = tables_to_csv(tables, output_path)
        print(f"Done. {count} row(s) written to: {output_path}")
    else:
        print("No tables detected. Falling back to plain text extraction...")
        rows = extract_text_as_rows(pdf_path)
        if not rows:
            print("No text content found in PDF.", file=sys.stderr)
            sys.exit(1)
        count = text_rows_to_csv(rows, output_path)
        print(f"Done. {count} row(s) written to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert PDF tables/text to CSV")
    parser.add_argument("pdf", help="Path to input PDF file")
    parser.add_argument(
        "-o",
        "--output",
        help="Path to output CSV file (default: same name as PDF with .csv extension)",
    )
    args = parser.parse_args()

    output = args.output or str(Path(args.pdf).with_suffix(".csv"))
    convert(args.pdf, output)


if __name__ == "__main__":
    main()
