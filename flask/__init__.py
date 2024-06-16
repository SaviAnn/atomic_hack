def process_image():
    import cv2
    import numpy as np

    # Загрузить изображение
    image = cv2.imread('/uploads/18143970.jpg')

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
    cv2.imwrite('/uploads/18143970.jpg', cv2.cvtColor(image_rectangle, cv2.COLOR_RGB2BGR))

    # Вывести позицию самого красного пикселя
    print(max_loc)