import pygame.font  # 导入pygame的字体模块，用于渲染文本得分
from pygame.sprite import Group  # 导入精灵组，用于管理飞船生命图标
from ship import Ship  # 导入Ship类，用于创建代表剩余生命的飞船图标


class Scoreboard:
    """一个用来显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化显示得分所涉及的属性"""
        self.ai_game = ai_game  # 存储游戏主对象的引用，用于访问游戏所有组件
        self.screen = ai_game.screen  # 获取游戏主屏幕Surface对象
        self.screen_rect = self.screen.get_rect()  # 获取屏幕的矩形区域，用于界面布局
        self.settings = ai_game.settings  # 获取游戏设置对象，包含背景色等参数
        self.stats = ai_game.stats  # 获取游戏统计对象，包含得分、等级、剩余生命等信息

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)  # 设置文本颜色：深灰色（R=30,G=30,B=30）
        self.font = pygame.font.SysFont(None, 48)  # 创建字体对象：默认字体，48号大小

        # 准备初始得分的图像（调用各个准备方法）
        self.prep_score()  # 准备当前得分的渲染图像
        self.prep_high_score()  # 准备最高得分的渲染图像
        self.prep_level()  # 准备当前等级的渲染图像
        self.prep_ships()  # 准备剩余飞船生命图标的精灵组

    def prep_ships(self):
        """显示还余下多少艘飞船（通过飞船图标表示剩余生命）"""
        self.ships = Group()  # 创建一个精灵组，用于管理所有剩余飞船图标

        # 循环创建飞船图标，数量等于剩余生命数
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)  # 创建一个新的飞船实例（作为图标）
            ship.rect.x = 10 + ship_number * ship.rect.width  # 水平排列：第一个在x=10，后续每个间隔一个飞船宽度
            ship.rect.y = 10  # 垂直位置：距离屏幕顶部10像素
            self.ships.add(ship)  # 将飞船图标添加到精灵组

    def prep_score(self):
        """将当前得分渲染为图像"""
        # 将得分四舍五入到最近的10的倍数（例如：1234 → 1230）
        # 第二个参数-1表示舍入到十位数
        rounded_score = round(self.stats.score, -1)

        # 格式化得分，添加千位分隔符（例如：1230 → "1,230"）
        score_str = f"{rounded_score:,}"

        # 使用字体渲染得分文本为图像
        # 参数：文本内容，是否抗锯齿，文本颜色，背景颜色（使用游戏背景色）
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # 在屏幕的右上角显示得分
        self.score_rect = self.score_image.get_rect()  # 获取得分图像的矩形区域
        self.score_rect.right = self.screen_rect.right - 20  # 右对齐，距离右边20像素
        self.score_rect.top = 20  # 距离顶部20像素

    def show_score(self):
        """在屏幕上显示得分、最高分、等级以及剩余飞船图标"""
        self.screen.blit(self.score_image, self.score_rect)  # 绘制当前得分
        self.screen.blit(self.high_score_image, self.high_score_rect)  # 绘制最高得分
        self.screen.blit(self.level_image, self.level_rect)  # 绘制等级
        self.ships.draw(self.screen)  # 绘制所有剩余飞船图标（Group的draw方法）

    def prep_high_score(self):
        """将最高分渲染为图像"""
        # 将最高分四舍五入到最近的10的倍数
        high_score = round(self.stats.high_score, -1)

        # 格式化最高分，添加千位分隔符
        high_score_str = f"{high_score:,}"

        # 渲染最高分文本为图像
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)

        # 将最高分设置在屏幕顶部的中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx  # 水平居中
        self.high_score_rect.top = self.score_rect.top  # 垂直位置与当前得分对齐（顶部高度相同）

    def check_high_score(self):
        """检查是否诞生了新的最高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score  # 更新最高分记录
            self.prep_high_score()  # 重新渲染最高分图像
            # 注意：这里有两个相同的调用，可能是代码错误，应该只有一个

    def prep_level(self):
        """将当前等级渲染为图像"""
        level_str = str(self.stats.level)  # 将等级数字转换为字符串
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)  # 渲染等级文本

        # 将等级放在得分的下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right  # 与得分右对齐
        self.level_rect.top = self.score_rect.bottom + 10  # 在得分下方10像素处
