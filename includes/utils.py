import re
import tldextract


def is_valid_domain(domain):
    domain = domain.strip()
    if ' ' in domain or '.' not in domain:
        return False
    extracted = tldextract.extract(domain)
    return bool(extracted.domain and extracted.suffix)


def is_valid_phone_number(phone_number):
    pattern = r'^\+?[\d\s\-\.\(\)]{7,20}$'
    return bool(re.match(pattern, phone_number.strip())) and any(c.isdigit() for c in phone_number)


def get_text_or_na(element):
    return element.get_text(strip=True) if element else "N/A"


def celebrity_indice(vote_count, average_note):
    if vote_count == "N/A" or average_note == "N/A":
        return 0
    note = float(average_note.replace(",", ".").replace("\u202f", ""))
    votes = float(vote_count.replace("(", "").replace(")", "").replace("\u202f", ""))
    return round(note * votes)
