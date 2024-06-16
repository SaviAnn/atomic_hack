import time

ready_flag=0
def process_image(paths_img):
    import cv2
    import numpy as np
    defect_type=[]
    if type(paths_img)!=type(['123']):
        paths_img=[paths_img]
    for path in paths_img:

        # Загрузить изображение
        image = cv2.imread(path)

        # Преобразовать изображение в RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Найти самый красный пиксель
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(image_rgb[:,:,0])

        # Нарисовать прямоугольник вокруг самого красного пикселя
        start_point = (max_loc[0] - 10, max_loc[1] - 10)
        end_point = (max_loc[0] + 10, max_loc[1] + 10)
        color = (255, 0, 0) # RGB
        thickness = 2
        image_rectangle = cv2.rectangle(image_rgb, start_point, end_point, color, thickness)

        # Сохранить изображение
        cv2.imwrite(path, cv2.cvtColor(image_rectangle, cv2.COLOR_RGB2BGR))

        # Вывести позицию самого красного пикселя
        print(max_loc)
        # time.sleep(1)
        # defect_type.append(path[-6:-2])
    ready_flag=1

def print_(a):
    print(a)