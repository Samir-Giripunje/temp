import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf, output_dir):
    """
    Splits a PDF file into smaller PDFs with 50 pages each and processes them using marker_single.

    :param input_pdf: Path to the input PDF file.
    :param output_dir: Directory to save the output PDFs.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    reader = PdfReader(input_pdf)
    total_pages = len(reader.pages)

    for i in range(0, total_pages, 50):
        writer = PdfWriter()
        
        # Add pages in chunks of 50
        for j in range(i, min(i + 50, total_pages)):
            writer.add_page(reader.pages[j])

        output_file = os.path.join(output_dir, f"{i // 50}.pdf")
        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)

        print(f"Created: {output_file}")

    process_with_marker(output_dir)

def process_with_marker(output_dir):
    """
    Processes all PDFs in the output directory using marker_single.

    :param output_dir: Directory containing the split PDFs.
    """
    pdf_files = sorted([f for f in os.listdir(output_dir) if f.endswith('.pdf')], key=lambda x: int(x.split('.')[0]))

    for pdf_file in pdf_files:
        pdf_path = os.path.join(output_dir, pdf_file)
        command = f"marker_single {pdf_path}"
        print(f"Executing: {command}")
        os.system(command)

def combine_md_files(input_dir, output_file):
    """
    Combines all .md files from sequentially named folders in the input directory into a single .md file.

    :param input_dir: Directory containing folders with .md files.
    :param output_file: Path to the output .md file.
    """
    folders = sorted([f for f in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, f))], key=lambda x: int(x))

    with open(output_file, "w") as outfile:
        for folder in folders:
            folder_path = os.path.join(input_dir, folder)
            md_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.md')], key=lambda x: int(x.split('.')[0]))

            for md_file in md_files:
                md_path = os.path.join(folder_path, md_file)
                with open(md_path, "r") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n\n")

    print(f"Combined .md files into: {output_file}")

if __name__ == "__main__":
    input_pdf_path = input("Enter the path to the input PDF file: ").strip()
    output_directory = input("Enter the directory to save split PDFs: ").strip()

    split_pdf(input_pdf_path, output_directory)

    conversion_results_dir = input("Enter the path to the conversion results directory: ").strip()
    combined_md_output = input("Enter the path for the combined .md output file: ").strip()

    combine_md_files(conversion_results_dir, combined_md_output)
