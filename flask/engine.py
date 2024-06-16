from ultralytics import YOLO
import matplotlib.pyplot as plt
from PIL import Image
def process_image(path):
    model_cus = YOLO('model_weights/best.pt')
    results = model_cus(path)  # Предположим, что model_cus возвращает список с результатами

    draw_boxes(path,results)

    # Функция для рисования bounding box'ов и текста классов на изображении
def draw_boxes(image_path, results):
    # Загрузка изображения
    image = Image.open(image_path)
    for result in results:
        # detection
        result.boxes.xyxy  # box with xyxy format, (N, 4)
        result.boxes.xywh  # box with xywh format, (N, 4)
        result.boxes.xyxyn  # box with xyxy format but normalized, (N, 4)
        result.boxes.xywhn  # box with xywh format but normalized, (N, 4)
        result.boxes.conf  # confidence score, (N, 1)
        result.boxes.cls  # cls, (N, 1)

    # Извлечение координат и классов bounding box'ов из результатов
    boxes = results[0].boxes.xywhn.cpu().detach().numpy()  # Конвертируем в NumPy массив
    classes = results[0].boxes.cls.cpu().detach().numpy()  # Конвертируем в NumPy массив
    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    ax = plt.gca()
    for box, cls in zip(boxes, classes):
        x, y, w, h = box
        x_min = (x - w / 2) * image.width
        y_min = (y - h / 2) * image.height
        width = w * image.width
        height = h * image.height

        # Рисуем bounding box
        rect = plt.Rectangle((x_min, y_min), width, height, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

        # Добавляем текст с классом
        ax.text(x_min, y_min - 5, f'Class {int(cls)}', bbox=dict(facecolor='red', alpha=0.5), fontsize=10,
                color='white')

    plt.axis('off')

    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)

    # Получение текущего объекта Figure и его Axes
    fig = plt.gcf()
    ax = plt.gca()
    defect_type=""
    # Удаление белых рамок
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    plt.savefig(image_path, bbox_inches=extent, dpi=300, format='png')
    print(  # box with xyxy format, (N, 4)
          result.boxes.cls)





    print(int(result.boxes.cls[0]))
    for i in result.boxes.cls:
        i_int=int(i)
        print(i_int)
        if i_int==0:
            defect_type+='прилегающие дефекты    '+str(i_int)
        if i_int==1:
            defect_type+='дефекты целостности    '+str(i_int)
        if i_int==2:
            defect_type+='дефекты геометрии      '+str(i_int)
        if i_int==3:
            defect_type+='дефекты постобработки   '+str(i_int)
        if i_int==4:
            defect_type+='дефекты невыполнения    '+str(i_int)
    print(defect_type)
    with open('defect_type.txt','w+')as file:
        file.write(defect_type)



