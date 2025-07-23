import pdfplumber
import re

NON_SECTION_HEADINGS = set([
    "ingredients", "instructions", "method", "preparation", "directions",
    "table of contents", "references", "appendix", "contents", "index", "notes"
])

# Add common action verbs (not used as likely headings) for even stricter action-line rejection
ACTION_VERBS = set([
    "add", "mix", "place", "remove", "pour", "heat", "spread", "beat", "drizzle",
    "serve", "bake", "cook", "boil", "fry", "grate", "garnish", "chop", "slice", "layer", "sauté", "return", "stir"
])

def is_probable_section_heading(line):
    line_strip = line.strip("•:.- ").strip()
    lstrip = line_strip.lower()

    if len(line_strip) < 4 or len(line_strip) > 80:
        return False
    if lstrip in NON_SECTION_HEADINGS:
        return False

    # Ingredient or numbered (e.g. recipe) lines
    if re.match(r'^\d', line_strip):
        return False
    if re.match(r'^\d+(\.\d+)*$', line_strip):
        return False

    # Ignore lines with units/quantities
    units = ['cup', 'tablespoon', 'teaspoon', 'grams', 'g', 'kg', 'ml', 'oz', 'lb', 'pound', 'slice', 'clove', 'slices', 'cloves', 'cups', 'tablespoons', 'teaspoons']
    if any(unit in lstrip for unit in units):
        return False

    # Remove lines with ingredient phrases or common step patterns
    bad_phrases = [
        "salt and pepper to taste", "season with salt and pepper", "add salt and pepper",
        "mixed greens", "add to taste", "to taste", "layer with"
    ]
    if any(phrase in lstrip for phrase in bad_phrases):
        return False

    # ********* Core improvement: reject lines starting with action verbs **********
    first_word = line_strip.split()[0].lower() if line_strip.split() else ""
    if first_word in ACTION_VERBS:
        return False

    # COMMUON CASES:
    if line_strip.isupper() and len(line_strip) > 4:
        return True
    if re.match(r'^\d+(\.\d+)*[\s\.:)\-]+', line_strip):
        return True
    if line_strip == line_strip.title() and 4 < len(line_strip) < 70 and len(line_strip.split()) > 1:
        return True
    if len(line_strip.split()) >= 2 and line_strip[0].isupper() and not line_strip[0].isdigit():
        return True

    return False

def extract_pdf_sections(pdf_path):
    document_sections = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                idx, n = 0, len(lines)
                while idx < n:
                    line = lines[idx]
                    if is_probable_section_heading(line):
                        # Uncomment below to debug headings:
                        # print(f"EXTRACTED: {repr(line)} (Page {i+1})")
                        section_lines = []
                        for offset in range(1, 16):
                            next_idx = idx + offset
                            if next_idx >= n:
                                break
                            next_line = lines[next_idx]
                            if is_probable_section_heading(next_line):
                                break
                            section_lines.append(next_line)
                        section_text = "\n".join(section_lines)[:1500]
                        if len(section_text.strip()) > 20:
                            document_sections.append({
                                "page": i + 1,
                                "title": line.strip("•:.- ")[:80],
                                "text": section_text
                            })
                        idx += max(1, len(section_lines))
                    else:
                        idx += 1
    except Exception as e:
        print(f"Could not process {pdf_path}: {e}")
    return document_sections
