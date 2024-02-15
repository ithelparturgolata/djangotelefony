from django.http import HttpResponse
import zipfile
from django.shortcuts import render
from PyPDF2 import PdfReader, PdfWriter
import os
import tempfile

def split_pdf(request):
    if request.method == 'POST':
        try:
            pdf_file = request.FILES['pdf_file']
            num_pages = int(request.POST.get('num_pages'))
            base_name = request.POST.get('base_name')
            different_name = request.POST.get('different_name')

            # Read PDF file
            pdf_reader = PdfReader(pdf_file)
            num_total_pages = len(pdf_reader.pages)

            # Split PDF file
            start_page = 0
            file_counter = 1
            output_files = []

            while start_page < num_total_pages:
                pdf_writer = PdfWriter()
                end_page = min(start_page + num_pages, num_total_pages)
                for page_num in range(start_page, end_page):
                    pdf_writer.add_page(pdf_reader.pages[page_num])

                output_file_name = f'{base_name}{file_counter:03d}{different_name}.pdf'  # Format with leading zeros
                output_file_path = os.path.join(tempfile.gettempdir(), output_file_name)

                with open(output_file_path, 'wb') as output_file:
                    pdf_writer.write(output_file)

                output_files.append(output_file_path)

                start_page += num_pages
                file_counter += 1

            # Prepare the response to prompt download
            zip_filename = 'split_pdfs.zip'
            response = HttpResponse(content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

            # Create a zip file containing all split PDF files
            with zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in output_files:
                    zipf.write(file_path, arcname=os.path.basename(file_path))

            # Clean up temporary files
            for file_path in output_files:
                os.remove(file_path)

            return response
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    return render(request, 'split_pdf.html')
