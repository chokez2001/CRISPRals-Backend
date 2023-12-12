def get_percentage(value, total):
    return round((value * 100) / total, 1)

def format_accession_number(rf, gen_bank):
    return f"RF:{rf or '-'} GenBank: {gen_bank or '-'}"


def format_repeat_sequences(array_repeat_sequences):
    if array_repeat_sequences is None:
        return '-'
    return array_repeat_sequences.replace("\n", '')
