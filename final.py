import pyxel
import random

# 定数
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GORILLA_WIDTH = 50
GORILLA_HEIGHT = 50
GROUND_HEIGHT = 100
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT
GORILLA_SPEED = 5
JUMP_FORCE = -15
GRAVITY = 1
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 40
COIN_WIDTH = 20
COIN_HEIGHT = 20
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
FPS = 30

class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="ゴリラの冒険")
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        # ゲームの初期化
        self.gorilla_x = 100
        self.gorilla_y = GROUND_Y - GORILLA_HEIGHT
        self.gorilla_width = GORILLA_WIDTH
        self.gorilla_height = GORILLA_HEIGHT
        self.velocity_y = 0
        self.on_ground = True
        self.obstacles = []
        self.coins = []
        self.enemies = []
        self.coins_collected = 0
        self.hits = 0
        self.max_hits = 4
        self.running = True

    def generate_objects(self):
        if random.randint(1, 60) == 1:
            self.obstacles.append([SCREEN_WIDTH, GROUND_Y - OBSTACLE_HEIGHT])
        if random.randint(1, 80) == 1:
            self.coins.append([SCREEN_WIDTH, random.randint(50, GROUND_Y - COIN_HEIGHT)])
        if random.randint(1, 120) == 1:
            self.enemies.append([SCREEN_WIDTH, GROUND_Y - ENEMY_HEIGHT])

    def update(self):
        if not self.running:
            if pyxel.btnp(pyxel.KEY_R):  # リスタート
                self.reset_game()
            return

        # キー入力
        if pyxel.btn(pyxel.KEY_LEFT):
            self.gorilla_x = max(self.gorilla_x - GORILLA_SPEED, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.gorilla_x = min(self.gorilla_x + GORILLA_SPEED, SCREEN_WIDTH - self.gorilla_width)
        if pyxel.btnp(pyxel.KEY_SPACE) and self.on_ground:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False

        # 重力とジャンプ
        self.velocity_y += GRAVITY
        self.gorilla_y += self.velocity_y
        if self.gorilla_y + self.gorilla_height >= GROUND_Y:
            self.gorilla_y = GROUND_Y - self.gorilla_height
            self.velocity_y = 0
            self.on_ground = True

        # オブジェクト生成
        self.generate_objects()

        # 障害物の更新
        for obstacle in self.obstacles[:]:
            obstacle[0] -= GORILLA_SPEED
            if self.check_collision(obstacle, OBSTACLE_WIDTH, OBSTACLE_HEIGHT):
                self.hits += 1
                self.obstacles.remove(obstacle)
            elif obstacle[0] + OBSTACLE_WIDTH < 0:
                self.obstacles.remove(obstacle)

        # コインの更新
        for coin in self.coins[:]:
            coin[0] -= GORILLA_SPEED
            if self.check_collision(coin, COIN_WIDTH, COIN_HEIGHT):
                self.coins_collected += 1
                self.coins.remove(coin)
            elif coin[0] + COIN_WIDTH < 0:
                self.coins.remove(coin)

        # 敵の更新
        for enemy in self.enemies[:]:
            enemy[0] -= GORILLA_SPEED
            if self.check_collision(enemy, ENEMY_WIDTH, ENEMY_HEIGHT):
                self.hits += 1
                self.enemies.remove(enemy)
            elif enemy[0] + ENEMY_WIDTH < 0:
                self.enemies.remove(enemy)

        # ゲームオーバー判定
        if self.hits >= self.max_hits:
            self.running = False

    def check_collision(self, obj, obj_width, obj_height):
        return (
            self.gorilla_x < obj[0] + obj_width
            and self.gorilla_x + self.gorilla_width > obj[0]
            and self.gorilla_y < obj[1] + obj_height
            and self.gorilla_y + self.gorilla_height > obj[1]
        )

    def draw(self):
        pyxel.cls(6)

        if not self.running:
            pyxel.text(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 10, "GAME OVER", 7)
            pyxel.text(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 10, "Press R to Restart", 7)
            return

        # ゴリラ描画
        pyxel.rect(self.gorilla_x, self.gorilla_y, self.gorilla_width, self.gorilla_height, 11)

        # 地面描画
        pyxel.rect(0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT, 3)

        # 障害物描画
        for obstacle in self.obstacles:
            pyxel.rect(obstacle[0], obstacle[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT, 8)

        # コイン描画
        for coin in self.coins:
            pyxel.circ(coin[0] + COIN_WIDTH // 2, coin[1] + COIN_HEIGHT // 2, COIN_WIDTH // 2, 10)

        # 敵描画
        for enemy in self.enemies:
            pyxel.rect(enemy[0], enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT, 7)

        # スコアとライフ
        pyxel.text(10, 10, f"Coins: {self.coins_collected}", 7)
        pyxel.text(10, 20, f"Life: {self.max_hits - self.hits}", 7)


Game()