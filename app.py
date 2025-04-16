import logging
import pdfplumber
import os
import pytz
import platform
from pathlib import Path
from prompt_toolkit.shortcuts import radiolist_dialog, message_dialog
from datetime import datetime


#   logger setup start
log_dir=Path.cwd() / "log"
log_dir.mkdir(parents=True, exist_ok=True)
timezone=pytz.timezone("Europe/Berlin")
time_now=datetime.now(timezone)
log_file=log_dir / f"{str(time_now)[:-22]}_{str(time_now)[11:-16]}.log"
logger=logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

file_handler=logging.FileHandler(log_file, encoding="utf-8")

formatter=logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
#   logger setup end


#   opens file, exstracts table data and retursns it
def get_table_data(file, page_number=0):
    with pdfplumber.open(file) as pdf:
        page=pdf.pages[page_number]
        table=page.extract_table()
    return table

#   initialize screen with list of .pdf files located in Input/ directory
def select_source_file_screen():
    if not os.path.exists("Input"):
        print("Can't locate 'Input' folder")
        return None
    elif len(os.listdir("Input"))==0:
        logger.info("Directory has no working PDF files.")
        result=message_dialog(
                title="Error",
                text="There're no files inside Input folder.",
                ).run()
        return result
    else:
        result=radiolist_dialog(
            title="Select input file:",
            values=[(i, i) for i in os.listdir("Input") if i.endswith(".pdf")],
    ).run()
    return result


#   main function
def main():
    try:
        logger.info("Session has started.")
        input_file=select_source_file_screen()
        index=0
        if input_file==None:
            print("No files were choosen or there were any.\nExiting...")
        else:
            logger.info(f"Selected file: {input_file}")
            print(f"Selected file: {input_file}\n")
            table_data = get_table_data(f"./Input/{input_file}")
            for row in table_data[1:]:
                index+=1
                print(f"[{index}]",row[1:-8])
                
            input("\nPress ENTER to continue with printing.")
    except:
        print("An error occurred. Try reading the documentation or reading logs.")
        return

if __name__ == "__main__":
    main()

