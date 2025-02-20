import os
import PyPDF2
import requests
import weasyprint
from django.template.loader import render_to_string
from django.conf import settings


def pdf_generator(request, results, session_key):
    """
    Generates PDFs for the cover page and the comparison page.
    Then bundles those with the spec sheets into one packet for download by the user later

    :param request: web request from the results page
    :param results: list of turf items filted by the options selected by the user
    :param session_key: session key of the user's session
    :return: bool - returns if function was successful
    """
    paths = []
    context = {"results": results}

    for turf in results:
        response = requests.get(turf.spec_sheet_url, stream=True)
        path = os.path.join(settings.BASE_DIR, "media", f"{turf.name}.pdf")
        paths.append(path)
        if not os.path.exists(path):
            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"{path} downloaded")

    comparison_path = os.path.join(settings.BASE_DIR, "media", f"comparison_{session_key}.pdf")
    cover_path = os.path.join(settings.BASE_DIR, "media", f"cover_{session_key}.pdf")
    paths.append(comparison_path)
    paths.append(cover_path)

    comparison_html = render_to_string('pages/comparison.html', context)
    weasyprint.HTML(string=comparison_html).write_pdf(comparison_path)

    cover_html = render_to_string('pages/cover.html', context)
    weasyprint.HTML(string=cover_html).write_pdf(cover_path)

    output_path = os.path.join(settings.BASE_DIR, "media", f"packet_{session_key}.pdf")
    merger = PyPDF2.PdfMerger()
    for path in paths:
        with open(path, "rb") as f:
            merger.append(PyPDF2.PdfReader(f))

    with open(output_path, "wb") as f:
        merger.write(f)

    return True