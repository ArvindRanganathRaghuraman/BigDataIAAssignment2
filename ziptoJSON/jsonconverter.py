import os
import json
import zipfile

ip_folder = 'ceac_financial_statements 2'
#op_folder = 'ceac_financial_statements 2/2009q1new_json'

#if not os.path.exists(op_folder):
 #   os.makedirs(op_folder)

for file_nm in os.listdir(ip_folder):
    if file_nm.endswith('.zip'):
        zip_path = os.path.join(ip_folder,file_nm)
        folder_name = os.path.splitext(file_nm)[0] + 'json'
        op_folder = os.path.join(ip_folder,folder_name)

        if not os.path.exists(op_folder):
            os.makedirs(op_folder)

    with zipfile.ZipFile(zip_path,'r') as zip_ref:
        for zip_info in zip_ref.infolist():
            if zip_info.filename.endswith('.txt'):
                with zip_ref.open(zip_info.filename) as file:
                    data = file.read().decode('utf-8')
                    json_filename = os.path.splitext(os.path.basename(zip_info.filename))[0] + '.json'


                    json_path = os.path.join(op_folder,os.path.splitext(zip_info.filename)[0] + '.json')

                    with open(json_path,'w',encoding = "utf-8") as json_file:
                        json.dump(data,json_file,indent =4)

                    print(f"Converted: {zip_info.filename} -> {json_path}")
print("all files converted")
