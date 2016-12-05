# Created by: Hamza Salman
# Created on: November 2016
# Created for: ICS3U
# This scene shows the game scene.

from scene import *
import ui
from numpy import random

class GameScene(Scene):
    def setup(self):
        # this method is called, when user moves to this scene
        
        #Removed deepcopy
        self.size_of_screen_x = self.size.x
        self.size_of_screen_y = self.size.y
        self.center_of_screen_x = self.size_of_screen_x/2
        self.center_of_screen_y = self.size_of_screen_y/2
        
        self.menu_button_position = Vector2(self.center_of_screen_x, self.center_of_screen_y)
        self.menu_button_created = False
        self.right_button_pressed = False
        self.left_button_pressed = False
        self.speed_of_spaceship = 20.0
        self.missiles = []
        self.aliens = []
        self.alien_attack_rate = 1
        self.alien_attack_speed = 20.0
        self.scale_of_object = 0.75
        self.game_over = False
        self.score = 0
        
        background_position = Vector2(self.center_of_screen_x, self.center_of_screen_y)
        self.background = SpriteNode('./assets/sprites/star_background.PNG',
                                     position = background_position,
                                     parent = self,
                                     size = self.size)
        
        spaceship_position = Vector2(self.center_of_screen_x, 100)
        self.spaceship = SpriteNode('./assets/sprites/spaceship.PNG',
                                      parent = self,
                                      position = spaceship_position,
                                      scale = self.scale_of_object)
        
        left_button_position = Vector2(100, 100)
        self.left_button = SpriteNode('./assets/sprites/left_button.PNG',
                                      parent = self,
                                      position = left_button_position,
                                      alpha = 0.5,
                                      scale = self.scale_of_object)
        
        right_button_position = Vector2(250, 100)
        self.right_button = SpriteNode('./assets/sprites/right_button.PNG',
                                      parent = self,
                                      position = right_button_position,
                                      alpha = 0.5,
                                      scale = self.scale_of_object)
        
        red_button_position = Vector2(self.size_of_screen_x - 100, 100)
        self.red_button = SpriteNode('./assets/sprites/red_button.PNG',
                                      parent = self,
                                      position = red_button_position,
                                      alpha = 0.5,
                                      scale = self.scale_of_object)
        
        score_label_position = Vector2(50, self.size_of_screen_y - 10)
        self.score_label = LabelNode(text = 'Score: 0',
                                     font = ('Helvetica', 20),
                                     parent = self,
                                     position = score_label_position)
    
    def update(self):
        # this method is called, hopefully, 60 times a second
        
        if self.left_button_pressed == True:
            self.spaceship.run_action(Action.move_by(-1*self.speed_of_spaceship, 0.0, 0.1))
        if self.right_button_pressed == True:
            self.spaceship.run_action(Action.move_by(self.speed_of_spaceship, 0.0, 0.1))
        
        # This should create an alien every 1/60 to 2 seconds
        alien_create_chance = random.randint(1, 60)
        if alien_create_chance <= self.alien_attack_rate and self.game_over == False:
            self.add_alien()
        
        for missile in self.missiles:
            if missile.position.y > self.size_of_screen_y + 100:
                missile.remove_from_parent()
                self.missiles.remove(missile)
        
        for alien in self.aliens:
            if alien.position.y < -50:
                if self.game_over == False:
                    self.score = self.score - 2
                alien.remove_from_parent()
                self.aliens.remove(alien)
        
        if len(self.missiles) > 0 and len(self.aliens) > 0:
            for missile in self.missiles:
                for alien in self.aliens:
                    if alien.frame.intersects(missile.frame):
                        missile.remove_from_parent()
                        self.missiles.remove(missile)
                        alien.remove_from_parent()
                        self.aliens.remove(alien)
                        self.score = self.score + 1
        
        for alien_hit in self.aliens:
            if alien_hit.frame.intersects(self.spaceship.frame):
                self.spaceship.position = Vector2(-300, -500)
                self.spaceship.remove_from_parent()
                alien_hit.remove_from_parent()
                self.aliens.remove(alien_hit)
                self.game_over = True
        
        if not self.score_label.text == 'Score: ' + str(self.score) and self.game_over == False:
            self.score_label.text = 'Score: ' + str(self.score)
        
        if self.game_over == True and self.menu_button_created == False:
            
            self.menu_button = SpriteNode('./assets/sprites/menu_button.PNG',
                                          parent = self,
                                          position = self.menu_button_position,
                                          scale = self.scale_of_object)
            self.menu_button_created = True
    
    def touch_began(self, touch):
        # this method is called, when user touches the screen
        
        if self.left_button.frame.contains_point(touch.location):
            self.left_button_pressed = True
        
        if self.right_button.frame.contains_point(touch.location):
            self.right_button_pressed = True
    
    def touch_moved(self, touch):
        # this method is called, when user moves a finger around on the screen
        pass
    
    def touch_ended(self, touch):
        # this method is called, when user releases a finger from the screen
        
        self.right_button_pressed = False
        self.left_button_pressed = False
        
        if self.red_button.frame.contains_point(touch.location) and self.game_over == False:
            self.create_new_missile()
        
        if self.game_over == True and self.menu_button.frame.contains_point(touch.location):
            self.dismiss_modal_scene()
    
    def did_change_size(self):
        # this method is called, when user changes the orientation of the screen
        # thus changing the size of each dimension
        pass
    
    def pause(self):
        # this method is called, when user touches the home button
        # save anything before app is put to background
        pass
    
    def resume(self):
        # this method is called, when user place app from background 
        # back into use. Reload anything you might need.
        pass
    
    def create_new_missile(self):
        #creates new missile and adds it to an array when called
        
        missile_start_position = self.spaceship.position
        missile_end_position = Vector2(self.spaceship.position.x, self.size_of_screen_y)
        self.missiles.append(SpriteNode('./assets/sprites/missile.PNG',
                                      parent = self,
                                      position = missile_start_position,
                                      scale = self.scale_of_object))
        
        missile_move_action = Action.move_to(missile_end_position.x,
                                             missile_end_position.y + 100,
                                             3.0)
        self.missiles[len(self.missiles) - 1].run_action(missile_move_action)
    
    def add_alien(self):
        # When this is called it creates a new alien
        
        alien_start_position = Vector2(random.randint(100, self.size_of_screen_x - 99),
                                       self.size_of_screen_y + 60)
        
        alien_end_position = Vector2(random.randint(100, self.size_of_screen_x - 99), -100)
        
        self.aliens.append(SpriteNode('./assets/sprites/alien.PNG',
                                      parent = self,
                                      position = alien_start_position))
        
        alien_move_action = Action.move_to(alien_end_position.x,
                                           alien_end_position.y,
                                           self.alien_attack_speed,
                                           TIMING_SINODIAL)
        
        self.aliens[len(self.aliens) - 1].run_action(alien_move_action)
