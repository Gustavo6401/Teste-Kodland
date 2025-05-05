# Personagem principal
player = Actor('player')
player.x = 100
player.y = 450

# Controle de Pulo
is_jumping = False
jump_speed = 0
gravity = 0.5

WIDTH = 800
HEIGHT = 600

# Inimigo Vermelho
enemy = Actor('enemy')
enemy.x = WIDTH + 100
enemy.y = 450

start_button = Actor('start_game', center=(WIDTH // 2, HEIGHT // 2 - 70))
sound = Actor('sound', center=(WIDTH // 2, HEIGHT // 2))
exit = Actor('exit', center=(WIDTH // 2, HEIGHT // 2 + 70))

scenario = Actor('scenario', (WIDTH // 2, HEIGHT // 2))
scenario2 = Actor('scenario', (WIDTH + WIDTH // 2, HEIGHT // 2))

scroll_speed = 2 # Velocidade do Scroll

# Pontuação
score = 0
victory_score = 20
game_won = False

game_state = 'start'

def draw():
    screen.clear()
    scenario.draw()
    scenario2.draw()
    player.draw()
    enemy.draw()

    sounds.music.play()

    if game_state == 'start':
        draw_start_screen()
    elif game_state == 'playing':
        screen.draw.text(f"Pontos: {score}", (10, 10), fontsize=40, color="white")
    elif game_state == 'victory':
        screen.draw.text(f"Pontos: {score}", (10, 10), fontsize=40, color="white")
        screen.draw.text("🎉 Você venceu! 🎉", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="yellow")
        screen.draw.text("Pressione ESPAÇO para jogar novamente", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=40, color="white")

def draw_start_screen():
    start_button.draw()
    sound.draw()
    exit.draw()

def update():
    if game_state == 'playing':
        scroll_background()
        move_player()
        apply_gravity()
        move_enemy()
        check_collision()
        

def scroll_background():
    scenario.x -= scroll_speed
    scenario2.x -= scroll_speed

    if scenario.right < 0:
        scenario.left = scenario2.right
    if scenario2.right < 0:
        scenario2.left = scenario.right

def move_player():
    if keyboard.right:
        player.x += 5
    if keyboard.left:
        player.x -= 5

    # Mantém o Personagem Dentro da Tela
    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH

def apply_gravity():
    global is_jumping, jump_speed

    if is_jumping:
        player.y += jump_speed
        jump_speed += gravity

        # Quando cai de Volta no Chão
        if player.y >= 450:
            player.y = 450
            is_jumping = False

def move_enemy():
    global score, game_state

    enemy.x -= 4

    # Quando inimigo sai da tela (player desviou)
    if enemy.right < 0:
        enemy.left = WIDTH + 50
        score += 1
        print(f"Pontos: {score}")

        if score >= victory_score:
            game_state = 'victory'
            print("🎉 Você venceu!")

def check_collision():
    if player.colliderect(enemy):
        global score
        print("🔥 Colidiu com o inimigo!")
        reset_enemy()
        score = 0

def reset_enemy():
    enemy.left = WIDTH + 50  # reseta a posição do inimigo

def on_key_down(key):
    global is_jumping, jump_speed, game_state, score

    if game_state == 'playing':
        if key == keys.UP and not is_jumping:
            is_jumping = True
            jump_speed = -10

def on_mouse_down(pos):
    global game_state

    if start_button.collidepoint(pos):
        start_game()

    if sound.collidepoint(pos):
        print()

    if exit.collidpoint(pos):
        print()

def start_game():
    global game_state, score, player, enemy

    score = 0
    player.x = 100
    player.y = 450
    enemy.x = WIDTH + 100
    enemy.y = 450
    game_state = 'playing'