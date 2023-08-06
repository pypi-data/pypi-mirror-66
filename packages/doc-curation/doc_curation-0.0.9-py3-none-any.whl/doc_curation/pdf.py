"""
Curate and process pdf files.
"""
import errno
import logging
import os
import shutil

from pikepdf import Pdf
from pathlib import Path

from curation_utils import list_helper, file_helper

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s")


def _get_ocr_dir(pdf_path):
    return os.path.join(os.path.dirname(pdf_path), Path(pdf_path).stem + "_splits")


def split_and_ocr_on_drive(pdf_path, google_key='/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/service_account_key.json', 
        small_pdf_pages=25, start_page=1, end_page=None, pdf_compression_power=0):
    """
    OCR some pdf with google drive. Automatically splits into 25 page bits and ocrs them individually.
    
    We compress the pdf provided (if compression_power>0) because:

     -  If drive API detects text in your pdf it won't OCR the image and will just return the text it found
     - If a PDF has layers, google drive ocr fails. Need to print into a pdf in such a case. 
     - One does not need insane resolution to OCR. I guessed that file size and/or resolution is a critical factor in determining if OCR via Drive API succeeds.

    However, pdf compression results in reduction in OCR accuracy. So, beware that tradeoff.

    Still, sometimes, the operation may time out, or you might get an Internal service error. In that case, try reducing small_pdf_pages or increasing the compression power.
    
    :param pdf_path:
    :param google_key: A json key which can be obtained from https://console.cloud.google.com/iam-admin/serviceaccounts (create a project, generate a key via "Actions" column.). 
    :param small_pdf_pages: Number of pages per segment - an argument used for splitting the pdf into small bits for OCR-ing. 
    :param pdf_compression_power: 0,1,2,3,4
    :return: 
    """
    
    compressed_pdf_path = pdf_path.replace(".pdf", "_tiny.pdf")
    compress_with_gs(input_file_path=pdf_path, output_file_path=compressed_pdf_path, power=pdf_compression_power)
    split_into_small_pdfs(pdf_path=compressed_pdf_path, small_pdf_pages=small_pdf_pages, start_page=start_page, end_page=end_page)
    
    # Do the OCR
    from curation_utils.google import drive
    drive_client = drive.get_cached_client(google_key=google_key)
    pdf_segments = [str(pdf_segment) for pdf_segment  in Path(_get_ocr_dir(compressed_pdf_path)).glob("*.pdf")]
    ocr_segments = sorted([pdf_segment + ".txt" for pdf_segment in pdf_segments])
    for pdf_segment in sorted(pdf_segments):
        drive_client.ocr_file(local_file_path=str(pdf_segment))
        os.remove(pdf_segment)
    
    # Combine the ocr segments
    final_ocr_path = pdf_path + ".txt"
    file_helper.concatenate_files(input_path_list=ocr_segments, output_path=final_ocr_path)


def split_into_small_pdfs(pdf_path, output_directory=None, start_page=1, end_page=None, small_pdf_pages=25):

    pdf_name_stem = Path(pdf_path).stem
    if output_directory == None:
        output_directory = _get_ocr_dir(pdf_path)
    # noinspection PyArgumentList
    with Pdf.open(pdf_path) as pdf:
        if end_page == None:
            end_page = len(pdf.pages)
        pages = range(start_page, end_page+1)
        page_sets = list_helper.divide_chunks(list_in=pages, n=small_pdf_pages)
        for page_set in page_sets:
            pages = [pdf.pages[i-1] for i in page_set]
            dest_pdf_path = os.path.join(output_directory, "%s_%04d-%04d.pdf" % (pdf_name_stem, page_set[0], page_set[-1]))
            if not os.path.exists(dest_pdf_path):
                # noinspection PyArgumentList
                dest_pdf = Pdf.new()
                dest_pdf.pages.extend(pages)
                os.makedirs(os.path.dirname(dest_pdf_path), exist_ok=True)
                dest_pdf.save(filename=dest_pdf_path)
            else:
                logging.warning("%s exists", dest_pdf_path)

# Adapted from https://github.com/theeko74/pdfc/blob/master/pdf_compressor.py
def compress_with_gs(input_file_path, output_file_path, power=3):
    """Function to compress PDF and remove text via Ghostscript command line interface
    
    :param power: 0,1,2,3,4
    """
    quality = {
        0: '/default',
        1: '/prepress',
        2: '/printer',
        3: '/ebook',
        4: '/screen'
    }

    # Basic controls
    # Check if valid path
    if not os.path.isfile(input_file_path):
        logging.fatal("Error: invalid path for input PDF file")
        return

        # Check if file is a PDF by extension
    if input_file_path.split('.')[-1].lower() != 'pdf':
        logging.fatal("Error: input file is not a PDF")
        return

    logging.info("Compress PDF...")
    initial_size = os.path.getsize(input_file_path)
    import subprocess
    try:
        subprocess.call(['gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                         '-dPDFSETTINGS={}'.format(quality[power]),
                         '-dFILTERTEXT',
                         '-dNOPAUSE', '-dQUIET', '-dBATCH',
                         '-sOutputFile={}'.format(output_file_path),
                         input_file_path]
                        )
    except OSError as e:
        if e.errno == errno.ENOENT:
            # handle file not found error.
            logging.error("ghostscript not found. Proceeding without compression.")
            shutil.copyfile(input_file_path, output_file_path)
            return
        else:
            # Something else went wrong while trying to run the command
            raise
    final_size = os.path.getsize(output_file_path)
    ratio = 1 - (final_size / initial_size)
    logging.info("Compression by {0:.0%}.".format(ratio))
    logging.info("Final file size is {0:.1f}MB".format(final_size / 1000000))
    return ratio


