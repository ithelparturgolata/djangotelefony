from django.shortcuts import render
from PyPDF2 import PdfReader, PdfWriter
import os
from django.shortcuts import render
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def split_pdf(request):
    if request.method == 'POST':
        try:
            pdf_file = request.FILES['pdf_file']
            num_pages = int(request.POST.get('num_pages'))
            output_dir = request.POST.get('output_dir')
            base_name = request.POST.get('base_name')

            # Create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Read PDF file
            pdf_reader = PdfReader(pdf_file)
            num_total_pages = len(pdf_reader.pages)

            # Split PDF file
            start_page = 0
            file_counter = 1
            while start_page < num_total_pages:
                pdf_writer = PdfWriter()
                end_page = min(start_page + num_pages, num_total_pages)
                for page_num in range(start_page, end_page):
                    pdf_writer.add_page(pdf_reader.pages[page_num])

                output_file_name = f'{base_name}{file_counter:03d}.pdf'  # Format with leading zeros
                output_file_path = os.path.join(output_dir, output_file_name)
                with open(output_file_path, 'wb') as output_file:
                    pdf_writer.write(output_file)

                start_page += num_pages
                file_counter += 1

            return render(request, 'split_pdf_success.html')
        except Exception as e:
            return render(request, 'split_pdf.html', {'error_message': str(e)})
    else:
        return render(request, 'split_pdf.html')
