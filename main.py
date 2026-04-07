import sys
import pygame
import random


from time import sleep
from playsound3 import playsound

from src.settings import Settings
from src.ship import Ship
from src.bullet import Bullet
from src.alien import Alien
from src.game_stats import GameStats
from src.button import Button
from src.scoreboard import Scoreboard


class AlienInvasion:
    """Класс для управления ресурасами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""

                  
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")
        
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.scoreboard = Scoreboard(self)
        
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")

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

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
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
            self.bullets.empty()
            #  Создание нового флота и размещения корабля
            self._create_fleet()
            self.ship.center_ship()
            #  Указатель мыши скрывается
            pygame.mouse.set_visible(False)
            #  Звук кнопик Play
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
        var_sound_shot = random.randrange(2)
        if var_sound_shot == 1:             
            playsound(r"assets\sounds\shot1.mp3", block=False)
        else:
            playsound(r"assets\sounds\shot2.mp3", block=False)
             
        """Создание нового снаряда и включение его в групу bullets"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet) 
    
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        #  Вычисление кол-ва пришельцев по горизонтали
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        #  Вычисление кол-ва пришельцев по вертикали
        available_space_y = self.settings.screen_height - (3 * alien_height)
        number_aliens_y = available_space_y // (2 * alien_height)

        #  Создаем флот
        for x_num in range(number_aliens_x):
            for y_num in range(number_aliens_y):
                self._create_alien(x_num, y_num)

    def _create_alien(self, x_num, y_num):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.rect.x = alien_width + (2 * alien_width * x_num)
        alien.rect.y = alien_height + (2 * alien_height * y_num)
        alien.x = alien.rect.x
        self.aliens.add(alien)

                  
    def _check_fleet_edges(self):
        """Реагирует на достижение прищельцеп края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление движения"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1    

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ships_left > 0:
            #  Уменьшение жизней
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()
            #  Очистка списков пришельцев и пуль
            self.aliens.empty()
            self.bullets.empty()
            #  Создание нового флота и размещение нового корабля игрока
            self._create_fleet()
            self.ship.center_ship()
            #  Пауза
            sleep(0.5)   
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)  

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #  Происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break


    def _update_aliens(self):
        self.aliens.update()
        self._check_fleet_edges()

        #  Проверка коллизий "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            playsound(r"assets\sounds\ship_hit1.mp3", block=False)
            self._ship_hit()
        #  Проверить, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()



    def _update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            var_sound_destruction = random.randrange(5)
            if var_sound_destruction == 1:             
                playsound(r"assets\sounds\destruction1.mp3", block=False)
            elif var_sound_destruction == 2:
                playsound(r"assets\sounds\destruction2.mp3", block=False)
            elif var_sound_destruction == 3:
                playsound(r"assets\sounds\destruction3.mp3", block=False)
            elif var_sound_destruction == 4:
                playsound(r"assets\sounds\destruction4.mp3", block=False)
            else:
                playsound(r"assets\sounds\destruction5.mp3", block=False)
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
             

        if not self.aliens:
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
        #  
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        #  Рисуем пули
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #  Рисуем пришельцев
        self.aliens.draw(self.screen)
        # Кнопка Play отображается в том случае, если игра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()
        #  Выводим счет очков
        self.scoreboard.show_score()
        # Отображение последнего прорисованного экрана
        pygame.display.flip()



if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
