# os: 1 thư viện của python
import os
from PIL import Image
import numpy as np
import cv2


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

# Hàm tính ngưỡng Otsu (không dùng skimage)
def otsu_threshold(image):
    pixel_counts, bin_edges = np.histogram(image, bins=256, range=(0, 256))
    total_pixels = image.size
    current_max, threshold = 0, 0
    sum_total, sum_background = 0, 0
    weight_background, weight_foreground = 0, 0

    for i in range(256):
        sum_total += i * pixel_counts[i]

    for i in range(256):
        weight_background += pixel_counts[i]
        if weight_background == 0:
            continue
        weight_foreground = total_pixels - weight_background
        if weight_foreground == 0:
            break
        sum_background += i * pixel_counts[i]
        mean_background = sum_background / weight_background
        mean_foreground = (sum_total - sum_background) / weight_foreground
        between_class_variance = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2

        if between_class_variance > current_max:
            current_max = between_class_variance
            threshold = i
    return threshold

# Hiển thị hình ảnh bằng thư viện OopenCV
def display(title, img):
    cv2.imshow(title, img)
    # Chờ một khoảng thời gian
    cv2.waitKey(0)
    # Đóng window
    cv2.destroyWindow(title)

# Detect Image
def detect(img):
    #Gọi file Face Cascade
    face_cascade = cv2.CascadeClassifier('./FaceCascade/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./FaceCascade/haarcascade_eye_tree_eyeglasses.xml')
    # Chuyển sang ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Nhận diện khuôn mặt
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    # Nhận diện mắt
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(5,5))
    # Vẽ hộp chứa khuôn mặt
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255,0), 2)
    # Vẽ hộp chứa khuôn mặt
    for (x, y, w, h) in eyes:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0,0), 2)
    # Trả về ảnh
    return img
    
