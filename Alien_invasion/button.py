import pygame.font  # 导入pygame的字体模块，用于文本渲染


class Button:
    """为游戏创建按钮的类"""

    def __init__(self, ai_game, msg):
        """初始化按钮的属性"""
        self.screen = ai_game.screen  # 获取游戏主屏幕Surface对象，用于后续绘制
        self.screen_rect = ai_game.screen.get_rect()  # 获取屏幕的矩形区域，用于居中定位

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50  # 定义按钮的宽度和高度（像素）
        self.button_color = (0, 135, 0)  # 设置按钮背景颜色：RGB格式的绿色（R=0,G=135,B=0）
        self.text_color = (255, 255, 255)  # 设置文本颜色：白色（R=255,G=255,B=255）
        self.font = pygame.font.SysFont(None, 48)  # 创建字体对象：None表示使用默认字体，48是字号大小

        # 创建按钮的rect对象，并使其居中
        # 先在(0,0)位置创建一个指定大小的矩形，这是pygame创建矩形的常见方式
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # 将按钮矩形中心点设置为屏幕中心点，实现按钮在屏幕居中
        self.rect.center = self.screen_rect.center

        # 按钮只需要创建一次（渲染文本图像）
        # 调用私有方法_prep_msg来渲染文本图像，msg是按钮上显示的文字
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上方居中"""
        # 使用字体对象渲染文本，生成一个Surface图像
        # 参数说明：
        # msg: 要渲染的文本字符串
        # True: 启用抗锯齿，使文字边缘更平滑
        # self.text_color: 文本颜色
        # self.button_color: 背景颜色（可选，这里传入按钮颜色作为文字背景）
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        # font.render() 方法详解：
        # 语法：render(text, antialias, color, background=None)
        # 参数：
        # - text: 要渲染的字符串
        # - antialias: 布尔值，是否启用抗锯齿（True=平滑，False=锯齿）
        # - color: 文字颜色（RGB元组）
        # - background: 可选参数，背景颜色（如果不提供，背景透明）

        # 获取文本图像的矩形对象，用于定位
        self.msg_image_rect = self.msg_image.get_rect()

        # 将文本图像的中心点设置为屏幕中心点
        # 由于按钮也在屏幕中心，所以文本会显示在按钮中央
        self.msg_image_rect.center = self.screen_rect.center

    def draw_button(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        # 第一步：在按钮矩形区域内填充按钮颜色
        # screen.fill()的第二个参数可以指定填充区域
        # 这会绘制一个实心矩形作为按钮背景
        self.screen.fill(self.button_color, self.rect)

        # 第二步：在按钮上方绘制文本图像
        # 将渲染好的文本图像绘制到屏幕上，位置由msg_image_rect决定
        self.screen.blit(self.msg_image, self.msg_image_rect)