from PIL import Image, ImageDraw
import numpy as np

def pixelate_and_draw(image_path, output_path, block_size=10, max_circle_radius=5):
    # 打開圖片並轉換為灰度模式
    img = Image.open(image_path).convert('L')
    width, height = img.size

    # 新建一個相同大小的彩色圖片作為背景
    new_img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(new_img)

    # 將圖片轉為 numpy 陣列
    img_array = np.array(img)

    # 將圖片分成 block_size x block_size 的區塊
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            # 計算區塊內的平均亮度
            block = img_array[y:y+block_size, x:x+block_size]
            brightness = np.mean(block)

            # 根據亮度計算圓圈的半徑
            radius = max_circle_radius * (1 - brightness / 255)

            # 計算圓圈的中心點
            center = (x + block_size // 2, y + block_size // 2)

            # 畫出實心圓圈
            draw.ellipse(
                (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
                fill="black"
            )

    new_img.save(output_path)

pixelate_and_draw("input_image.jpg", "output_image.jpg", block_size=10, max_circle_radius=5)