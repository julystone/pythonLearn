# encoding: utf-8

from collections import defaultdict
from Utils import DataUtil
import os


def filter_files_with_cvm(folder_path):
    folder_file = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if 'CVM' in file and '~' not in file:
                abs_path = os.path.join(root, file)
                folder_file.append(abs_path)
    print(folder_file)
    return folder_file


def cvm_2_obj(cvm_path, obj_file, obj_sheet):
    CVM_file = filter_files_with_cvm(cvm_path)
    CVM_list = []
    for file in CVM_file:
        CVM_single = DataUtil.ReadExcel(file_name=file)
        CVM_list.append(CVM_single)

    OBJ = DataUtil.ReadExcel(file_name=obj_file, if_new_column='安全组')
    sheet_list = OBJ.sheet_list

    for sheet in sheet_list:
        print(sheet)
        default_dict = defaultdict(int)
        default_dict.clear()
        for obj in OBJ.read_data_obj(sheet):  # 每一行ins
            for CVM_single in CVM_list:
                for ins in CVM_single.read_data_obj():
                    if ins.ID == obj.ID:
                        default_dict[ins.ID] += 1
                        OBJ.w_data(obj.row, 8 + default_dict[ins.ID], CVM_single.sheet_name[:-4])
        print(len(default_dict), default_dict)

    for CVM_single in CVM_list:
        CVM_single.close()

    OBJ.save()
    OBJ.close()


if __name__ == '__main__':
    cvm_2_obj("./CVMfiles_pc", "./CVMfiles_pc/腾讯云账号1实例2024.xlsx", '腾讯云上海')
