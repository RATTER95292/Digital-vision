import numpy as np
import cv2
import time

def imshow(name_of_window, image):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL) # Название окна
    cv2.imshow(name_of_window, image) # Создать окно с изображением
    cv2.waitKey(0) # Ждем нажатие кнопки на клавиатуре
    cv2.destroyAllWindows() # Убираем это окно

# Распознавание
def rec(img):

    ret = ""
    h, w, _ = img.shape # Размеры изображения
    img = img[0+20:h-20,0+50:w-50] # Обрезка изображения

    # Копирование изображения
    deb = img.copy()

    # Фильтрация
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2XYZ)
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    d = np.clip(11*(hsv[:, :, 1].astype("float")*hsv[:, :, 2].astype("float") / (255*255))**1.6, 0, 1)#0.25
    d2 = d > 0.9

    d2 = (d2*255).astype("uint8")
    d3 = d2.copy()
    d3 = cv2.dilate(d3, np.ones((6, 6), dtype="uint8"))
    dout = d2


    cnts = cv2.findContours(dout, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) == 0:
        return "", deb


    # Рисование контуров
    cnts = sorted([cnt for cnt in cnts if cv2.contourArea(cnt) > 2700], key=cv2.contourArea, reverse=True)
    cv2.drawContours(deb, cnts, -1, (255,0,0), 3)
    if len(cnts) == 0:
        return "", deb

    cnt = cnts[0]

    points = cv2.contourArea(cnt)
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.array(box, dtype="int")


    for i, b in enumerate(box):
        cv2.circle(deb, (b[0], b[1]), 10, (0, 255.0*(i)/4.0, 0), -1)




    imshow("deb", deb)
    return ret, deb

image = cv2.imread("C:/Users/Ratter/Downloads/Telegram Desktop/photo_2023-01-24_10-44-07.jpg")
imshow("Original image",image)
rec(image)
