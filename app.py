import logging
import pdfplumber
import os
from prompt_toolkit.shortcuts import radiolist_dialog, message_dialog

logging.getLogger("pdfminer").setLevel(logging.ERROR)

def get_table_data(file, page_number=0):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[page_number]
        table = page.extract_table()
    return table

def select_source_file_screen():
    if not os.path.exists("Input"):
        print("Can't locate 'Input' folder")
        return None
    elif len(os.listdir("Input")) == 0:
        result = message_dialog(
                title = "Error",
                text = "There're no files inside Input folder.",
                ).run()
        return result
    else:
        result = radiolist_dialog(
            title = "Select input file:",
            values = [(i, i) for i in os.listdir("Input") if i.endswith(".pdf")],
    ).run()
    return result

def main():
    try:
        input_file = select_source_file_screen()
        index=0
        if input_file == None:
            print("Exiting...")
        else:
            print(f"Selected file: {input_file}\n")
            table_data = get_table_data(f"./Input/{input_file}")
            for row in table_data[1:]:
                index+=1
                print(f"[{index}]",row[1:-8])
            input("\nPress Enter to continue with printing.")
    except:
        print("An error occurred. Try reading the documentation.")
        return

if __name__ == "__main__":
    main()

