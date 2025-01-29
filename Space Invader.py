from kivy.app import App
from kivy.uix.widget import Widget  
from kivy.uix.image import Image
from kivy.core.window import  Window
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock    #atualização da tela em tempo real
from kivy.properties import ListProperty
from random import randint
import logging

screen_width = 800
screen_height = 600
Window.size = (screen_width, screen_height) 

class Bullet(Widget):
    def __init__(self, **kwargs):
        super(Bullet, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=(0,0), size=(5, 10))
        self.velocity_y = 5
        self.velocity_x = 0
        self. bind(pos=self.update_rect)    
        
    def update_rect(self, *args):
        self.rect.pos = self.pos
            
    def update(self):
        self.y += self.velocity_y
        self.x += self.velocity_x
        
class Enemy(Image):
    def __init__(self, **kwargs):
        super(Enemy, self).__init__(**kwargs)
        self.source = 'enemies.png'
        self.size_hint= (None, None)
        self.size = (50, 50)
       
            
class SpaceInvaderGame(Widget):
    bullets = ListProperty([])
    enemies = ListProperty([])
    
    def __init__(self, **kwargs):
        
        super(SpaceInvaderGame, self).__init__(**kwargs)

        self.logger = logging.getLogger().getChild(__name__)
        
        with self.canvas:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(pos=(0,0), size=(screen_width, screen_height))
            self.background = Image(source='./fundo.png', pos=(0,0), size = Window.size, fit_mode="fill")
                               
        # adicionando a imagem da nave,  com a posiçõa
        self.nave = Image(source='./nave.png', size=(74,74), pos=(screen_width/2-50, 20), allow_stretch = True)
        self.add_widget(self.nave)
        Window.bind(on_resize=self.on_window_resize)

        self.logger.info("Testing Logger, init finished")
        
     # movimentao da nave  
        Window.bind(on_key_down = self.on_key_down)
        Window.bind(on_key_up = self.on_key_up)    
        
        self.left_pressed = False
        self.right_pressed = False
        
        Clock.schedule_interval(self.update, 1.0/60.0)
        Clock.schedule_interval(self.spawn_enemy, 1.0/2.0)
        
        self._init_enemies()

    def on_window_resize(self, width, height, *args):
        self.background.size = Window.size
        self.nave.pos = (Window.size[0]/2-50, 20)
    
    def on_key_down(self, window, key, *args):
        if key == 276:
            self.left_pressed = True
        if key == 275:
            self.right_pressed = True
        if key == 32: #aqui é pra atirar qnd apertar o espaço 
            self.fire_bullet()
                
    def on_key_up(self, window, key, *args):
        if key == 276:
            self.left_pressed = False
        if key == 275:
            self.right_pressed = False
        if key == 32:
            self.fire_bullet()
            
    def update(self, dt):
        if self.left_pressed and self.nave.x > 0:
            self.nave.x -= 5
        if self.right_pressed and self.nave.right < self.width:
            self.nave.x += 5
        for bullet in self.bullets:
            bullet.y += 10
            if bullet.y > screen_height:
                self.remove_widget(bullet)
                self.bullets.remove(bullet) 
                
            bullet.update()
        for enemy in self.enemies:
            
            enemy.y -= 1
            if enemy.y < 0:
                self.remove_widget(enemy)
                self.enemies.remove(enemy)       
                
                
    def fire_bullet(self):
        bullet = Bullet()
        bullet.size = (5, 5)
        bullet.pos = (self.nave.center_x - bullet.width/2, self.nave.top)
        self.add_widget(bullet)
        self.bullets.append(bullet)
       

    def _init_enemies(self):
        enemy = Enemy()
        enemy.pos = (randint(0, screen_width - enemy.width), screen_height)
        self.add_widget(enemy)
        self.enemies.append(enemy)
       
    def spawn_enemy(self, dt):
         while(len(self.enemies) < 15):
            enemy = Enemy()
            enemy.pos = (randint(0, screen_width - enemy.width), screen_height)
            self.add_widget(enemy)
            self.enemies.append(enemy) 
    def collision(self):
        for enemy in self.enemies:
            for bullet in self.bullets:
                if self.is_collision(bullet, enemy):
                    self.remove_widget(bullet)
                    self.bullets.remove(bullet)
                    self.remove_widget(enemy)
                    self.enemies.remove(enemy)
                
    def is_collision(self, enemy, bullet):
        if bullet.x > enemy.x and bullet.x < enemy.right and bullet.y > enemy.y and bullet.y < enemy.top:
            return True
        else:
            return False
            
class SpaceInvaderApp(App):
    def build(self):
        return SpaceInvaderGame()

if __name__ == '__main__':
    SpaceInvaderApp().run() 