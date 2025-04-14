import logging
import pdfplumber
import os
from prompt_toolkit.shortcuts import radiolist_dialog

logging.getLogger("pdfminer").setLevel(logging.ERROR)

def get_data(file, page_number=0):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[page_number]
        table = page.extract_table()
    return table

def get_input():
    if not os.path.exists("Input"):
        print("Can't locate 'Input' folder")
        return None
    result = radiolist_dialog(
        title = "Select input file:",
        values = [(i, i) for i in os.listdir("Input") if i.endswith(".pdf")],
    ).run()
    return result

def main():
    input_file = get_input()
    index=0
    if input_file == None:
        print("Exiting...")
    else:
        print(f"Selected file: {input_file}")
        table_data = get_data(f"./Input/{input_file}")
        for row in table_data:
            index+=1
            print(f"[{index}]",row[1:-8])


if __name__ == "__main__":
    main()

