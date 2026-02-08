import pygame
from pygame.sprite import Sprite  # 导入Sprite类，用于创建精灵对象


class Bullet(Sprite):
    """管理飞船所发射子弹的类"""

    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()  # 调用父类Sprite的构造函数，确保精灵功能正常初始化
        self.screen = ai_game.screen  # 获取游戏主屏幕的引用，用于后续可能的绘制或边界检测
        self.settings = ai_game.settings  # 获取游戏设置对象，包含子弹的颜色、速度、尺寸等参数
        self.color = self.settings.bullet_color  # 从设置中获取子弹的颜色值，通常是一个RGB元组

        # 在(0,0)处创建一个表示子弹的矩形，再设置其正确位置
        # 使用pygame.Rect创建矩形，而不是从图像加载
        # 参数格式：Rect(left, top, width, height)
        self.rect = pygame.Rect(0, 0,  # 初始位置为(0,0)，后续会调整，先创建后定位的思想
                                self.settings.bullet_width,  # 子弹的宽度（从设置中获取）
                                self.settings.bullet_height)  # 子弹的高度（从设置中获取）
        # 第一步：创建矩形对象（必须在某个位置创建）
        # pygame.Rect 需要初始位置，但我们还不知道最终位置
        # (0,0) 是最简单、最常用的临时位置
        # 创建矩形对象和定位矩形对象是两个独立的步骤
        # 避免手动计算位置坐标

        # 将子弹矩形顶部中点与飞船矩形顶部中点对齐
        # 这样子弹会从飞船的顶部中心位置发射
        self.rect.midtop = ai_game.ship.rect.midtop

        # 存储用浮点数表示的子弹位置
        # 使用浮点数确保子弹移动平滑，特别是当速度为小数时
        self.y = float(self.rect.y)  # 将矩形的y坐标转换为浮点数

    def update(self):
        """向上移动子弹（负y方向）"""
        # 更新子弹的准确位置（使用浮点数计算）
        # 减去bullet_speed是因为在pygame坐标系中，y轴向下为正
        # 所以减少y值会使子弹向上移动
        self.y -= self.settings.bullet_speed

        # 更新表示子弹的rect位置
        # 将计算得到的浮点数y坐标赋值给矩形对象的y属性
        # pygame.Rect会自动将浮点数转换为整数进行绘制
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        # 使用pygame.draw.rect绘制子弹矩形
        pygame.draw.rect(self.screen,
                         self.color, # 子弹颜色
                         self.rect# 子弹矩形
                         )