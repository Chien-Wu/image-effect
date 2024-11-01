import imageio
import os
import cv2
from PIL import Image, ImageDraw
import numpy as np

INPUT_DIR = "input"
OUTPUT_DIR = "output"
BLOCK_SIZE = 10
MAX_CIRCLE_RADIUS = 5
COLOR_DARK = '#00008B'  # 深藍色
COLOR_LIGHT = '#FFC0CB'  # 粉紅色

# 確保輸出資料夾存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_frame(frame, block_size=10, max_circle_radius=5):
    # 將 RGB 轉為 BGR，再轉為灰度
    frame_bgr = frame[:, :, ::-1]
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape

    new_img = Image.new("RGB", (width, height), COLOR_LIGHT)
    draw = ImageDraw.Draw(new_img)
    img_array = np.array(gray)

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block = img_array[y:y+block_size, x:x+block_size]
            brightness = np.mean(block)
            radius = max_circle_radius * (1 - brightness / 255)
            center = (x + block_size // 2, y + block_size // 2)
            draw.ellipse(
                (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
                fill=COLOR_DARK
            )

    return cv2.cvtColor(np.array(new_img), cv2.COLOR_RGB2BGR)

# 處理 input 資料夾中的每個影片
for filename in os.listdir(INPUT_DIR):
    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, filename)

    # 確認檔案是影片格式（例如 .mov）
    if filename.lower().endswith(('.mov', '.mp4', '.avi')):
        print(f"處理影片：{filename}")
        reader = imageio.get_reader(input_path, 'ffmpeg')
        writer = imageio.get_writer(output_path, fps=8)

        for frame in reader:
            processed_frame = process_frame(frame, BLOCK_SIZE, MAX_CIRCLE_RADIUS)
            writer.append_data(processed_frame)

        writer.close()
        print(f"儲存處理後影片到：{output_path}")