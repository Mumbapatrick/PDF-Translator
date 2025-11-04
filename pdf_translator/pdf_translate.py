import fitz
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException
import time
import sys

MAX_CHARS = 5000
DEFAULT_FONT = "helv"

def chunk_text(text, max_len=MAX_CHARS):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_len, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks

def translate_text(text, target_lang="fr", auto_detect=True):
    text = text.strip()
    if not text:
        return text
    source_lang = "auto"
    if auto_detect:
        try:
            source_lang = detect(text)
        except LangDetectException:
            return text
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        chunks = chunk_text(text)
        translated_chunks = [translator.translate(chunk) for chunk in chunks]
        return " ".join(translated_chunks)
    except Exception as e:
        print(f"[!] Translation error: {e}")
        return text

def int_to_rgb(color_int):
    if isinstance(color_int, int):
        r = ((color_int >> 16) & 255) / 255
        g = ((color_int >> 8) & 255) / 255
        b = (color_int & 255) / 255
        return (r, g, b)
    return (0, 0, 0)

def wrap_text(text, font, fontsize, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        width = font.text_length(test_line, fontsize)
        if width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def insert_text_in_rect(page, rect, text, fontname, color, fontsize):
    line_spacing = 1.2
    font = fitz.Font(fontname=fontname)
    while fontsize > 4:
        lines = wrap_text(text, font, fontsize, rect.width)
        total_height = len(lines) * fontsize * line_spacing
        if total_height <= rect.height:
            y_offset = rect.y0
            for line in lines:
                page.insert_text((rect.x0, y_offset), line, fontname=fontname, fontsize=fontsize, color=color)
                y_offset += fontsize * line_spacing
            break
        fontsize -= 0.5
    return fontsize

def translate_pdf_text_only(input_pdf_path, output_pdf_path, target_lang="fr", auto_detect=True):
    print(f"[+] Starting translation of {input_pdf_path}")
    start_time = time.time()
    doc = fitz.open(input_pdf_path)

    total_pages = len(doc)
    for page_number, page in enumerate(doc, start=1):
        sys.stdout.write(f"\r🔄 Processing page {page_number}/{total_pages}...")
        sys.stdout.flush()
        blocks = page.get_text("dict")["blocks"]
        translations = []

        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    original_text = span["text"].strip()
                    if not original_text:
                        continue
                    translated_text = translate_text(original_text, target_lang, auto_detect)
                    rect = fitz.Rect(span["bbox"])
                    color = int_to_rgb(span.get("color", 0))
                    fontsize = span["size"]

                    translations.append({
                        "rect": rect,
                        "text": translated_text,
                        "color": color,
                        "fontsize": fontsize
                    })
                    page.add_redact_annot(rect, fill=(1, 1, 1))

        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

        for t in translations:
            insert_text_in_rect(page, t["rect"], t["text"], DEFAULT_FONT, t["color"], t["fontsize"])

    doc.save(output_pdf_path)
    doc.close()

    end_time = time.time()
    print(f"\n✅ Translation completed: {output_pdf_path}")
    print(f"⏱ Duration: {round(end_time - start_time, 2)} seconds\n")
    return output_pdf_path
