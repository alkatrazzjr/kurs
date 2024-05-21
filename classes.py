import pygame

class PlayerShip:
    def __init__(self, x, y, images, charge_image):
        self.x = x
        self.y = y
        self.images = images
        self.charge_image = charge_image
        self.speed = 5
        self.boost_speed = 10
        self.charge_left = 5
        self.fuel = 100
        self.is_boosting = False
        self.move_sheep_cnt = 0
        self.ammo = []
        self.meteors_destroyed = 0
        self.score = 0
        self.can_shoot = True
        self.fuel_bar_length = 100
        self.fuel_bar_height = 10
        self.fuel_bar_x = 10
        self.fuel_bar_y = 130
        self.message = ""
        self.message_timer = 0

    def get_current_image(self):
        if self.move_sheep_cnt >= len(self.images):
            self.move_sheep_cnt = 0
        image = self.images[self.move_sheep_cnt]
        self.move_sheep_cnt += 1
        return image

    def move_left(self):
        self.x -= self.boost_speed if self.is_boosting else self.speed

    def move_right(self):
        self.x += self.boost_speed if self.is_boosting else self.speed

    def move_up(self):
        self.y -= self.boost_speed if self.is_boosting else self.speed

    def move_down(self):
        self.y += self.boost_speed if self.is_boosting else self.speed

    def shoot(self):
        if self.charge_left > 0 and self.can_shoot:
            bullet_x = self.x + self.images[0].get_width() // 2 - self.charge_image.get_width() // 2
            bullet_y = self.y - self.charge_image.get_height()
            self.ammo.append(pygame.Rect(bullet_x, bullet_y, self.charge_image.get_width(), self.charge_image.get_height()))
            self.charge_left -= 1
            self.can_shoot = False

    def update_ammo(self, meteors):
        for i, bullet in enumerate(self.ammo):
            bullet.y -= 5
            if bullet.y < -10:
                self.ammo.pop(i)
            for j, meteor in enumerate(meteors):
                if bullet.colliderect(meteor.get_rect()):
                    meteors.pop(j)
                    self.ammo.pop(i)
                    self.meteors_destroyed += 1
                    self.score += 100
                    self.message = "Метеорит сбит!"
                    self.message_timer = 60
                    break

    def draw(self, screen):
        screen.blit(self.get_current_image(), (self.x, self.y))
        for bullet in self.ammo:
            screen.blit(self.charge_image, (bullet.x, bullet.y))

    def boost(self):
        if self.fuel > 0:
            self.is_boosting = True
            self.fuel -= 1
        else:
            self.is_boosting = False

    def stop_boost(self):
        self.is_boosting = False

    def increment_score(self):
        self.score += 1

    def reset(self):
        self.x = 220
        self.y = 450
        self.ammo.clear()
        self.charge_left = 5
        self.meteors_destroyed = 0
        self.score = 0
        self.can_shoot = True
        self.fuel = 100
        self.is_boosting = False
        self.message = ""

    def draw_fuel_bar(self, screen):
        fuel_ratio = self.fuel / 100
        pygame.draw.rect(screen, (255, 0, 0), (self.fuel_bar_x, self.fuel_bar_y, self.fuel_bar_length, self.fuel_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.fuel_bar_x, self.fuel_bar_y, self.fuel_bar_length * fuel_ratio, self.fuel_bar_height))

    def draw_message(self, screen, font):
        if self.message_timer > 0:
            message_surface = font.render(self.message, True, (255, 255, 255))
            screen.blit(message_surface, (screen.get_width() // 2 - message_surface.get_width() // 2, screen.get_height() - 30))
            self.message_timer -= 1

class Meteor:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.speed = 10

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.y > 700

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
