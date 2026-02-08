import pygame
from pygame.sprite import Sprite  # 导入Sprite类，用于创建精灵对象


class Alien(Sprite):
    """创建表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置相应的起始位置"""
        super().__init__()  # 调用父类Sprite的构造函数，确保精灵功能正常初始化
        self.screen = ai_game.screen  # 获取游戏主屏幕的引用，用于绘制外星人和边界检测
        self.settings = ai_game.settings  # 获取游戏设置对象，包含外星人的速度、移动方向等参数

        # 加载外星人图像，获取其外接矩形
        self.image = pygame.image.load("images/alien.bmp")  # 从指定路径加载外星人图像文件
        self.rect = self.image.get_rect()  # 获取图像对应的矩形对象，用于定位、绘制和碰撞检测

        # 每个外星人初始位置都在屏幕左上角附近
        # 这样安排可以使外星人群整齐排列，不紧贴屏幕边缘
        self.rect.x = self.rect.width  # 设置x坐标为外星人图像自身的宽度
        self.rect.y = self.rect.height  # 设置y坐标为外星人图像自身的高度
        # 这样定位使得第一个外星人距离屏幕左上角有一个外星人的间隔
        # 后续创建的外星人会基于这个位置进行偏移排列

        # 存储外星人精准的水平位置（使用浮点数）
        # 因为速度可能是小数，使用浮点数确保移动平滑
        self.x = float(self.rect.x)  # 将矩形x坐标转换为浮点数，便于进行精确的位置计算
        # 转化为浮点数可以保证游戏对象可以平滑移动
        # 否则出现取整的情况

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()  # 获取屏幕的矩形区域，包含屏幕的边界信息
        # 检查外星人是否到达屏幕边缘：
        # 1. self.rect.right >= screen_rect.right: 外星人右边缘 >= 屏幕右边缘
        # 2. self.rect.left <= 0: 外星人左边缘 <= 屏幕左边缘
        # 任意条件满足即返回True，表示外星人碰到了屏幕边缘
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """向左或向右移动外星人"""
        # 计算外星人的新水平位置：
        # self.settings.alien_speed: 外星人的基础移动速度
        # self.settings.fleet_direction: 外星人群的移动方向(1表示右，-1表示左)
        # 两者相乘得到实际移动距离（带方向）
        self.x += self.settings.alien_speed * self.settings.fleet_direction

        # 将计算得到的浮点数位置同步到矩形对象的x坐标
        # 确保绘制位置与实际计算位置一致
        self.rect.x = self.x