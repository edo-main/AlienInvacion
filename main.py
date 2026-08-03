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
from src.game_stats import GameStats
from src.button import Button
from src.scoreboard import Scoreboard
from src.settings_menu import SettingsMenu
from src.sounds import Sounds


class AlienInvasion:
    """Класс для управления ресурасами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""

                  
        pygame.init()
        self.settings = Settings()
        self.sounds = Sounds()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        self.menu_mode = 'main'
        
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.scoreboard = Scoreboard(self)
        self.settings_menu = SettingsMenu(self)
        
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.aliens2 = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play", 
                                  self.settings.play_button_color,
                                  self.settings.play_button_xpos,
                                  self.settings.play_button_ypos,
                                  self.settings.basic_button_width,
                                  self.settings.basic_button_height)
        self.setting_button = Button(self, "Setting", 
                                     self.settings.setting_button_color,
                                     self.settings.setting_button_xpos,
                                     self.settings.setting_button_ypos,
                                     self.settings.basic_button_width,
                                     self.settings.basic_button_height)

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self._update()
            self._draw()

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
                self._check_settings_button(mouse_pos)
                self._check_return_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if play_button_clicked and not self.stats.game_active:
            #  Сброс игровых настроек
            self.settings.initialize_dinamic_settings()
            #  Сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            #  Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.aliens2.empty()
            self.bullets.empty()
            #  Создание нового флота и размещения корабля
            self._create_fleet()
            self.ship.center_ship()
            #  Указатель мыши скрывается
            pygame.mouse.set_visible(False)
            #  Звук кнопик Play
            playsound(r"assets\sounds\button1.mp3", block=False)

    def _check_settings_button(self, mouse_pos):
        """Заходит в меню настроек"""
        settings_button_clicked = self.setting_button.rect.collidepoint(mouse_pos)
        if settings_button_clicked and not self.stats.game_active:
            self.menu_mode = 'settings'
            self.aliens.empty()
            self.bullets.empty()
            playsound(r"assets\sounds\button1.mp3", block=False)

    def _check_return_button(self, mouse_pos):
        """Возврат в главное меню"""
        back_button_clicked = self.settings_menu.back_button.rect.collidepoint(mouse_pos)
        if back_button_clicked and self.menu_mode == 'settings':
            self.menu_mode = 'main'
            playsound(r"assets\sounds\button1.mp3", block=False)


    def _check_keydown_events(self, event):
                """Реагирует на нажатие клавиш"""    
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                
                if event.key == pygame.K_q:
                    sys.exit()

                if self.stats.game_active and event.key == pygame.K_SPACE:                     
                    self._fire_bullet()
                if not self.stats.game_active and event.key == pygame.K_ESCAPE:
                    playsound(r"assets\sounds\button1.mp3", block=False)
                    self.stats.game_active = True
                    pygame.mouse.set_visible(False)
    
                elif self.stats.game_active and event.key == pygame.K_ESCAPE:
                    playsound(r"assets\sounds\button1.mp3", block=False)
                    self.stats.game_active = False
                    pygame.mouse.set_visible(True)
    
    def _check_keyup_events(self, event):
                """Реагирует на отпускание клавиш"""             
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в групу bullets"""            
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet) 

        self.sounds.fire()  # Звуки пушки
    
    def _create_fleet(self):
        for one_alien in range(self.settings.aliens_number):
            alien = Alien(self)
            y = random.randrange(-350, -20)
            x = random.randrange(100, self.settings.screen_width - 100)
            alien.rect.y = y
            alien.rect.x = x
            alien.x = alien.rect.x
            alien.y = alien.rect.y
            self.aliens.add(alien)
        for one_alien2 in range(self.settings.aliens2_number):
            alien2 = Alien2(self)
            y = random.randrange(-350, -20)
            x = random.randrange(100, self.settings.screen_width - 100)
            alien2.rect.y = y
            alien2.rect.x = x
            alien2.x = alien2.rect.x
            alien2.y = alien2.rect.y
            self.aliens2.add(alien2)
  

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ships_left > 0:
            #  Уменьшение жизней
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()
            #  Очистка списков пришельцев и пуль
            self.aliens.empty()
            self.aliens2.empty()
            self.bullets.empty()
            #  Создание нового флота и размещение нового корабля игрока
            self._create_fleet()
            self.ship.center_ship()
            #  Пауза
            sleep(0.5)
        else: 
            #  Когда жизни закончились                                  
            self.stats.game_active = False
            self.aliens.empty()
            self.aliens2.empty()
            pygame.mouse.set_visible(True)  

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #  Происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break
        for alien2 in self.aliens2.sprites():
            if alien2.rect.bottom >= screen_rect.bottom:
                #  Происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break


    def _update_aliens(self):
        self.aliens.update()
        self.aliens2.update()
        #  Проверка коллизий "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.sounds.ship_hit()
            self._ship_hit()
        if pygame.sprite.spritecollideany(self.ship, self.aliens2):
            self.sounds.ship_hit()
            self._ship_hit()
        #  Проверить, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()



    def _update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        collisions2 = pygame.sprite.groupcollide(self.bullets, self.aliens2, True, False)

        if collisions:
            self.sounds.destruction()  # Звуки разрушения aliens

            for aliens in collisions.values():  # Начисляем очки
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if collisions2:
            self.sounds.destruction()  # Звуки разрушения aliens2

            for bullet, aliens2 in collisions2.items():  # Уменьшаем ХП, уничтожаем alien2, начисляем очки
                for alien2 in aliens2:
                    alien2.hp -= self.settings.bullet_power
                    alien2.hp_width -= 30
                    if alien2.hp <= 0:
                        self.stats.score += self.settings.alien2_points * len(aliens2)           
                        alien2.kill()           
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
                         

             

        if not self.aliens and not self.aliens2:
            #  Уничтожение сущетсвующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()


    
    def _update(self):
        self.ship.update()
        self.bullets.update()
        self._update_aliens()
        self._update_bullets()


    def _draw(self):
        """Обновляет изображения на экране"""
        #  Фон
        self.screen.fill(self.settings.bg_color)
        #  Отображаем активную игру
        if self.stats.game_active:
            #  Рисуем наш корабль
            self.ship.blitme()
            #  Рисуем пули
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            #  Рисуем пришельцев
            self.aliens.draw(self.screen)
            self.aliens2.draw(self.screen)
            for alien2 in self.aliens2.sprites():
                alien2.draw_alien2()
            #  Выводим счет очков
            self.scoreboard.show_score()
        #  Отображение меню
        if not self.stats.game_active and self.menu_mode == 'main':
            self.play_button.draw_button(self.settings.play_button_color)
            self.setting_button.draw_button(self.settings.setting_button_color)
        #  Отображение меню настроек
        elif not self.stats.game_active and self.menu_mode == 'settings':
            self.settings_menu.draw_settings_menu()
        # Отображение последнего прорисованного экрана
        pygame.display.flip()



if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
