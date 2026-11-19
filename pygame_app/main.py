"""
WordRhythm: 2D Rhythm Boss Battle (Pygame & Pygbag WebAssembly Edition)
Fully compatible with pygbag for WebAssembly compilation and native desktop Pygame execution.
"""
import asyncio
import math
import time
import random
import sys
import os
import pygame

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
FONT_TITLE = pygame.font.SysFont("Arial", 28, bold=True)
FONT_MAIN = pygame.font.SysFont("Arial", 20, bold=True)
FONT_SMALL = pygame.font.SysFont("Arial", 16)
FONT_PHONETIC = pygame.font.SysFont("Courier", 18)

# Colors
COLOR_BG = (12, 14, 28)
COLOR_CYAN = (0, 255, 204)
COLOR_BLUE = (0, 229, 255)
COLOR_PINK = (255, 0, 127)
COLOR_RED = (255, 42, 95)
COLOR_YELLOW = (255, 230, 0)
COLOR_WHITE = (240, 244, 252)
COLOR_GRAY = (80, 90, 110)

SAMPLE_CHALLENGES = [
    {
        "type": "sentence_assemble",
        "vn_prompt": "Tôi muốn ăn một quả táo tươi ngon.",
        "target_words": ["I", "want", "to", "eat", "a", "fresh", "apple"],
        "distractors": ["drinks", "he", "an"],
        "bpm": 110
    },
    {
        "type": "fill_blank",
        "sentence": "She is following an Italian ___ to cook pasta.",
        "target": "recipe",
        "hint": "Công thức nấu ăn (/ˈres.ə.pi/)",
        "bpm": 115
    },
    {
        "type": "vocab_pronounce",
        "vn_prompt": "loài người, con người",
        "target": "human",
        "phonetic": "/ˈhjuː.mən/",
        "bpm": 120
    },
    {
        "type": "paragraph_order",
        "vn_prompt": "Sắp xếp thứ tự đoạn văn (1-3):",
        "sentences": [
            {"id": 1, "text": "First, wake up early."},
            {"id": 2, "text": "Next, drink warm water."},
            {"id": 3, "text": "Finally, start your workout."}
        ],
        "bpm": 110
    }
]

class GameState:
    def __init__(self):
        self.player_hp = 3
        self.boss_hp = 100
        self.boss_max_hp = 100
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.bpm = 115
        self.beat_interval = 60.0 / self.bpm
        self.last_beat_time = time.time()
        self.beat_pulse = 0.0

        self.current_idx = 0
        self.assembled_words = []
        self.input_text = ""
        self.paragraph_order = []
        self.game_over = False
        self.victory = False

        self.boss_shake = 0
        self.boss_hurt = 0
        self.floating_texts = []

        self.setup_challenge()

    def setup_challenge(self):
        if self.current_idx >= len(SAMPLE_CHALLENGES):
            self.victory = True
            return

        ch = SAMPLE_CHALLENGES[self.current_idx]
        self.bpm = ch.get("bpm", 115)
        self.beat_interval = 60.0 / self.bpm
        self.assembled_words = []
        self.input_text = ""

        if ch["type"] == "sentence_assemble":
            pool = list(ch["target_words"]) + list(ch["distractors"])
            random.shuffle(pool)
            self.word_pool = [{"word": w, "used": False} for w in pool]
        elif ch["type"] == "paragraph_order":
            self.paragraph_order = list(ch["sentences"])
            random.shuffle(self.paragraph_order)

    def damage_boss(self, amount):
        self.boss_hp = max(0, self.boss_hp - amount)
        self.boss_shake = 15
        self.boss_hurt = 10
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        pts = 100 * (1 + (self.combo // 5))
        self.score += pts
        self.floating_texts.append({"text": f"-{amount} HP!", "x": 400, "y": 140, "color": COLOR_CYAN, "life": 40})

        if self.boss_hp <= 0:
            self.victory = True
        else:
            self.current_idx += 1
            self.setup_challenge()

    def damage_player(self):
        self.combo = 0
        self.boss_shake = 20
        self.floating_texts.append({"text": "MISS!", "x": 400, "y": 200, "color": COLOR_RED, "life": 45})
        self.current_idx += 1
        self.setup_challenge()

async def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("WordRhythm - 2D Pygame & Pygbag WebAssembly Edition")
    clock = pygame.time.Clock()

    # Load Boss PNG icons from assets
    boss_images = {}
    assets_dir = os.path.join(os.path.dirname(__file__), "assets", "bosses")
    if os.path.exists(assets_dir):
        for name in ["boss_chef", "boss_cyber", "boss_chimera", "boss_monopoly", "boss_nomad", "boss_examiner"]:
            p = os.path.join(assets_dir, f"{name}.png")
            if os.path.exists(p):
                try:
                    raw = pygame.image.load(p).convert_alpha()
                    boss_images[name] = pygame.transform.smoothscale(raw, (90, 90))
                except Exception as e:
                    print(f"Could not load {p}: {e}")

    state = GameState()
    running = True

    while running:
        current_time = time.time()
        dt = current_time - state.last_beat_time

        if dt >= state.beat_interval:
            state.last_beat_time = current_time
            state.beat_pulse = 1.0

        if state.beat_pulse > 0:
            state.beat_pulse = max(0.0, state.beat_pulse - 0.08)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if state.game_over or state.victory:
                    if event.key == pygame.K_r:
                        state = GameState()
                    continue

                ch = SAMPLE_CHALLENGES[state.current_idx]
                if ch["type"] == "sentence_assemble":
                    # Hotkeys 1-9 to pick words
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        idx = event.key - pygame.K_1
                        if idx < len(state.word_pool) and not state.word_pool[idx]["used"]:
                            state.word_pool[idx]["used"] = True
                            state.assembled_words.append(state.word_pool[idx]["word"])
                    elif event.key == pygame.K_RETURN:
                        # Check sentence
                        ans = " ".join(state.assembled_words).strip().lower()
                        target = " ".join(ch["target_words"]).strip().lower()
                        if ans == target:
                            state.damage_boss(30)
                        else:
                            state.damage_player()
                    elif event.key == pygame.K_BACKSPACE:
                        if state.assembled_words:
                            w = state.assembled_words.pop()
                            for item in state.word_pool:
                                if item["word"] == w and item["used"]:
                                    item["used"] = False
                                    break

                elif ch["type"] in ["fill_blank", "vocab_pronounce"]:
                    if event.key == pygame.K_BACKSPACE:
                        state.input_text = state.input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        ans = state.input_text.strip().lower()
                        target = ch["target"].lower()
                        if ans == target:
                            state.damage_boss(35)
                        else:
                            state.damage_player()
                    else:
                        if len(event.unicode) > 0 and event.unicode.isprintable():
                            state.input_text += event.unicode

                elif ch["type"] == "paragraph_order":
                    if event.key == pygame.K_RETURN:
                        is_sorted = all(s["id"] == i + 1 for i, s in enumerate(state.paragraph_order))
                        if is_sorted:
                            state.damage_boss(40)
                        else:
                            state.damage_player()
                    elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                        # Swap first two for demo ordering
                        state.paragraph_order[0], state.paragraph_order[1] = state.paragraph_order[1], state.paragraph_order[0]

        # Draw Screen
        screen.fill(COLOR_BG)

        # Beat Ring
        pulse_r = int(50 + state.beat_pulse * 30)
        pygame.draw.circle(screen, (0, int(150 + state.beat_pulse * 105), int(200 + state.beat_pulse * 55)), (400, 160), pulse_r, 2)

        # Boss
        boss_x = 400 + (random.randint(-state.boss_shake, state.boss_shake) if state.boss_shake > 0 else 0)
        boss_y = 160
        if state.boss_shake > 0: state.boss_shake -= 1

        # Determine Boss Avatar for current challenge
        b_key = "boss_chef"
        if ch:
            if ch.get("type") == "vocab_pronounce":
                b_key = "boss_cyber"
            elif ch.get("type") == "paragraph_order":
                b_key = "boss_examiner"

        b_img = boss_images.get(b_key)
        if b_img:
            screen.blit(b_img, (boss_x - 45, boss_y - 45))
            if state.boss_hurt > 0:
                state.boss_hurt -= 1
                pygame.draw.circle(screen, COLOR_RED, (boss_x, boss_y), 47, 3)
            else:
                pygame.draw.circle(screen, COLOR_CYAN, (boss_x, boss_y), 47, 2)
        else:
            boss_color = COLOR_RED if state.boss_hurt > 0 else COLOR_CYAN
            if state.boss_hurt > 0: state.boss_hurt -= 1
            pygame.draw.circle(screen, boss_color, (boss_x, boss_y), 45)
            pygame.draw.circle(screen, COLOR_WHITE, (boss_x - 16, boss_y - 6), 6)
            pygame.draw.circle(screen, COLOR_WHITE, (boss_x + 16, boss_y - 6), 6)

        # Boss HP Bar
        hp_bar_w = 300
        hp_pct = max(0, state.boss_hp / state.boss_max_hp)
        pygame.draw.rect(screen, COLOR_GRAY, (250, 40, hp_bar_w, 16))
        pygame.draw.rect(screen, COLOR_CYAN, (250, 40, int(hp_bar_w * hp_pct), 16))
        hp_txt = FONT_SMALL.render(f"BOSS HP: {state.boss_hp} / {state.boss_max_hp}", True, COLOR_WHITE)
        screen.blit(hp_txt, (340, 20))

        # Stats
        stats_txt = FONT_SMALL.render(f"SCORE: {state.score}  |  COMBO: {state.combo}x  |  BPM: {state.bpm}", True, COLOR_YELLOW)
        screen.blit(stats_txt, (30, 70))

        # Render Active Challenge
        if not state.game_over and not state.victory:
            ch = SAMPLE_CHALLENGES[state.current_idx]
            ch_type_txt = FONT_MAIN.render(f"THỬ THÁCH: {ch['type'].upper()}", True, COLOR_CYAN)
            screen.blit(ch_type_txt, (50, 260))

            if ch["type"] == "sentence_assemble":
                vn_txt = FONT_MAIN.render(f"Boss: \"{ch['vn_prompt']}\"", True, COLOR_WHITE)
                screen.blit(vn_txt, (50, 300))

                # Render assembled words
                ans_str = " ".join(state.assembled_words) or "[Chọn các từ 1-9 bên dưới...]"
                ans_txt = FONT_MAIN.render(f"Câu ghép: {ans_str}", True, COLOR_YELLOW)
                screen.blit(ans_txt, (50, 340))

                # Render buttons
                for i, item in enumerate(state.word_pool):
                    col = COLOR_GRAY if item["used"] else COLOR_CYAN
                    w_txt = FONT_SMALL.render(f"[{i+1}] {item['word']}", True, col)
                    screen.blit(w_txt, (50 + (i % 5) * 140, 400 + (i // 5) * 40))

                enter_txt = FONT_SMALL.render("Nhấn [ENTER] để tấn công | [BACKSPACE] để xóa từ vừa chọn", True, COLOR_WHITE)
                screen.blit(enter_txt, (50, 520))

            elif ch["type"] == "fill_blank":
                s_txt = FONT_MAIN.render(ch["sentence"], True, COLOR_WHITE)
                screen.blit(s_txt, (50, 300))
                h_txt = FONT_SMALL.render(f"Gợi ý: {ch['hint']}", True, COLOR_YELLOW)
                screen.blit(h_txt, (50, 340))

                inp_box = FONT_TITLE.render(f"> {state.input_text}_", True, COLOR_CYAN)
                screen.blit(inp_box, (50, 390))
                screen.blit(FONT_SMALL.render("Gõ từ còn thiếu và nhấn [ENTER]", True, COLOR_WHITE), (50, 460))

            elif ch["type"] == "vocab_pronounce":
                vn_txt = FONT_TITLE.render(f"Từ vựng: {ch['vn_prompt']}", True, COLOR_WHITE)
                screen.blit(vn_txt, (50, 300))
                p_txt = FONT_PHONETIC.render(f"Phát âm: {ch['phonetic']}", True, COLOR_YELLOW)
                screen.blit(p_txt, (50, 350))

                inp_box = FONT_TITLE.render(f"> {state.input_text}_", True, COLOR_CYAN)
                screen.blit(inp_box, (50, 400))
                screen.blit(FONT_SMALL.render("Nhập từ tiếng Anh tương ứng và nhấn [ENTER]", True, COLOR_WHITE), (50, 470))

            elif ch["type"] == "paragraph_order":
                screen.blit(FONT_MAIN.render(ch["vn_prompt"], True, COLOR_WHITE), (50, 300))
                for i, s in enumerate(state.paragraph_order):
                    p_txt = FONT_SMALL.render(f"{i+1}. {s['text']}", True, COLOR_CYAN)
                    screen.blit(p_txt, (50, 340 + i * 36))
                screen.blit(FONT_SMALL.render("Nhấn mũi tên [UP/DOWN] để hoán đổi, [ENTER] để xác nhận", True, COLOR_YELLOW), (50, 500))

        elif state.victory:
            win_txt = FONT_TITLE.render("🏆 CHIẾN THẮNG! BOSS ĐÃ BỊ HẠ GỤC!", True, COLOR_CYAN)
            screen.blit(win_txt, (180, 300))
            screen.blit(FONT_MAIN.render(f"Tổng Điểm: {state.score} | Max Combo: {state.max_combo}x", True, COLOR_WHITE), (240, 360))
            screen.blit(FONT_SMALL.render("Nhấn [R] để chơi lại màn đấu", True, COLOR_YELLOW), (280, 420))

        elif state.game_over:
            lose_txt = FONT_TITLE.render("💀 BẠN ĐÃ THUA CUỘC (HẾT 3 HP)!", True, COLOR_RED)
            screen.blit(lose_txt, (200, 300))
            screen.blit(FONT_SMALL.render("Nhấn [R] để hồi sinh và tái đấu", True, COLOR_YELLOW), (280, 380))

        # Floating texts
        for ft in list(state.floating_texts):
            ft["y"] -= 1.2
            ft["life"] -= 1
            if ft["life"] <= 0:
                state.floating_texts.remove(ft)
            else:
                txt = FONT_MAIN.render(ft["text"], True, ft["color"])
                screen.blit(txt, (ft["x"] - txt.get_width() // 2, ft["y"]))

        pygame.display.flip()
        clock.tick(FPS)
        # Yield to event loop for pygbag WebAssembly compatibility
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
