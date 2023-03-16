import shutil
from bs4 import BeautifulSoup
import chardet
import os
import win32com.client as win32
import zipfile
import glob
from entity_load import *

def check_file_error(filename):
    with open(filename, "r", encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    for line in lines:
        if line.find('判决'):
            return False

    return True

#给一个文件夹的路径，将该路径下的所有doc转为txt，并且保留源文件
def doc_to_txt_old(folder_path):
    # 遍历文件夹下所有.doc文件
    word = win32.gencache.EnsureDispatch('Word.Application')
    file_cnt = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".doc"):
                file_cnt += 1
                if file_cnt % 20 == 0:
                    print('Loading file :', file_cnt)
                #print(file)
                # 定义文件路径
                doc_path = os.path.join(root, file)
                # 使用win32com.client打开文件
                #print(doc_path)

                if check_file_error(doc_path):
                    print('FileError dir=',doc_path)
                    continue

                doc = word.Documents.Open(doc_path)
                # 获取文件名，并替换扩展名
                txt_path = os.path.splitext(doc_path)[0] + ".txt"
                # 保存为txt文件
                doc.SaveAs(txt_path, 2)
                doc.Close()
    word.Quit()

def extract_html_content(html_str):
    start_index = html_str.find("<TITLE></TITLE>") + len("<TITLE></TITLE>")
    end_index = html_str.find("</div></BODY></HTML></body></html>") + len("</div></BODY></HTML></body></html>")
    html_str = html_str[start_index:end_index]
    html_strs = html_str.split('</div><div')
    for i in range(len(html_strs)-1):
        html_strs[i] = html_strs[i] + '</div>'
        html_strs[i+1] = '<div' + html_strs[i+1]
    return html_strs

def html_to_text(html_strings):
    for i in range(len(html_strings)):
        html_strings[i] = BeautifulSoup(html_strings[i], 'html.parser').get_text()
    return html_strings

def doc_to_txt(folder_path):
    # 遍历文件夹下所有.doc文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".doc"):
                #print(file)
                # 定义文件路径
                doc_path = os.path.join(root, file)

                with open(doc_path, 'r', encoding='ansi', errors='ignore') as f:
                    doc = f.read()

                htmls = extract_html_content(doc)
                texts = html_to_text(htmls)

                # 获取文件名，并替换扩展名
                txt_path = os.path.splitext(doc_path)[0] + ".txt"
                # 保存为txt文件
                with open(txt_path, 'w', encoding='utf-8') as f:
                    text = '\n'.join(texts)
                    f.write(text)


def unzip_files(zip_file_path, destination_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)


def decode_file(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        return f.read()

def convert_encoding(file_path):
    content = decode_file(file_path)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def convert_directory(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for name in files:
            if name.endswith('.txt'):
                #print(name)
                file_path = os.path.join(root, name)
                convert_encoding(file_path)

def delete_doc_files(folder_path):
    doc_files = glob.glob(os.path.join(folder_path, "*.doc"))
    for file in doc_files:
        os.remove(file)



def delete_files_with_keyword(folder_path, keyword):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if keyword in file:
                os.remove(os.path.join(root, file))

def find_all_txt_files(path):
    txt_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(os.path.join(root, file))
    return txt_files

def solve_txt(txt_files):
    fail_sum = 0
    for txt_file in txt_files:
        a = Judgenemt(txt_file)
        out = a.outputJSON()

        if out == -1:
            fail_sum += 1
            continue

        with codecs.open("../files/entity_extraction.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(out, ensure_ascii=False))
            f.write("\n")

    print('Convert end:', len(txt_files)-fail_sum, '/', len(txt_files))



#all = find_all_txt_files("D:\\Code\\law\\pythonProject\\doc_temp")
#print(all)
#solve_txt(all)
#work("D:/Judgements/天津市红桥区人民法院/20211202230944211202HFW30HP46W.zip")
