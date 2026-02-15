import os 
import shutil

path = input("Enter the directory path: ")

files = os.listdir(path)

for i in files:
    file_name, file_ext = os.path.splitext(i)
    print(f"File Name: {file_name}, Extension: {file_ext}")
    file_ext1 = file_ext[1:]
    folder_path = path+"\\"+file_ext1
    if os.path.exists(folder_path):
        shutil.move(path+"\\"+i, folder_path)
    else:
        os.mkdir(folder_path)
        shutil.move(path+"\\"+i, folder_path) 
    