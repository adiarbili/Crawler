import csv
import sys
import math
import re

# TFtd - Number of times that term t occurs in document d.
# DFt - Number of documents that contain term t.

IDFt = lambda N, DFt: math.log10(N / DFt) if DFt != 0 else 0.0
one_plus_log_TFdt = lambda TFdt: 1 + math.log10(TFdt) if TFdt != 0 else 0.0


def read_file(full_path):
    # list of content
    list = []

    with open(full_path, 'r', encoding="utf-8") as file:
        for line in file:
            if line != '\n':
                list.append(line.strip('\n'))

    return list


def TF_IDF(docs, terms):
    TF_IDF = []

    TF_list = TF(docs, terms)
    DF_list = calc_DFt(TF_list)
    log_IDF_list = calc_log_IDF(DF_list)

    one_plus_log_TF_list = calc_one_plus_log_TF(TF_list)

    i = 0

    for TF_row in one_plus_log_TF_list:
        TF_IDF_row = []
        log_IDF = log_IDF_list[i]
        for value in TF_row:
            TF_IDF_row.append(round(log_IDF * value, 3))

        i += 1
        TF_IDF.append(TF_IDF_row)

    return TF_list, DF_list, log_IDF_list, one_plus_log_TF_list, TF_IDF


def TF(docs, terms):
    TF_list = []

    for term in terms:
        TF_term = []
        # TF_term.append(TFtd(query, term))
        reg_term = '[^a-z]' + term + '[^a-z]|^' + term + '[^a-z]|[^a-z]' + term + '$|^' + term + '$'
        for doc in docs:
            TF_term.append(TFtd(doc, reg_term))

        TF_list.append(TF_term)

    return TF_list


def TFtd(doc, reg_term):
    TFtd = 0

    TFtd += len(re.findall(reg_term, doc, re.IGNORECASE))

    return TFtd


def calc_DFt(TF):
    DF_list = []

    for TFdt in TF:

        DFt = 0

        for val in TFdt:
            if val >= 1:
                DFt += 1

        DF_list.append(DFt)

    return DF_list


def calc_log_IDF(DF_list):
    log_IDF_list = []

    for DFt in DF_list:
        log_IDF_list.append(round(IDFt(number_of_doc, DFt), 3))

    return log_IDF_list


def calc_one_plus_log_TF(TF_list):
    res = []

    for TFdt in TF_list:
        TF_row = []
        for val in TFdt:
            TF_row.append(round(one_plus_log_TFdt(val), 3))

        res.append(TF_row)

    return res


documents = read_file("documents.txt")
terms = read_file("terms.txt")
# documents = read_file("docs_hw1.txt")
# terms = read_file("terms_hw1.txt")

number_of_doc = len(documents)

TF_list, DF_list, log_IDF_list, one_plus_log_TF_list, TF_IDF = TF_IDF(documents, terms)

print("TF table:")
print(*TF_list, sep="\n", end="\n\n")

print("DF table:")
print(DF_list, end="\n\n")

print("log IDF table:")
print(log_IDF_list, end="\n\n")

print("1+log(TF) table:")
print(*one_plus_log_TF_list, sep="\n", end="\n\n")

print("TF-IDF table:")
print(*TF_IDF, sep="\n", end="\n\n")
