import pygame
from classes import PlayerShip, Meteor

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Shooting Stars")

icon_app = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon_app)

bg = pygame.image.load('images/background.png').convert_alpha()
bg_sound = pygame.mixer.Sound('sounds/04.Battle.mp3')
bg_sound.play()

label = pygame.font.Font('fonts/Montserrat-Thin.ttf', 40)
loose_label = label.render(' Вы проиграли ', False, (193, 196, 77))
restart_label = label.render(' заново ', False, (193, 96, 77))
restart_label_rect = restart_label.get_rect(topleft=(180, 200))

font = pygame.font.Font('fonts/Montserrat-Thin.ttf', 20)

meteor_image = pygame.image.load('images/meteor.png').convert_alpha()
meteor_y = -30
meteor_x = 220

meteor_timer = pygame.USEREVENT + 1
pygame.time.set_timer(meteor_timer, 3000)

meteor_list = []

charge_image = pygame.image.load('images/Charge_1.png').convert_alpha()

move_sheep_images = [
    pygame.image.load('images/move/1.png').convert_alpha(),
    pygame.image.load('images/move/2.png').convert_alpha(),
    pygame.image.load('images/move/3.png').convert_alpha(),
    pygame.image.load('images/move/4.png').convert_alpha(),
    pygame.image.load('images/move/5.png').convert_alpha(),
    pygame.image.load('images/move/6.png').convert_alpha()
]

player_ship = PlayerShip(220, 450, move_sheep_images, charge_image)

bg_y = 0
gameplay = True
running = True

while running:

    clock.tick(20)

    screen.blit(bg, (0, bg_y))
    screen.blit(bg, (0, bg_y - 640))

    if gameplay:
        player_ship.draw(screen)

        sheep_rect = pygame.Rect(player_ship.x, player_ship.y, player_ship.images[0].get_width(),
                                 player_ship.images[0].get_height())

        if meteor_list:
            for i, meteor in enumerate(meteor_list):
                meteor.draw(screen)
                meteor.move()

                if meteor.off_screen():
                    meteor_list.pop(i)

                if sheep_rect.colliderect(meteor.get_rect()):
                    gameplay = False

        player_ship.update_ammo(meteor_list)
        player_ship.increment_score()

        if bg_y == 640:
            bg_y = 0
        else:
            bg_y += 2

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_ship.x > 0:
            player_ship.move_left()
        elif keys[pygame.K_RIGHT] and player_ship.x < 500:
            player_ship.move_right()
        elif keys[pygame.K_UP]:
            player_ship.move_up()
        elif keys[pygame.K_DOWN]:
            player_ship.move_down()
        if keys[pygame.K_SPACE]:
            player_ship.shoot()
        else:
            player_ship.can_shoot = True

        if keys[pygame.K_LSHIFT]:
            player_ship.boost()
        else:
            player_ship.stop_boost()

        # Display stats
        score_text = font.render(f'Очки: {player_ship.score}', True, (255, 255, 255))
        meteors_destroyed_text = font.render(f'Уничтожено метеоритов: {player_ship.meteors_destroyed}', True,
                                             (255, 255, 255))
        charge_left_text = font.render(f'Осталось пуль: {player_ship.charge_left}', True, (255, 255, 255))

        screen.blit(score_text, (10, 10))
        screen.blit(meteors_destroyed_text, (10, 40))
        screen.blit(charge_left_text, (10, 70))
        player_ship.draw_fuel_bar(screen)
        player_ship.draw_message(screen, font)

    else:
        screen.fill((87, 89, 89))
        screen.blit(loose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_ship.reset()
            meteor_list.clear()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == meteor_timer:
            meteor_list.append(Meteor(meteor_x, meteor_y, meteor_image))
