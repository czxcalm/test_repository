import pygame
import sys
import os
import time
import math
from PIL import Image

# 确保中文显示正常
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei"], 24)

# 表盘配置
WIDTH, HEIGHT = 400, 400
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 180
FPS = 30

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# 动画帧配置
ANIMATION_FRAMES = 5
FRAME_DELAY = 100  # 毫秒
ANIMATION_PATH = "."  # 当前目录

# 加载并处理猪猪侠动画帧
def load_animation_frames():
    frames = []
    # 修正帧文件名映射（根据实际文件列表）
    frame_mapping = {
        0: "1.png",    # 静止帧
        1: "2.png",      # 点头帧1
        2: "3.png",      # 点头帧2
        3: "4.png",      # 眨眼帧1
        4: "5.png"       # 眨眼帧2
    }
    
    for i in range(ANIMATION_FRAMES):
        filename = frame_mapping[i]
        # 检查文件是否存在
        if any(f.name == filename for f in os.scandir(ANIMATION_PATH)):
            try:
                # 打开图片并转换为透明背景
                img = Image.open(filename).convert("RGBA")
                img = img.resize((100, 100), Image.LANCZOS)
                # 转换为Pygame表面
                frame = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
                frames.append(frame)
            except Exception as e:
                print(f"加载帧{i+1}失败: {e}")
                frames.append(create_placeholder_frame(i+1))
        else:
            print(f"文件不存在: {filename}")
            frames.append(create_placeholder_frame(i+1))
    return frames

# 创建占位符帧
def create_placeholder_frame(frame_num):
    frame = pygame.Surface((100, 100), pygame.SRCALPHA)
    frame.fill((255, 255, 255, 0))  # 透明背景
    text = font.render(f"帧{frame_num}", True, (255, 0, 0))
    text_rect = text.get_rect(center=(50, 50))
    frame.blit(text, text_rect)
    return frame

# 绘制表盘和指针
def draw_clock(screen, current_time, animation_frames, frame_index):
    screen.fill(WHITE)
    
    # 绘制表盘外圈
    pygame.draw.circle(screen, GRAY, CENTER, RADIUS, 2)
    pygame.draw.circle(screen, WHITE, CENTER, RADIUS - 5)
    
    # 绘制刻度
    for i in range(12):
        angle = math.radians(i * 30)  # 每小时30度
        # 计算刻度位置
        x = CENTER[0] + (RADIUS - 20) * math.sin(angle)
        y = CENTER[1] - (RADIUS - 20) * math.cos(angle)
        pygame.draw.circle(screen, BLACK, (int(x), int(y)), 5)
    
    # 获取当前时间
    hours = current_time.tm_hour % 12
    minutes = current_time.tm_min
    seconds = current_time.tm_sec
    
    # 绘制时针
    hour_angle = math.radians(hours * 30 + minutes * 0.5)
    hour_x = CENTER[0] + (RADIUS - 80) * math.sin(hour_angle)
    hour_y = CENTER[1] - (RADIUS - 80) * math.cos(hour_angle)
    pygame.draw.line(screen, BLACK, CENTER, (int(hour_x), int(hour_y)), 6)
    
    # 绘制分针
    min_angle = math.radians(minutes * 6 + seconds * 0.1)
    min_x = CENTER[0] + (RADIUS - 50) * math.sin(min_angle)
    min_y = CENTER[1] - (RADIUS - 50) * math.cos(min_angle)
    pygame.draw.line(screen, BLACK, CENTER, (int(min_x), int(min_y)), 4)
    
    # 绘制秒针
    sec_angle = math.radians(seconds * 6)
    sec_x = CENTER[0] + (RADIUS - 30) * math.sin(sec_angle)
    sec_y = CENTER[1] - (RADIUS - 30) * math.cos(sec_angle)
    pygame.draw.line(screen, RED, CENTER, (int(sec_x), int(sec_y)), 2)
    
    # 绘制中心圆点
    pygame.draw.circle(screen, BLACK, CENTER, 8)
    
    # 绘制猪猪侠动画
    if animation_frames:
        pig_img = animation_frames[frame_index]
        # 放置在表盘中心下方
        pig_rect = pig_img.get_rect(center=(CENTER[0], CENTER[1] + 20))
        screen.blit(pig_img, pig_rect)

# 主函数
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("猪猪侠表盘动画")
    clock = pygame.time.Clock()
    
    # 加载动画帧
    animation_frames = load_animation_frames()
    frame_index = 0
    frame_timer = 0
    animation_state = 0  # 0:静止, 1:点头, 2:眨眼
    
    running = True
    while running:
        current_time = time.localtime()
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # 控制动画状态（每5秒切换一次动画）
        current_sec = current_time.tm_sec
        if current_sec % 5 == 0:
            animation_state = 1  # 点头动画
        elif current_sec % 2 == 0:
            animation_state = 2  # 眨眼动画
        else:
            animation_state = 0  # 静止
        
        # 更新帧索引
        frame_timer += clock.tick(FPS)
        if frame_timer >= FRAME_DELAY:
            if animation_state == 1:  # 点头（帧0→1→2→0）
                frame_index = (frame_index % 3)  # 0,1,2循环
            elif animation_state == 2:  # 眨眼（帧0→3→4→0）
                frame_index = 3 + (frame_index % 2)  # 3,4循环
            else:
                frame_index = 0  # 静止帧
            frame_timer = 0
        
        # 绘制表盘
        draw_clock(screen, current_time, animation_frames, frame_index)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()