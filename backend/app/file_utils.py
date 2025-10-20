from docx import Document
import io
from concurrent.futures import ThreadPoolExecutor
from services.ocr_service import extract_text_from_image
import logging

logger = logging.getLogger(__name__)

# Thread pool to handle OCR in parallel
ocr_executor = ThreadPoolExecutor(max_workers=5)  # Adjust number of workers to your rate limits and performance needs

def extract_text_from_file(file_bytes, filename):
    text = ""

    if filename.endswith(".txt"):
        text = file_bytes.decode("utf-8")

    elif filename.endswith(".docx"):
        doc = Document(io.BytesIO(file_bytes))
        
        # Extract text from paragraphs
        text += "\n".join(p.text for p in doc.paragraphs)

        # Collect all images
        all_images = []
        processed_hashes = set()
        
        # Normal paragraph images
        for paragraph in doc.paragraphs:
            all_images.extend(_get_images_from_paragraph(paragraph))

        # Table images
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        all_images.extend(_get_images_from_paragraph(paragraph))

        # Header and Footer images
        for section in doc.sections:
            for paragraph in section.header.paragraphs:
                all_images.extend(_get_images_from_paragraph(paragraph))
            for paragraph in section.footer.paragraphs:
                all_images.extend(_get_images_from_paragraph(paragraph))

        # Images from related_parts (avoid duplicates with hash)
        for rel in doc.part.related_parts.values():
            if getattr(rel, "content_type", "").startswith("image/"):
                try:
                    img_bytes = rel.blob
                    img_hash = hash(img_bytes)
                    if img_hash not in processed_hashes:
                        processed_hashes.add(img_hash)
                        all_images.append(img_bytes)
                except Exception as e:
                    logger.warning(f"Error obtaining image from related_parts: {e}")

        # Process all images with parallel OCR
        if all_images:
            logger.info(f"Processing {len(all_images)} images...")
            ocr_texts = _process_images_parallel(all_images)
            text += "\n" + "\n".join(filter(None, ocr_texts))

    else:
        raise ValueError("Format not supported for text extraction")

    return text.strip()


def _get_images_from_paragraph(paragraph):
    images = []
    for run in paragraph.runs:
        images.extend(_get_images_from_run(run))
    return images


def _get_images_from_run(run):
    images = []
    for element in run._element.iter():
        if element.tag.endswith("blip"):
            embed_id = element.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
            if embed_id:
                try:
                    part = run._parent._parent.part.related_part(embed_id)
                    images.append(part.blob)
                except Exception as e:
                    logger.warning(f"Error obtaining image from run: {e}")
    return images


def _process_images_parallel(images):
    futures = []
    
    for img_bytes in images:
        future = ocr_executor.submit(extract_text_from_image, img_bytes)
        futures.append(future)
    
    results = []
    for i, future in enumerate(futures, 1):
        try:
            result = future.result(timeout=60)
            results.append(result)
            logger.info(f"Image {i}/{len(futures)} processed")
        except Exception as e:
            logger.error(f"Error processing image {i}/{len(futures)}: {e}")
            results.append(None)
    
    return results