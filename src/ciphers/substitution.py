def substitution(text, mapping):
    """Performs Substitution cipher on the input text. mapping should be a dictionary containing input_letter:output_letter"""
    text = text.upper()
    for k, v in mapping.items():
        text = text.replace(k.upper(), v.lower())
    return text
