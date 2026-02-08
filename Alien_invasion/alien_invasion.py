import sys  # 导入系统模块，用于退出程序
from time import sleep  # 导入时间模块，用于暂停游戏（飞船被撞后的反应时间）
import pygame  # 导入pygame主模块，游戏开发的核心库
from settings import Settings  # 导入游戏设置类
from game_stats import GameStats  # 导入游戏统计类
from ship import Ship  # 导入飞船类
from bullet import Bullet  # 导入子弹类
from alien import Alien  # 导入外星人类
from button import Button  # 导入按钮类
from scoreboard import Scoreboard  # 导入记分板类


class AlienInvasion:
    """管理游戏资源和行为的类（主游戏类）"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()  # 初始化pygame所有模块
        self.clock = pygame.time.Clock()  # 创建时钟对象，用于控制帧率
        self.settings = Settings()  # 创建游戏设置实例

        # 创建游戏窗口（屏幕）
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)  # 设置窗口大小
        )
        pygame.display.set_caption("Alien Invasion")  # 设置窗口标题

        # 创建一个用于存储游戏统计信息的实例，并创建一个得分牌
        self.stats = GameStats(self)  # 游戏统计对象，跟踪得分、生命、等级等
        self.sb = Scoreboard(self)  # 记分板对象，负责显示游戏状态信息

        # 创建游戏对象
        self.ship = Ship(self)  # 创建玩家飞船实例
        self.bullets = pygame.sprite.Group()  # 创建子弹精灵组，用于管理所有子弹
        self.aliens = pygame.sprite.Group()  # 创建外星人精灵组，用于管理所有外星人

        self._create_fleet()  # 创建外星人群（舰队）

        # 游戏启动后处于非活动状态（等待玩家点击Play按钮）
        self.game_active = False
        # 创建Play按钮
        self.play_button = Button(self, "Play")  # 创建开始游戏按钮

    def run_game(self):
        """开始游戏的主循环（游戏引擎的核心）"""
        while True:  # 游戏主循环，无限循环直到玩家退出
            self._check_events()  # 检查并处理用户输入事件

            if self.game_active:  # 只有在游戏活动时才更新游戏状态
                self.ship.update()  # 更新飞船位置（根据按键状态）
                self._update_bullets()  # 更新子弹位置并处理碰撞
                self._update_aliens()  # 更新外星人位置并检查碰撞
                self.bullets.update()  # 更新所有子弹的位置

            self._update_screen()  # 绘制新一帧的画面
            self.clock.tick(60)  # 控制帧率为60帧/秒

    def _check_events(self):
        """监听键盘和鼠标事件"""
        for event in pygame.event.get():  # 遍历所有待处理的事件
            if event.type == pygame.QUIT:  # 如果点击窗口关闭按钮
                sys.exit()  # 退出游戏
            elif event.type == pygame.KEYDOWN:  # 如果按下键盘按键
                self._check_keydown_events(event)  # 处理按键按下事件
            elif event.type == pygame.KEYUP:  # 如果释放键盘按键
                self._check_keyup_events(event)  # 处理按键释放事件
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 如果按下鼠标按钮
                mouse_pos = pygame.mouse.get_pos()  # 获取鼠标当前位置
                self._check_play_button(mouse_pos)  # 检查是否点击了Play按钮

    def _check_play_button(self, mouse_pos):
        """单击Play以开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)  # 检查鼠标是否在按钮区域内
        if button_clicked and not self.game_active:  # 如果点击了按钮且游戏不处于活动状态
            # 还原游戏设置（重置速度等动态设置）
            self.settings.initialize_dynamic_settings()
            # 重置游戏的统计信息
            self.stats.reset_stats()  # 重置得分、生命、等级
            self.sb.prep_score()  # 重新渲染得分图像
            self.sb.prep_level()  # 重新渲染等级图像
            self.sb.prep_ships()  # 重新渲染剩余飞船图标
            self.game_active = True  # 将游戏状态设置为活动

            # 清空外星人列表和子弹列表
            self.bullets.empty()  # 清空所有子弹
            self.aliens.empty()  # 清空所有外星人

            # 创建一个新的外星舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()  # 创建新的一群外星人
            self.ship.center_ship()  # 将飞船重置到初始位置
            # 隐藏光标（让玩家专注于游戏）
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按下按钮"""
        if event.key == pygame.K_LEFT:  # 如果按下左箭头键
            self.ship.moving_left = True  # 设置飞船左移标志为True
        elif event.key == pygame.K_RIGHT:  # 如果按下右箭头键
            self.ship.moving_right = True  # 设置飞船右移标志为True
        elif event.key == pygame.K_ESCAPE:  # 如果按下ESC键
            sys.exit()  # 退出游戏
        elif event.key == pygame.K_SPACE:  # 如果按下空格键
            self._fire_bullet()  # 发射子弹

    def _check_keyup_events(self, event):
        """响应释放按钮"""
        if event.key == pygame.K_LEFT:  # 如果释放左箭头键
            self.ship.moving_left = False  # 设置飞船左移标志为False
        elif event.key == pygame.K_RIGHT:  # 如果释放右箭头键
            self.ship.moving_right = False  # 设置飞船右移标志为False

    def _fire_bullet(self):
        """创建一个子弹，并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:  # 检查子弹数量是否超过限制
            new_bullet = Bullet(self)  # 创建新的子弹实例
            self.bullets.add(new_bullet)  # 将子弹添加到子弹组中

    def _create_fleet(self):
        """创建一个外星舰队"""
        # 创建一个外星人，再不断添加，直到没有外星人可以添加为止
        # 外星人的间距为外星人的宽度和高度
        alien = Alien(self)  # 创建一个外星人实例（仅用于获取尺寸）
        alien_width, alien_height = alien.rect.size  # 获取外星人的宽度和高度

        current_x, current_y = alien_width, alien_height  # 初始化起始位置（留出边距）
        while current_y < (self.settings.screen_height - 3 * alien_height):  # 垂直方向循环
            while current_x < (self.settings.screen_width - 2 * alien_width):  # 水平方向循环
                self._create_alien(current_x, current_y)  # 在当前位置创建外星人
                current_x += 2 * alien_width  # 水平移动到下一个位置（间隔一个外星人宽度）

            # 添加一行外星人后，重置x的值并递增y值（换行）
            current_x = alien_width  # 重置x坐标到起始位置
            current_y += 2 * alien_height  # 向下移动到下一行（间隔一个外星人高度）

    def _create_alien(self, x_position, y_position):
        """创建一个外星人并将其放在当前行中"""
        new_alien = Alien(self)  # 创建新的外星人实例
        new_alien.x = x_position  # 设置外星人的浮点数x坐标
        new_alien.rect.x = x_position  # 设置外星人矩形的x坐标
        new_alien.rect.y = y_position  # 设置外星人矩形的y坐标
        self.aliens.add(new_alien)  # 将外星人添加到外星人组中

    def _update_aliens(self):
        """更新外星舰队中所有外星人的位置"""
        self._check_fleet_edges()  # 检查外星人群是否到达屏幕边缘
        self.aliens.update()  # 更新所有外星人的位置（调用每个外星人的update方法）

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):  # 如果飞船与任何外星人碰撞
            self._ship_hit()  # 处理飞船被撞事件

    def _update_bullets(self):
        """更新子弹的位置并删除已经消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()  # 更新所有子弹的位置（调用每个子弹的update方法）
        # 删除已经消失的子弹（超出屏幕顶部）
        for bullet in self.bullets.copy():  # 遍历子弹副本（避免在迭代时修改原列表）
            if bullet.rect.bottom < 0:  # 如果子弹底部超出屏幕顶部（完全消失）
                self.bullets.remove(bullet)  # 从子弹组中移除该子弹

        self._check_bullet_alien_collisions()  # 检查子弹和外星人的碰撞

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        # 删除发生碰撞的子弹和外星人

        if not self.aliens:  # 如果所有外星人都被消灭
            # 删除现有的子弹并创建一个新的外星舰队
            self.bullets.empty()  # 清空所有子弹
            self._create_fleet()  # 创建新的外星人群
            self.settings.increase_speed()  # 提高游戏速度（增加挑战性）

            # 提高等级
            self.stats.level += 1  # 等级加1
            self.sb.prep_level()  # 更新等级显示

        # 检查是否有子弹击中外星人
        # 如果有，则删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True  # 参数：子弹组，外星人组，是否删除子弹，是否删除外星人
        )
        if collisions:  # 如果有碰撞发生
            for aliens in collisions.values():  # 遍历所有被击中的外星人组
                self.stats.score += self.settings.alien_points * len(aliens)  # 增加得分（每个外星人得分为alien_points）
            self.sb.prep_score()  # 更新得分显示
            self.sb.check_high_score()  # 检查并更新最高分

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新的屏幕"""
        self.screen.fill(self.settings.bg_color)  # 用背景色填充整个屏幕
        for bullet in self.bullets.sprites():  # 遍历所有子弹
            bullet.draw_bullet()  # 绘制每个子弹
        self.ship.blitme()  # 绘制飞船
        self.aliens.draw(self.screen)  # 绘制所有外星人（Group的draw方法）

        # 显示得分
        self.sb.show_score()  # 显示记分板上的所有信息

        # 如果游戏处于非活动状态那么就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()  # 绘制Play按钮

        # 让最近绘制的屏幕可见（刷新显示）
        pygame.display.flip()  # 更新整个显示界面
        self.clock.tick(60)  # 控制帧率为60帧/秒

    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():  # 遍历所有外星人
            if alien.check_edges():  # 如果该外星人到达屏幕边缘
                self._change_fleet_direction()  # 改变舰队移动方向
                break  # 只需要检测到一个外星人到达边缘就足够

    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变它们的方向"""
        for alien in self.aliens.sprites():  # 遍历所有外星人
            alien.rect.y += self.settings.fleet_drop_speed  # 所有外星人向下移动一定距离
        self.settings.fleet_direction *= -1  # 改变水平移动方向（1变-1，-1变1）

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:  # 如果还有剩余生命
            # 将ships_left减一并且更新记分牌
            self.stats.ships_left -= 1  # 剩余生命减1
            self.sb.prep_ships()  # 更新剩余飞船显示

            # 清空此时外星人和子弹的列表
            self.bullets.empty()  # 清空所有子弹
            self.aliens.empty()  # 清空所有外星人

            # 创建一个新的外星舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()  # 创建新的外星人群
            self.ship.center_ship()  # 重置飞船位置

            # 将时间暂停五秒钟给人反应
            sleep(0.5)  # 暂停0.5秒，让玩家有时间反应

        else:  # 如果没有剩余生命
            self.game_active = False  # 游戏结束
            pygame.mouse.set_visible(True)  # 显示鼠标光标（以便点击Play重新开始）

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕下方"""
        for alien in self.aliens.sprites():  # 遍历所有外星人
            if alien.rect.bottom >= self.settings.screen_height:  # 如果外星人底部到达或超过屏幕底部
                # 就像飞船被撞到一样处理
                self._ship_hit()  # 处理飞船被撞事件
                break  # 只需要检测到一个外星人到达底部就足够


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()  # 创建游戏主类的实例
    ai.run_game()  # 启动游戏主循环