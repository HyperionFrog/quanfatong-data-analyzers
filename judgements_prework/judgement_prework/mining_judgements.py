from judgements_prework import *
from entity_load import *
import fnmatch

#给出压缩包的路径，实现自动解压，并将里面所有民事判决书转为txt，并进行实体提取
def work(zip_source_file):
    folder_path = 'D:\\Code\\law\\pythonProject\\doc_temp'
    print('Unzipping document, path = ', folder_path)
    unzip_files(zip_source_file, folder_path)#解压全部文件
    delete_files_with_keyword(folder_path, '刑事') #删除所有刑事判决书
    print('Converting doc documents..')
    doc_to_txt(folder_path) #将所有doc转为txt
    print('Deleting doc documents..')
    delete_doc_files(folder_path) #将所有doc删除
    #print('Converting txt to utf-8')
    #convert_directory(folder_path) #转码为utf-8
    print('Solving txt files')
    txt_files = find_all_txt_files(folder_path)
    solve_txt(txt_files)
    print('Deleting txt"')
    shutil.rmtree(folder_path)

def find_zip_files(path):
    zip_files = []
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, '*.zip'):
            zip_files.append(os.path.join(root, file))
    return zip_files

def solve_all():
    zip_files = find_zip_files('D:\\Code\\law\\pythonProject\\files\\judgements')
    print(zip_files)

    for zip_file in zip_files:
        print('Solving :',zip_file)
        work(zip_file)

solve_all()
#doc_to_txt("D:\\Code\\law\\pythonProject\\doc_temp")