import sys
import pygame
import random


from time import sleep
from playsound3 import playsound

from src.settings import Settings
from src.ship import Ship
from src.bullet import Bullet
from src.alien import Alien
from src.alien2 import Alien2
from src.alien3 import Alien3
from src.alien3_bullet import Alien3Bullet
from src.heart import Heart
from src.rapid_bonus import RapidBonus
from src.shield_bonus import ShieldBonus
from src.game_stats import GameStats
from src.button import Button
from src.scoreboard import Scoreboard
from src.settings_menu import SettingsMenu
from src.sounds import Sounds
from src.saver import Saver
from src.explosion import Explosion
from src.shield_eff import ShieldEff
from src.fast_eff import FastEff


class AlienInvasion:
    """Класс для управления ресурасами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        self.sounds = Sounds(self)

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()

        pygame.display.set_caption("Alien Invasion")

        
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.scoreboard = Scoreboard(self)
        self.settings_menu = SettingsMenu(self)
        self.saver = Saver(self)
        self.heart = Heart(self)
        self.rapid = RapidBonus(self)
        self.shield_bonus = ShieldBonus(self)

        self.bullets = pygame.sprite.Group()
        self.aliens1 = pygame.sprite.Group()
        self.aliens2 = pygame.sprite.Group()
        self.aliens3 = pygame.sprite.Group()
        self.aliens3_bullets = pygame.sprite.Group()
        self.all_aliens = pygame.sprite.Group()
        self.rapid_list = pygame.sprite.Group()
        self.shield_list = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.shield_eff = pygame.sprite.Group()
        self.fast_eff = pygame.sprite.Group()

        self._create_fleet()
        self.game_status = 'none'
        self.menu_mode = 'main'

        self.play_button = Button(self, "NEW GAME", 
                                  self.settings.play_button_color,
                                  self.settings.play_button_xpos,
                                  self.settings.play_button_ypos,
                                  self.settings.basic_button_width,
                                  self.settings.basic_button_height)
        self.setting_button = Button(self, "SETTINGS", 
                                     self.settings.setting_button_color,
                                     self.settings.setting_button_xpos,
                                     self.settings.setting_button_ypos,
                                     self.settings.basic_button_width,
                                     self.settings.basic_button_height)
        self.continue_button = Button(self, "CONTINUE", 
                                     self.settings.continue_button_color,
                                     self.settings.continue_button_xpos,
                                     self.settings.continue_button_ypos,
                                     self.settings.basic_button_width + 60,
                                     self.settings.basic_button_height + 20)
        self.quit_button = Button(self, "QUIT", 
                                             self.settings.quit_button_color,
                                             self.settings.quit_button_xpos,
                                             self.settings.quit_button_ypos,
                                             self.settings.basic_button_width,
                                             self.settings.basic_button_height)


        self.rapid_bonus_active = False
        self.shield_bonus_active = False
        self.alien3_fire_time = 0


        self.pause_time = 0
        self.play_time = 0
        self.all_pause_time = 0

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            self._draw()
            if self.stats.game_active:
                self._update()

    def _check_events(self):
        """Обрабатывает нажатия клавишь и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_continue_button(mouse_pos)
                self._check_settings_button(mouse_pos)
                self._check_quit_button(mouse_pos)
                self._check_return_button(mouse_pos)
        self._press_space()

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if play_button_clicked and not self.stats.game_active and self.game_status != 'losing':
            #  Сброс игровых настроек
            self.settings.initialize_dinamic_settings()
            self.pause_time = 0
            self.play_time = 0
            self.all_pause_time = 0
            #  Сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_hearts()
            #  Очистка списков пришельцев и снарядов
            self._clear_game_objects()
            #  Создание нового флота и размещения корабля
            self._create_fleet()
            self.ship.center_ship()
            #  Указатель мыши скрывается
            pygame.mouse.set_visible(False)
            self.game_status = 'play'
            #  Звук кнопик Play
            self.sounds.button()

    def _check_continue_button(self, mouse_pos):
        """Возврат в главное меню"""
        continue_button_clicked = self.continue_button.rect.collidepoint(mouse_pos)
        if continue_button_clicked and self.menu_mode == 'main' and self.game_status != 'losing':
            self.game_status = 'play'
            self.play_time = pygame.time.get_ticks()
            self.all_pause_time += self.play_time - self.pause_time
            self.sounds.button()
            self.stats.game_active = True
            pygame.mouse.set_visible(False)

    def _check_quit_button(self, mouse_pos):
        """Закрыть игру"""
        quit_button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if quit_button_clicked and self.menu_mode == 'main' and self.game_status != 'losing':
            self.sounds.button()
            sys.exit()

    def _check_settings_button(self, mouse_pos):
        """Заходит в меню настроек"""
        settings_button_clicked = self.setting_button.rect.collidepoint(mouse_pos)
        if settings_button_clicked and not self.stats.game_active and self.game_status != 'losing':
            self.menu_mode = 'settings'
            #self.aliens1.empty()
            #self.bullets.empty()
            self.sounds.button()

    def _check_return_button(self, mouse_pos):
        """Возврат в главное меню"""
        back_button_clicked = self.settings_menu.back_button.rect.collidepoint(mouse_pos)
        if back_button_clicked:
            if self.menu_mode == 'settings':
                self.menu_mode = 'main'
                self.sounds.button()
            elif self.game_status == 'losing':
                self.game_status = 'none'
                self.sounds.button()

    def _check_keydown_events(self, event):
                """Реагирует на нажатие клавиш"""             
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True              

                if event.key == pygame.K_ESCAPE:
                    if not self.stats.game_active and self.game_status == 'pause' and self.menu_mode == 'main':
                        self.game_status = 'play'
                        self.play_time = pygame.time.get_ticks()
                        self.all_pause_time += self.play_time - self.pause_time
                        self.sounds.button()
                        self.stats.game_active = True
                        pygame.mouse.set_visible(False)
                
                    elif self.stats.game_active and self.game_status == 'play':
                        self.game_status = 'pause'
                        self.pause_time = pygame.time.get_ticks()
                        self.sounds.button()
                        self.stats.game_active = False
                        pygame.mouse.set_visible(True)

                    elif not self.stats.game_active and self.menu_mode == 'settings':
                        self.menu_mode = 'main'
                        self.sounds.button()
    
    def _check_keyup_events(self, event):
                """Реагирует на отпускание клавиш"""             
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _press_space(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE] and self.stats.game_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.settings.last_shot_time >= self.settings.fire_delay:
                self._fire_bullet()
                self.settings.last_shot_time = current_time

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в групу bullets"""            
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet) 
        self.sounds.fire()  # Звуки пушки

    def _create_rapid_bonus(self):
        if len(self.rapid_list) < 1:
            bonus = RapidBonus(self)
            self.rapid_list.add(bonus)

    def _create_shield_bonus(self):
        if len(self.shield_list) < 1:
            bonus = ShieldBonus(self)
            self.shield_list.add(bonus)
    
    def _create_fleet_group(self, group_class, group_size, target_group):
        for one in range(group_size):
            unit = group_class(self)
            y = random.randrange(-250, -20)
            x = random.randrange(100, self.settings.screen_width - 100)
            unit.rect.y = y
            unit.rect.x = x
            unit.x = unit.rect.x
            unit.y = unit.rect.y
            target_group.add(unit)
    
    def _create_fleet(self):
        self._create_fleet_group(Alien, self.settings.aliens1_number, self.aliens1)
        self._create_fleet_group(Alien2, self.settings.aliens2_number, self.aliens2)
        self._create_fleet_group(Alien3, self.settings.aliens3_number, self.aliens3)

    def _clear_game_objects(self):
        """Удаляет пришельцев и пули"""
        self.aliens1.empty()
        self.aliens2.empty()
        self.aliens3.empty()
        self.aliens3_bullets.empty()
        self.bullets.empty()

    def _respawn_ship(self):
        """Пересоздает корабль игрока и пришельцев"""
        self._clear_game_objects()
        self.rapid_bonus_active = False
        self.shield_bonus_active = False

        self.scoreboard.prep_hearts()
        #  Создание нового флота и размещение нового корабля игрока
        self.ship.center_ship()
        self._create_fleet()
        sleep(0.1)

    def _game_over(self):
        """Завершает игру при потере всех жизней"""
        self._clear_game_objects()
        self.rapid_list.empty()
        self.shield_list.empty()
        self.rapid_bonus_active = False
        self.shield_bonus_active = False

        self.game_status = 'losing'
        self.stats.game_active = False
        self.saver.save_new_record()
        pygame.mouse.set_visible(True) 

    def _ship_hit(self):
        """Обрабатывает столкновения корабля с пришельцами"""
        self.sounds.destruction()
        self.stats.ships_left -= 1
        if self.stats.ships_left > 0:
            self._respawn_ship()
        else: 
            self._game_over()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        self.all_aliens.empty()
        self.all_aliens.add(self.aliens1, self.aliens2, self.aliens3)
        for one in self.all_aliens.sprites():
            if one.rect.bottom > screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_collisions(self, type_group):
        if pygame.sprite.spritecollideany(self.ship, type_group):
            if not self.shield_bonus_active:
                exp = Explosion(self, self.ship.rect.centerx, self.ship.rect.centery, random.randint(50, 80))            
                self.explosions.add(exp)
                self.sounds.ship_hit()
                self._ship_hit()

    def _alien3_fire(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time > self.alien3_fire_time + self.settings.aliens3_fire_delay:
            for alien in self.aliens3.sprites():
                x = alien.rect.x + alien.rect.width // 2 - 6
                y = alien.rect.bottom
                if alien.rect.bottom > 0:
                    bullet1 = Alien3Bullet(self, x - 25, y)
                    bullet2 = Alien3Bullet(self, x + 25, y)
                    self.aliens3_bullets.add(bullet1, bullet2)
                    self.sounds.fire()
            self.alien3_fire_time = self.current_time
        for bullet in self.aliens3_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.aliens3_bullets.remove(bullet)


    def _update_aliens(self):
        self.aliens1.update()
        self.aliens2.update()
        self.aliens3.update()
        # Проверка коллизий "пришелец - корабль"
        self._ship_collisions(self.aliens1)
        self._ship_collisions(self.aliens2)
        self._ship_collisions(self.aliens3)
        self._ship_collisions(self.aliens3_bullets)
        # Проверить, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()
        # Стрельба противника
        self._alien3_fire()


    def _update_aliens3_bulets(self):
        #if pygame.sprite.collideany(self.ship, )
        self._ship_collisions(self.aliens3_bullets)

    def _update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions_alien1 = pygame.sprite.groupcollide(self.bullets, self.aliens1, True, True)
        collisions_alien2 = pygame.sprite.groupcollide(self.bullets, self.aliens2, True, False)
        collisions_alien3 = pygame.sprite.groupcollide(self.bullets, self.aliens3, True, False)

        if collisions_alien1:
            self.sounds.destruction()  # Звуки разрушения aliens
            for aliens in collisions_alien1.values():
                for alien in aliens:
                    exp = Explosion(self, alien.rect.centerx, alien.rect.centery, random.randint(20, 60))
                    self.explosions.add(exp)

            for aliens in collisions_alien1.values():  # Начисляем очки
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
            if self.rapid.random_drop_rapid():
                self._create_rapid_bonus()
            if self.shield_bonus.random_drop_shield():
                self._create_shield_bonus()
        if collisions_alien2:
            self.sounds.destruction()  # Звуки разрушения aliens2
            for bullet, aliens2 in collisions_alien2.items():  # Уменьшаем ХП, уничтожаем alien2, начисляем очки
                for alien2 in aliens2:
                    alien2.hp -= self.settings.bullet_power
                    alien2.hp_width -= 30
                    exp = Explosion(self, alien2.rect.centerx, alien2.rect.centery, random.randint(30, 90))
                    self.explosions.add(exp)
                    if alien2.hp <= 0:
                        self.stats.score += self.settings.alien2_points * len(aliens2)           
                        alien2.kill()
                        if self.rapid.random_drop_rapid():
                            self._create_rapid_bonus()
                        if self.shield_bonus.random_drop_shield():
                            self._create_shield_bonus()           
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if collisions_alien3:
            self.sounds.destruction()
            for bullet, aliens3 in collisions_alien3.items():  # Уменьшаем ХП, уничтожаем alien2, начисляем очки
                for alien3 in aliens3:
                    alien3.hp -= self.settings.bullet_power
                    alien3.hp_width -= 15
                    exp = Explosion(self, alien3.rect.centerx, alien3.rect.centery, random.randint(40, 120))

                    self.explosions.add(exp)
                    if alien3.hp <= 0:
                        self.stats.score += self.settings.alien3_points * len(aliens3)           
                        alien3.kill()
                        if self.rapid.random_drop_rapid():
                            self._create_rapid_bonus()
                        if self.shield_bonus.random_drop_shield():
                            self._create_shield_bonus()           
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens1 and not self.aliens2 and not self.aliens3:
            #  Уничтожение сущетсвующих снарядов и создание нового флота
            self.bullets.empty()
            self.settings.increase_speed()
            self._create_fleet()
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _get_rapid_bonus(self):
        for rapid in self.rapid_list.copy():
            self.rapid_list.remove(rapid)
        if not self.rapid_bonus_active:
            self.rapid_bonus_active = True
            self.rapid_current_time = pygame.time.get_ticks() - self.all_pause_time
            self.settings.fire_delay /= 1.5
            self.settings.bullet_color = (240, 40, 60)
            self.sounds.rapid(True)
            fast_eff = FastEff(self, self.ship.rect.centerx, self.ship.rect.top)
            self.fast_eff.add(fast_eff)
        elif self.rapid_bonus_active:
            self.rapid_current_time = pygame.time.get_ticks() - self.all_pause_time
            self.sounds.rapid(False)
            self.sounds.rapid(True)
            fast_eff = FastEff(self, self.ship.rect.centerx, self.ship.rect.top)
            self.fast_eff.add(fast_eff)

    def _get_shield_bonus(self):
        for shield in self.shield_list.copy():
            self.shield_list.remove(shield)
        if not self.shield_bonus_active:
            self.shield_bonus_active = True
            self.shield_current_time = pygame.time.get_ticks() - self.all_pause_time
            self.sounds.shield(True)
            shield_eff = ShieldEff(self, self.ship.rect.centerx, self.ship.rect.top)
            self.shield_eff.add(shield_eff)

        elif self.shield_bonus_active:
            self.shield_current_time = pygame.time.get_ticks() - self.all_pause_time
            self.sounds.shield(False)
            self.sounds.shield(True)
            shield_eff = ShieldEff(self, self.ship.rect.centerx, self.ship.rect.top)
            self.shield_eff.add(shield_eff)
   
    def _update_rapid(self):
        self.rapid_list.update()
        for rapid in self.rapid_list.copy():            
            if rapid.rect.top > self.screen_rect.bottom:
                self.rapid_list.remove(rapid)

        if pygame.sprite.spritecollideany(self.ship, self.rapid_list):
            self._get_rapid_bonus()

        if self.rapid_bonus_active:
            if pygame.time.get_ticks() - self.all_pause_time > self.rapid_current_time + self.settings.rapid_bonus_time:
                self.settings.fire_delay *= 1.5
                self.settings.bullet_color = (0, 255, 150)
                self.rapid_bonus_active = False

    def _update_shield(self):
        self.shield_list.update()
        for shield in self.shield_list.copy():            
            if shield.rect.top > self.screen_rect.bottom:
                self.shield_list.remove(shield)

        if pygame.sprite.spritecollideany(self.ship, self.shield_list):
            self._get_shield_bonus()

        if self.shield_bonus_active:
            #self.screen.blit(self.shield.image, self.shield.rect)
            if pygame.time.get_ticks() - self.all_pause_time > self.shield_current_time + self.settings.shield_bonus_time:
                self.shield_bonus_active = False

    def _update(self):
        self.ship.update()
        self.bullets.update()
        self.aliens3_bullets.update()
        self.explosions.update()
        self.shield_eff.update()
        self.fast_eff.update()
        self._update_aliens()
        self._update_bullets()
        self._update_rapid()
        self._update_shield()

    def _draw_background(self):
        self.screen.blit(self.settings.bg_image, (0, self.settings.bgy + 0))
        self.screen.blit(self.settings.bg_image_next, (0, -(self.settings.screen_height) + self.settings.bgy))
        if self.stats.game_active:
            self.settings.bgy += self.settings.bg_speed
        if self.settings.bgy >= self.settings.screen_height:
            self.settings.bgy = 0

    def _draw_active_game(self):
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for bullet in self.aliens3_bullets.sprites():
            bullet.draw_bullet()

        self.aliens1.draw(self.screen)
        self.aliens2.draw(self.screen)
        self.aliens3.draw(self.screen)
        self.explosions.draw(self.screen)
        self.shield_eff.draw(self.screen)
        self.fast_eff.draw(self.screen)

        for alien2 in self.aliens2.sprites():
            alien2.draw_alien2()
        for alien3 in self.aliens3.sprites():
            alien3.draw_alien3()

        self.rapid_list.draw(self.screen)
        self.shield_list.draw(self.screen)

        if self.shield_bonus_active:
            self.scoreboard.show_shield_bonus()
        if self.rapid_bonus_active:
            self.scoreboard.show_rapid_bonus()

        self.scoreboard.show_score()

    def _draw_menu(self, show_continue):
        """Рисует стартовое меню и меню с паузой
        
        Аргументы: 
            show_continue: если True, добавляет кнопку "Продолжить" """
        self.play_button.draw_button(self.settings.play_button_color)
        self.setting_button.draw_button(self.settings.setting_button_color)
        self.quit_button.draw_button(self.settings.quit_button_color)
        self.saver.show_old_record()
        if show_continue:
            self.continue_button.draw_button(self.settings.continue_button_color)

    def _draw(self):
        self._draw_background()
        if self.stats.game_active:
            self._draw_active_game()
        if not self.stats.game_active:
            if self.menu_mode == 'main':
                if self.game_status == 'none':
                    self._draw_menu(show_continue=False)
                elif self.game_status == 'pause':
                    self.sounds.shield(False)
                    self.sounds.rapid(False)
                    self._draw_active_game()
                    self._draw_menu(show_continue=True)
                elif self.game_status == 'losing':
                    self.scoreboard.show_record()
                    self.settings_menu.back_button.draw_button(self.settings.back_button_color)
            if self.menu_mode == 'settings':
                self.settings_menu.draw_settings_menu()
        pygame.display.flip()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
