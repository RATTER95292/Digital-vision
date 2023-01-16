import cv2

image = cv2.imread("C:/Users/Ratter/Downloads/cc.jpg") # открыть изображение

'''
Сохранить изображение
cv2.imwrite("./экспорт/путь.расширение", image)
'''

#Посмотреть изображение
def viewImage(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL) # Название окна
    cv2.imshow(name_of_window, image) # Создать окно с изображением
    cv2.waitKey(0) # Ждем нажатие кнопки на клавиатуре
    cv2.destroyAllWindows() # Убираем это окно

viewImage(image,"Original image")

image_croped = image[10:500, 500:2000] # Обрезать изображение
viewImage(image_croped,"Croped image")

scale_percent = 40 # Процент от изначального размера
width = int(image.shape[1] * scale_percent / 100) # Расчитываем ширину
height = int(image.shape[0] * scale_percent / 100)# Расчитываем высоту
dim = (width, height)
image_size = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)#
viewImage(image_size, "resize image")

(h, w, d) = image.shape # узнает высоту и ширину изображению
center = (w // 2, h // 2) # Находим центер изображения
M = cv2.getRotationMatrix2D(center, 180, 1.0) # повернуть изображение на 190 градусов
rotated = cv2.warpAffine(image, M, (w, h))
viewImage(rotated, "Rotaded image")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, threshold_image = cv2.threshold(image, 127, 255, 0)
viewImage(gray_image, "m")
viewImage(threshold_image, "Black-white")

blurred = cv2.GaussianBlur(image, (51, 51), 0) # Делаем размытие по Гауссу
viewImage(blurred, "Blur imige")

output = image.copy()
x = ((w//2) - 50, (h//2) - 50)
y = ((w//2) + 50, (h//2) + 50)
cv2.rectangle(output, x, y, (0, 255, 255), 3) # Рисуем прямоугольник
viewImage(output, "Imige")

output = image.copy()
cv2.putText(output, "Shlepa", x,cv2.FONT_HERSHEY_SIMPLEX, 1, (30, 105, 210), 3) # Написать текст
viewImage(output, "Imige with text")
