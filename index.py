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

    if game_state == 'start':
        draw_start_screen()
    elif game_state == 'playing':
        screen.draw.text(f"Pontos: {score}", (10, 10), fontsize=40, color="white")
    elif game_state == 'victory':
        screen.draw.text(f"Pontos: {score}", (10, 10), fontsize=40, color="white")
        screen.draw.text("🎉 Você venceu! 🎉", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="yellow")
        screen.draw.text("Pressione ESPAÇO para jogar novamente", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=40, color="white")

def draw_start_screen():
    screen.draw.text("🚀 Bem-vindo ao Desvia Inimigos!", center=(WIDTH // 2, HEIGHT // 2 - 100), fontsize=50, color="cyan")
    screen.draw.text("Instruções:", center=(WIDTH // 2, HEIGHT // 2 - 30), fontsize=40, color="white")
    screen.draw.text("Use as setas ESQUERDA/DIREITA para mover", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=30, color="white")
    screen.draw.text("Pressione SETA PARA CIMA para pular", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=30, color="white")
    screen.draw.text("Desvie de 20 inimigos para vencer!", center=(WIDTH // 2, HEIGHT // 2 + 100), fontsize=30, color="yellow")
    screen.draw.text("Pressione ENTER para começar", center=(WIDTH // 2, HEIGHT // 2 + 160), fontsize=40, color="lime")

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

    if game_state == 'start':
        if key == keys.RETURN:
            start_game()
    elif game_state == 'playing':
        if key == keys.UP and not is_jumping:
            is_jumping = True
            jump_speed = -10
    elif game_state == 'victory':
        if key == keys.SPACE:
            start_game()

def start_game():
    global game_state, score, player, enemy

    score = 0
    player.x = 100
    player.y = 450
    enemy.x = WIDTH + 100
    enemy.y = 450
    game_state = 'playing'