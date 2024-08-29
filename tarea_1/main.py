import unicodedata
import numpy as np
import re
from tabulate import tabulate


allowed_characters = re.compile(r"[^a-zA-Z0-9áéíóúñÁÉÍÓÚÑüÜ'\s-]")

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str.lower())
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def process_phrases(doc):
    phrases = []
    processed_phrases = []
    with open(doc, 'r', encoding='utf-8') as file:
        for phrase in file.readlines():
            no_accents_phrase = remove_accents(phrase)
            sanitized_phrase = re.sub(
                allowed_characters,
                "",
                no_accents_phrase).replace("\n", "")

            phrases.append(phrase)
            processed_phrases.append(sanitized_phrase)
    return phrases, processed_phrases


def obtain_w(phrase, keywords):
    w = np.zeros(len(keywords))
    idx = 0
    splitted_phrase = phrase.split(" ")
    for word in keywords:
        if word in splitted_phrase:
            w[idx] = 1
            idx += 1
    return w


def obtain_s(phrase, positive_words, neutral_words, negative_words):
    s = np.zeros(3)
    splitted_phrase = phrase.split(" ")
    for word in splitted_phrase:
        if word in positive_words:
            s[0] += 1
        elif word in neutral_words:
            s[1] += 1
        elif word in negative_words:
            s[2] += 1
    return s


def calculate_avg_quality(w, keywords_qty):
    words_sum = 0
    for n in w:
        words_sum += n
    return words_sum / keywords_qty


def calculate_feelings_avg(s):
    total_keywords_qty = 0

    for keyword_type_qty in s:
        total_keywords_qty += keyword_type_qty

    avg_positive_s = s[0]/total_keywords_qty
    avg_neutral_s = s[1]/total_keywords_qty
    avg_negative_s = s[2]/total_keywords_qty

    return avg_positive_s, avg_neutral_s, avg_negative_s


def main():
    positive_words = np.array([
        "encanto", "fascinante", "epico", "hermoso", "impresionante",
        "divertida", "mejor", "moderno"
    ])

    neutral_words = np.array([
        "preguntas", "esperaba", "siento", "necesito", "pienso", "piensa",
        "puro", "enganchado", "profunda", "clasico"
    ])

    negative_words = np.array([
        "complicadas", "decepcion", "predecible", "corta", "locura", "lloro",
        "fuerte"
    ])

    keywords = np.concatenate((
        positive_words,  neutral_words, negative_words
    ))

    phrases, processed_phrases = process_phrases("phrases.txt")

    table = [
        ['Phrase', 'Quality', 'Positive', 'Neutral', 'Negative']
    ]

    idx = 0
    for p in processed_phrases:
        w = obtain_w(p, keywords)
        s = obtain_s(p, positive_words, neutral_words, negative_words)

        quality = calculate_avg_quality(w, len(keywords))

        (avg_positive_s,
         avg_neutral_s,
         avg_negative_s) = calculate_feelings_avg(s)

        row = [phrases[idx], quality, avg_positive_s, avg_neutral_s, avg_negative_s]
        table.append(row)
        idx += 1

    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))





if __name__ == '__main__':
    main()