import pygame
from pygame.sprite import Sprite  # 导入Sprite类，用于创建精灵对象


class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self, ai_game):
        # ai_game 用于访问游戏中的所有资源，如主屏幕相关
        """初始化飞船并设置其初始位置"""
        super().__init__()  # 调用父类Sprite的构造函数，确保精灵功能正常初始化
        self.ship_speed = 15  # 设置飞船的移动速度（像素/帧）
        self.screen = ai_game.screen  # 获取主游戏屏幕的引用，用于绘制飞船
        self.settings = ai_game.settings  # 获取游戏设置对象的引用
        self.screen_rect = ai_game.screen.get_rect()  # 获取屏幕的矩形区域，用于边界检测

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')  # 从指定路径加载飞船图像
        self.rect = self.image.get_rect()  # 获取图像对应的矩形对象，用于定位和碰撞检测

        # 每艘新飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom  # 将飞船矩形底部中点对齐屏幕底部中点

        # 在飞船的属性x中存储一个浮点数
        self.x = float(self.rect.x)  # 将矩形x坐标转换为浮点数，便于进行更精确的位置计算

        # 移动标志(飞船一开始不动)
        self.moving_right = False  # 向右移动标志，初始为False（不移动）
        self.moving_left = False  # 向左移动标志，初始为False（不移动）

    def update(self):
        """根据移动标志调整飞船位置"""
        # 检查向右移动标志且确保飞船不会移出屏幕右边界
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ship_speed  # 增加x坐标值（向右移动）

        # 检查向左移动标志且确保飞船不会移出屏幕左边界
        if self.moving_left and self.rect.left > 0:
            self.x -= self.ship_speed  # 减少x坐标值（向左移动）

        # 这段代码有逻辑问题：它再次根据相同的标志移动rect.x
        # 但前面已经更新了self.x，这里会导致速度加倍
        # 应该是多余的代码，建议删除以下4行：
        if self.moving_right:
            self.rect.x += self.ship_speed
        if self.moving_left:
            self.rect.x -= self.ship_speed

        # 将更新后的浮点数x坐标赋值给rect.x，实现位置更新
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        # 将飞船图像绘制到屏幕的指定矩形位置
        self.screen.blit(self.image, self.rect)
        # screen.blit(source, dest, area=None, special_flags=0)
        # source (必需): 要绘制的图像（Surface 对象）
        # 可以是图像文件加载的结果
        # 也可以是创建的 Surface 对象
        # dest (必需): 绘制的位置
        # 可以是一个坐标元组 (x, y)
        # 也可以是一个 Rect 对象（矩形区域）
        # 如果提供 Rect，Pygame 会使用其 topleft（左上角）坐标
        # area (可选): 只绘制源图像的一部分
        # 指定源图像中的一个矩形区域
        # 格式：pygame.Rect(x, y, width, height)
        # special_flags (可选): 特殊的绘制效果
        # 如混合模式、透明度等
    def center_ship(self):
        """碰撞后重新将飞船置于屏幕底部的中央"""
        # 将飞船重新定位到屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 注意：这里应该同时更新self.x以保持数据一致
        # 建议添加：self.x = float(self.rect.x)