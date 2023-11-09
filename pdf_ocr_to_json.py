import json
import base64
import pytesseract
from pdf2image import convert_from_path
import glob
import shutil,os

def ocr_extraction(abs_file_name,data_file):
    if abs_file_name is None : return -1
    # pdfFile = wi(filename = abs_file_name, resolution = 300)
    data_json_list = None
    if os.path.isfile(data_file):
        with open(data_file, "r") as fp:   
            data_json_list = json.load(fp)
        if data_json_list is None: return -1
    pdfs = glob.glob(abs_file_name)
    print(abs_file_name)
    print("pdfs:",pdfs)
    for pdf_path in pdfs:
        pages = convert_from_path(pdf_path, 500)
    content_page_wise = []    
    for index,imgBlob in enumerate(pages):
        text = pytesseract.image_to_string(imgBlob,lang='eng')
        # print(base64.b64encode(bytearray(imgBlob) ))
        t ={ "pagenumber" : index,
            "category":data_json_list[index].get("category"),
            
            "Data": data_json_list[index].get("Data"),
            
            "ImageText" : text,
            
            "Isstart":data_json_list[index].get("Isstart")
            
           }
        content_page_wise.append(t)
    converted_ocr_base_dir = "/home/axe/GITHUB/KPO/OCR_PAGES/"
    file_name = os.path.basename(abs_file_name)
    file_name_without_extension = os.path.join(converted_ocr_base_dir,file_name.rpartition(".")[0] + ".json")
    print("json_file:",file_name_without_extension)
    with open(file_name_without_extension,"w") as fp:
        json.dump(content_page_wise,fp,indent=4)
        shutil.move(abs_file_name,r"/home/axe/GITHUB/KPO/PROCESSED")
    return content_page_wise

if __name__ == '__main__':
    ocr_extraction(abs_file_name=r'/home/axe/GITHUB/KPO/TO_PROCESS/21-123-1921.pdf',data_file=r'/home/axe/GITHUB/KPO/TO_PROCESS/21-123-1921.json')