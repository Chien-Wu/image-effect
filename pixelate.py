import imageio
import os
import cv2
from PIL import Image, ImageDraw
import numpy as np

INPUT_VIDEO = "input_video.mov"
OUTPUT_VIDEO = "output_video.mov"
BLOCK_SIZE = 10
MAX_CIRCLE_RADIUS = 5
COLOR_DARK = '#00008B'  # 深藍色
COLOR_LIGHT = '#FFC0CB'  # 粉紅色

print("檔案存在:", os.path.isfile(INPUT_VIDEO))

def process_frame(frame, block_size=10, max_circle_radius=5):
    # 將 BGR 轉為灰度
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

# 使用 imageio 讀取影片並逐幀處理
reader = imageio.get_reader(INPUT_VIDEO, 'ffmpeg')
writer = imageio.get_writer(OUTPUT_VIDEO, fps=8)

for frame in reader:
    processed_frame = process_frame(frame, BLOCK_SIZE, MAX_CIRCLE_RADIUS)
    writer.append_data(processed_frame)

writer.close()