import cv2

image = cv2.imread("C:/Users/Ratter/Downloads/cc.jpg") # открыть изображение

#посмотреть изображение
def viewImage(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

viewImage(image,"ШЛЕА")

image1 = image[10:500, 500:2000]
viewImage(image1,"ШЛЕА")

scale_percent = 20 # Процент от изначального размера
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
viewImage(image, "После изменения размера на 20 %")

(h, w, d) = image.shape
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 180, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))
viewImage(rotated, "Пёсик после поворота на 180 градусов")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, threshold_image = cv2.threshold(image, 127, 255, 0)
viewImage(gray_image, "Пёсик в градациях серого")
viewImage(threshold_image, "Чёрно-белый пёсик")

blurred = cv2.GaussianBlur(image, (51, 51), 0)
viewImage(blurred, "Размытый пёсик")

output = image.copy()
cv2.rectangle(output, (100, 100), (100, 400), (0, 255, 255), 10)
viewImage(output, "Обводим прямоугольником лицо пёсика")

output = image.copy()
cv2.putText(output, "We <3 Dogs", (100, 100),cv2.FONT_HERSHEY_SIMPLEX, 15, (30, 105, 210), 40)
viewImage(output, "Изображение с текстом")

cv2.imwrite("./экспорт/путь.расширение", image)
