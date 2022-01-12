
import pyautogui
import pdfplumber
import win32com.client as win32
import shutil

refined_table = []

with pdfplumber.open(r"C:\Users\home\Desktop\water\water.pdf") as pdf:
    pages = pdf.pages

    for page in pdf.pages:
        for table in page.extract_tables():
            if table[0][0] == '나.항목별 검사결과':
                for item in table:
                    if item[0] != '나.항목별 검사결과' and item[0] != '검 사 항 목':
                        refined_table.append(item)


shutil.copyfile(r"C:\Users\home\Desktop\water\water.hwp", r"C:\Users\home\Desktop\water\water_new.hwp")
hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
# hwp.XHwpWindows.Item(0).Visible = True
hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
# hwp
hwp.Open(r"C:\Users\home\Desktop\water\water_new.hwp")
pyautogui.hotkey('alt', 'tab')

field_list = [i for i in hwp.GetFieldList().split("\x02")]

for page, cols in enumerate(refined_table):
    if page == len(refined_table) - 1: break
    hwp.Run("TableCellBlockRow")
    hwp.Run('Copy')
    # hwp.Run('Paste')
    # hwp.Run("TableInsertLowerRow")
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('b')
    pyautogui.hotkey('d')

for page, cols in enumerate(refined_table):
    for index, field in enumerate(field_list):
        hwp.PutFieldText(f'{field}{{{{{page}}}}}', cols[index+1])
