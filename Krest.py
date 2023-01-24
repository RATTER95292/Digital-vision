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
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    d = np.clip(11*(hsv[:, :, 1].astype("float")*hsv[:, :, 2].astype("float") / (255*255))**1.6, 0, 1)
    d2 = d > 0.25
    d2 = (d2*255).astype("uint8")
    d3 = d2.copy()
    d3 = cv2.dilate(d3, np.ones((6, 6), dtype="uint8"))

    imshow("hsv", hsv)
    imshow("d", (d*255).astype("uint8"))
    imshow("d2", d2)
    imshow("d3", d3)

    dout = d3

    cnts = cv2.findContours(dout, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) == 0:
        return "", deb


    # Рисование контуров
    cnts = sorted([cnt for cnt in cnts if cv2.contourArea(cnt) > 2700], key=cv2.contourArea, reverse=True)
    cv2.drawContours(deb, cnts, -1, (0,255,0), 3)
    if len(cnts) == 0:
        return "", deb

    cnt = cnts[0]

    print(cv2.contourArea(cnt))
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.array(box, dtype="int")


    cv2.drawContours(deb, [cnt], -1, (0,0,255), 3)
    cv2.drawContours(deb,[box],0,(255,0,0),2)


    for i, b in enumerate(box):
        cv2.circle(deb, (b[0], b[1]), 10, (0, 255.0*(i)/4.0, 0), -1)

    # обрезка

    pts2 = np.float32([[0, 50], [0, 0], [50, 0], [50, 50]])
    print(box)
    pts1 = np.float32(box)
    M = cv2.getPerspectiveTransform(pts1, pts2)
    croped = cv2.warpPerspective(img, M, (50, 50))
    imshow("croped", croped)

    # класификация
    croped_hsv = cv2.cvtColor(croped, cv2.COLOR_BGR2HSV)
    chsv_d = croped_hsv.astype("float")/255.0
    cd = (chsv_d[:, :, 1] > 0.2)*(chsv_d[:, :, 2] > 0.2)

    red_t = ((chsv_d[:, :, 0] > 0.5)*(chsv_d[:, :, 0] < 1))*cd
    rr = (red_t < 0.5)*chsv_d[:, :, 0]*cd
    imshow("cd", (cd*255*chsv_d[:, :, 0]).astype("uint8"))
    imshow("rr", (rr*255).astype("uint8"))
    red = np.count_nonzero(red_t) > 100
    green = np.count_nonzero((rr > 0.36)*(rr< 0.4)) > 100
    blue = np.count_nonzero((rr > 0.405)*(rr< 0.5)) > 100
    yellow = np.count_nonzero((rr < 0.58)*(rr > 0.4)) > 100
    print(red, green, blue)


    imshow("deb", deb)
    print(ret)
    return ret, deb

image = cv2.imread("C:/Users/Ratter/Downloads/Telegram Desktop/photo_2023-01-24_10-44-07.jpg")
imshow("Original image",image)
rec(image)
