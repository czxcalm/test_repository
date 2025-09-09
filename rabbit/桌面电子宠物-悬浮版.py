import tkinter as tk
import ctypes
import os
import requests
from PIL import Image, ImageTk

# 图片文件映射（文件名 -> URL）
IMAGE_FILES = {
    "卡通兔子正常1.jpg": "https://s.coze.cn/t/KESQ4sw1y94/",
    "兔子正常状态2.jpg": "https://s.coze.cn/t/S1LQFJS2lvY/",
    "兔子正常状态3.jpg": "https://s.coze.cn/t/ynsuO1tDEiA/",
    "兔子正常状态4.jpg": "https://s.coze.cn/t/G_t3HTVlxLY/",
    "兔子正常5帧.jpg": "https://s.coze.cn/t/rb2IAiNfnlU/",
    "卡通兔子6帧.jpg": "https://s.coze.cn/t/xWCwlQNdYnY/",
    "兔子开心准备跳.jpg": "https://s.coze.cn/t/wavYgqThdF0/",
    "兔子开心跳跃2.jpg": "https://s.coze.cn/t/vO1GGUWx4_U/",
    "兔子开心跳第3帧.jpg": "https://s.coze.cn/t/SxibxBrf2-w/",
    "兔子开心下落4.jpg": "https://s.coze.cn/t/SQHZFxaA8sA/",
    "兔子开心第5帧.jpg": "https://s.coze.cn/t/NXw_3Taf49w/",
    "卡通兔子第6帧.jpg": "https://s.coze.cn/t/_E31ev-wX5Q/",
    "卡通兔子睡觉1.jpg": "https://s.coze.cn/t/-SsfU7C7N8M/",
    "兔子睡觉第2帧.jpg": "https://s.coze.cn/t/5yTxFiVetRQ/",
    "兔子睡觉3帧.jpg": "https://s.coze.cn/t/y7FKQIYbRSM/",
    "兔子睡觉4帧.jpg": "https://s.coze.cn/t/E-k40WqUp-M/",
    "兔子睡觉第5帧.jpg": "https://s.coze.cn/t/MUtdnc-r1pI/",
    "兔子睡觉第6帧.jpg": "https://s.coze.cn/t/qmOoHfZr-xc/"
}

# 下载图片到本地
def download_images():
    for filename, url in IMAGE_FILES.items():
        if not os.path.exists(filename):
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"下载成功: {filename}")
            except Exception as e:
                print(f"下载失败 {filename}: {e}")

# 定义状态和对应的图片文件
STATES = {
    "normal": ["卡通兔子正常1.jpg", "兔子正常状态2.jpg", "兔子正常状态3.jpg", "兔子正常状态4.jpg", "兔子正常5帧.jpg", "卡通兔子6帧.jpg"],
    "happy": ["兔子开心准备跳.jpg", "兔子开心跳跃2.jpg", "兔子开心跳第3帧.jpg", "兔子开心下落4.jpg", "兔子开心第5帧.jpg", "卡通兔子第6帧.jpg"],
    "sleep": ["卡通兔子睡觉1.jpg", "兔子睡觉第2帧.jpg", "兔子睡觉3帧.jpg", "兔子睡觉4帧.jpg", "兔子睡觉第5帧.jpg", "兔子睡觉第6帧.jpg"]
}

class DesktopPet:
    def __init__(self, root):
        self.root = root
        self.root.title("桌面电子宠物")
        
        # 窗口设置：无边框、透明背景、置顶
        self.root.overrideredirect(True)  # 无边框
        self.root.attributes("-topmost", True)  # 置顶
        self.root.attributes("-transparentcolor", "white")  # 白色透明
        
        # 加载图片
        download_images()
        self.images = self.load_images()
        self.current_state = "normal"
        self.current_frame = 0
        self.frame_delay = 200  # 动画间隔（毫秒）
        
        # 创建标签显示图片
        self.label = tk.Label(root, bg="white")
        self.label.pack()
        
        # 鼠标事件绑定（拖动窗口）
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)
        self.label.bind("<Button-3>", self.toggle_state)  # 右键切换状态
        
        # 初始位置（屏幕右下角）
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"100x100+{screen_width-150}+{screen_height-150}")
        
        # 启动动画
        self.update_frame()
        
        # 设置窗口穿透（点击穿透背景）
        self.set_click_through()
    
    def load_images(self):
        """加载所有状态的动画帧"""
        images = {}
        for state, filenames in STATES.items():
            frames = []
            for filename in filenames:
                if os.path.exists(filename):
                    img = Image.open(filename).resize((100, 100))
                    frames.append(ImageTk.PhotoImage(img))
            images[state] = frames
        return images
    
    def update_frame(self):
        """更新动画帧"""
        frames = self.images.get(self.current_state, [])
        if frames:
            self.label.config(image=frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(frames)
        self.root.after(self.frame_delay, self.update_frame)
    
    def start_drag(self, event):
        """开始拖动"""
        self.x = event.x
        self.y = event.y
    
    def drag(self, event):
        """拖动窗口"""
        x = self.root.winfo_pointerx() - self.x
        y = self.root.winfo_pointery() - self.y
        self.root.geometry(f"+{x}+{y}")
    
    def toggle_state(self, event):
        """切换状态（右键点击）"""
        states = list(STATES.keys())
        current_idx = states.index(self.current_state)
        self.current_state = states[(current_idx + 1) % len(states)]
        self.current_frame = 0  # 重置帧索引
    
    def set_click_through(self):
        """设置窗口点击穿透（仅Windows）"""
        try:
            hwnd = ctypes.windll.user32.FindWindowW(None, "桌面电子宠物")
            # 设置窗口属性：透明+穿透
            ctypes.windll.user32.SetWindowLongPtrW(hwnd, -20, 0x80000 | 0x20)
        except Exception as e:
            print(f"设置穿透失败: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopPet(root)
    root.mainloop()