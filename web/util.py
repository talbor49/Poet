def capitalize_first_letter(s):
    if s and len(s) > 1:
        capitalized = s[0].upper() + s[1:]
        return capitalized
    return ''
