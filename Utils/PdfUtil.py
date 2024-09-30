# coding: utf-8

import PyPDF2

import re


def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        print(len(pdf_reader.pages))
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text().replace('\n', '')
        return text


pdf_file_path = '../SearchWords/sensitive_file.pdf'
text = extract_text_from_pdf(pdf_file_path)
text_file = '../Utils/output.txt'
with open(text_file, 'w', encoding='utf-8') as file1:
    file1.write(text)
print(text)
pattern = "(\D)\d*．(\D)"
res = re.findall(pattern, text)
print(res)
# with open("./output.txt", 'w') as f:
#     f.write(text)
