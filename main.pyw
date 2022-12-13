# Written by Younès B. and Curtis Newton
# December 2022
import math

try: import pygame as pg, random
except ImportError: raise SystemExit("Sorry, can´t find required libraries.")

pg.init()
pg.display.init()
pg.font.init()
pg.mixer.init()


class App:
    def __init__(self) -> None:

        self.bg = pg.image.load("assets/bg.png")
        self.screen = pg.display.set_mode(self.bg.get_size())
        pg.display.set_caption("PyQuiz")
        pg.display.set_icon(pg.transform.scale(pg.image.load("assets/icon.png"), (32 * 1.5, 32 * 1.5)))

        self.margin, self.writing = 20, True
        self.credits, self.question = "Written by Younès B., and Curtis Newton, 2022", "Press Space Key to start."
        self.font = pg.font.Font("assets/dialog_font.ttf", 25)
        self.clock = pg.time.Clock()
        self.result = None

        self.buttons = Buttons(self.screen)

        self.run()

    def choose_randomly_question(self) -> None:
        if random.randint(0, 1): self.question = random.choice(open("assets/yes.txt", "r").readlines())
        else: self.question = random.choice(open("assets/no.txt", "r").readlines())

    def make_typing_effect(self) -> None:
        self.char_x_pos = 0
        for letter in self.question:
            self.screen.blit(self.font.render(letter, 0, pg.Color("black")), (self.char_x_pos, self.margin * 3.5))
            pg.display.flip()
            self.clock.tick(25)
            self.char_x_pos += self.margin

    def make_typing_effect_for_credits(self, timelaps: bool) -> None:
        self.char_x_pos = 0
        for letter in self.credits:
            self.screen.blit(self.font.render(letter, 0, pg.Color("black")), (self.char_x_pos, self.margin))
            pg.display.flip()
            if timelaps: self.clock.tick(25)
            self.char_x_pos += self.margin

    def draw_background(self) -> None: self.screen.blit(self.bg, (0, 0))

    def new_question(self) -> None:
        self.make_typing_effect_for_credits(False)
        self.choose_randomly_question()
        self.make_typing_effect()
        self.writing = False

    def display_result(self, value: bool) -> None:
        if value: self.result = self.font.render("Good job ! Press Space Key to continue.", 0, pg.Color("black"))
        else: self.result = self.font.render("Your answer is wrong. Press Space Key to continue.", 0, pg.Color("black"))

        self.draw_background()
        self.make_typing_effect_for_credits(False)
        self.screen.blit(self.result, (self.screen.get_width() / 2 - self.result.get_width() / 2, self.screen.get_height() / 2 - self.result.get_height() / 2))
        pg.display.flip()

        running = True
        while running:
            for evt in pg.event.get():
                if evt.type == pg.QUIT or evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE: self.quit()
                elif evt.type == pg.KEYDOWN and evt.key == pg.K_SPACE: running = False


    def play_game_music(self) -> None:
        music = pg.mixer.music.load("assets/music.wav")
        pg.mixer.music.play(-1, 0.0, 0)

    def wait_for_start(self) -> None:
        self.play_game_music()
        self.draw_background()
        self.make_typing_effect_for_credits(True)
        self.make_typing_effect()

        running = True
        while running:
            for evt in pg.event.get():
                if evt.type == pg.QUIT or evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE: self.quit()
                elif evt.type == pg.KEYDOWN and evt.key == pg.K_SPACE: running = False

        self.draw_background()


    def run(self) -> None:
        self.wait_for_start()
        self.new_question()

        while True:

            self.buttons.draw()
            pg.display.flip()

            for evt in pg.event.get():
                if evt.type == pg.QUIT or evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE:
                    self.quit()
                elif evt.type == pg.MOUSEBUTTONDOWN and not self.writing:
                    mouse = pg.mouse.get_pos()
                    if self.buttons.yes.collidepoint(evt.pos) and self.question in open("assets/yes.txt").readlines():
                        self.display_result(True)
                        self.draw_background()
                        self.new_question()
                    elif self.buttons.no.collidepoint(evt.pos) and self.question in open("assets/no.txt").readlines():
                        self.display_result(True)
                        self.draw_background()
                        self.new_question()
                    elif self.buttons.yes.collidepoint(evt.pos) and self.question not in open("assets/yes.txt").readlines():
                        self.display_result(False)
                        self.draw_background()
                        self.new_question()
                    elif self.buttons.no.collidepoint(evt.pos) and self.question not in open("assets/no.txt").readlines():
                        self.display_result(False)
                        self.draw_background()
                        self.new_question()


    def quit(self) -> None:
        pg.quit()
        quit()


class Buttons:
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen
        self.font = pg.font.Font("assets/dialog_font.ttf", 25)
        self.yes = pg.Rect(self.screen.get_width() / 4, self.screen.get_height() / 2 + 15, 100, 50)
        self.no = pg.Rect(self.screen.get_width() / 4 * 3, self.screen.get_height() / 2 + 25, 100, 50)

        self.text = None

    def draw(self) -> None:
        pg.draw.rect(self.screen, pg.Color("green"), self.yes)
        self.text = self.font.render("True", 0, pg.Color("black"))
        self.screen.blit(self.text, self.yes)

        pg.draw.rect(self.screen, pg.Color("red"), self.no)
        self.text = self.font.render("False", 0, pg.Color("black"))
        self.screen.blit(self.text, self.no)

if __name__ == "__main__": app = App()