from PIL import Image
import numpy as np
import os
from tqdm import tqdm

path = "/Users/aroslavsapoval/myProjects/data/images1000/"

if not os.path.exists(path):
    os.makedirs(path)

width = 1980
height = 1080

# Количество изображений, которые нужно создать
num_images = 1000

for i in tqdm(range(num_images), desc="Создание изображений"):
    # Создаем случайное изображение с использованием NumPy
    image_data = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    image = Image.fromarray(image_data)

    # Сохраняем изображение в формате PNG
    image.save(os.path.join(path, f"image_{i + 1}.png"))

print(f"Создано {num_images} изображений и сохранено по пути: {path}.")
