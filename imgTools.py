# os: 1 thư viện của python
import os
from PIL import Image
import numpy as np


def load_image(image_path):
    try:
        # Trả về 1 đối tượng hình ảnh
        img = Image.open(image_path)
        return img
    except Exception as e:
        print("Lỗi khi đọc hình ảnh từ: ", image_path, " ", e)
        return None

def is_image_file(file_path):
    extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
    # chuyển sang viết thường và chuỗi có kết thúc bằng 1 trong các extention
    return file_path.lower().endswith(extensions)

def get_image_list(folder_path):
    image_list = []
    # Kiểm tra đường dẫn của folder có tồn tại và có phải là 1 folder không?
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Lấy ra hết các tên file có trong folder
        filenames = os.listdir(folder_path)
        for filename in filenames:
            # Lấy ra đường dẫn của file hình ảnh - folder nối với file name
            file_path = os.path.join(folder_path, filename)
            # Kiểm tra đó có phải là file và có thuộc 1 trong các extention
            if os.path.isfile(file_path) and is_image_file(file_path):
                # Trả về 1 đối tượng hình ảnh
                img = load_image(file_path)
                # Thêm đối tượng đó vào mảng
                image_list.append(img)
    # Trả về mảng hình ảnh
    return image_list