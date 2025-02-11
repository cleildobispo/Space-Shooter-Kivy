from kivy.app import App
from kivy.uix.widget import Widget  
from kivy.uix.image import Image
from kivy.core.window import  Window
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock    #atualização da tela em tempo real
from kivy.properties import ListProperty, OptionProperty
from random import randint
import logging

screen_width = 800
screen_height = 600
Window.size = (screen_width, screen_height) 

class Municao(Widget):
    def __init__(self, **kwargs):
        super(Municao, self).__init__(**kwargs)
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
        
class Inimigo(Image):
    def __init__(self, **kwargs):
        super(Inimigo, self).__init__(**kwargs)
        self.source = 'enemies.png'
        self.size_hint= (None, None)
        self.size = (100, 100)
       
            
class SpaceInvaderGame(Widget):
    tiros = ListProperty([])
    inimigos = ListProperty([])
    game_overimage = OptionProperty('gameover.png')
    game_over_flag = False
    
    
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
        Window.bind(on_resize=self.window_resize)

        self.logger.info("Testing Logger, init finished")
        
     # movimentao da nave  
        Window.bind(on_key_down = self.IrDireita)
        Window.bind(on_key_up = self.IrEsquerda)    
        
        self.left_pressed = False
        self.right_pressed = False
        
        Clock.schedule_interval(self.update, 1.0/60.0)
        Clock.schedule_interval(self.spawn_inimigo, 1.0/2.0)
        
        self._init_inimigos()

    def window_resize(self, width, height, *args):
        self.background.size = Window.size
        self.nave.pos = (Window.size[0]/2-50, 20)
    
    def IrDireita(self, window, key, *args):
        if key == 276:
            self.left_pressed = True
        if key == 275:
            self.right_pressed = True
        if key == 32: #aqui é pra atirar qnd apertar o espaço 
            self.atirar()
                
    def IrEsquerda(self, window, key, *args):
        if key == 276:
            self.left_pressed = False
        if key == 275:
            self.right_pressed = False
        if key == 32:
            self.atirar()
            
    def update(self, dt):
        if self.game_over_flag:
            return
        
        if self.left_pressed and self.nave.x > 0:
            self.nave.x -= 5
        if self.right_pressed and self.nave.right < self.width:
            self.nave.x += 5
        for bullet in self.tiros:
            bullet.y += 10
            if bullet.y > screen_height:
                self.remove_widget(bullet)
                self.tiros.remove(bullet) 
                
            bullet.update()
        for enemy in self.inimigos:
            
            enemy.y -= 1
            if enemy.y < 0:
                self.remove_widget(enemy)
                self.inimigos.remove(enemy)       
                
        self.ver_colisao()
        
    def atirar(self):
        if self.game_over_flag:
            return
        bullet = Municao()
        bullet.size = (5, 5)
        bullet.pos = (self.nave.center_x - bullet.width/2, self.nave.top)
        self.add_widget(bullet)
        self.tiros.append(bullet)
       

    def _init_inimigos(self):
        enemy = Inimigo()
        enemy.pos = (randint(0, screen_width - enemy.width), screen_height)
        self.add_widget(enemy)
        self.inimigos.append(enemy)
       
    def spawn_inimigo(self, dt):
         while(len(self.inimigos) < 15):
            enemy = Inimigo()
            enemy.pos = (randint(0, screen_width - enemy.width), screen_height)
            self.add_widget(enemy)
            self.inimigos.append(enemy) 
    def ver_colisao(self):
        for enemy in self.inimigos:
            for bullet in self.tiros:
                if self.colisao(bullet, enemy):
                    self.remove_widget(bullet)
                    self.remove_widget(enemy)
                    self.tiros.remove(bullet)
                    self.inimigos.remove(enemy)
                    break
        for enemy in self.inimigos[:]:
            if self.colisao(enemy, self.nave):
                self.game_over() 
            
        
              
    def colisao(self, obj1, obj2):
        if (obj1.x < obj2.right and obj1.right > obj2.x and
            obj1.y < obj2.top and obj1.top > obj2.y):
            return True
        return False
     
def game_over(self):
    self.game_over_flag = True
    for bullet in self.tiros:
        self.remove_widget(bullet)
    for enemy in self.inimigos:
        self.remove_widget(enemy)
    self.bullets.clear()
    self.enemies.clear()    
    self.game_over_image = source='gameover.png'       
    self.game_over.image.size = (400, 400)
    self.add_widget(self.game_over_image)
    self.game_over_image.pos = (screen_width/2 - 200, screen_height/2 - 200)
    self.add_widget(self.game_over_image)
    
class SpaceInvaderApp(App):
    def build(self):
        return SpaceInvaderGame()

if __name__ == '__main__':
    SpaceInvaderApp().run() 
