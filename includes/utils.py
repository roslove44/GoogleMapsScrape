import re
import tldextract


def is_valid_domain(domain):
    extracted = tldextract.extract(domain)
    return bool(extracted.domain and extracted.suffix)


def is_valid_phone_number(phone_number):
    pattern = r'^\+?[\d\s\-\.\(\)]{7,20}$'
    return bool(re.match(pattern, phone_number.strip())) and any(c.isdigit() for c in phone_number)


def security_of_null(variable):
    return variable.get_text() if variable else "N/A"


def contains_alphabet(string):
    pattern = re.compile(r'[a-zA-Z]')
    return bool(pattern.search(string))


def celebrity_indice(vote_count, average_note):
    if vote_count != "N/A" and average_note != "N/A":
        average_note = float(average_note.replace(",", ".").replace("\u202f", ""))
        vote_count = float(vote_count.replace("(", "").replace(")", "").replace("\u202f", ""))
        return round(average_note * vote_count)
    else:
        return 0
