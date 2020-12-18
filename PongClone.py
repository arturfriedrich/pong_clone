import arcade


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title,)
        self.center_window()

        self.batch = arcade.ShapeElementList()

        # start screen colors
        self.player1_color, self.player2_color = arcade.color.BLACK, arcade.color.BLACK
        self.ball_color = arcade.color.BLACK
        self.score_display_player1_color, self.score_display_player2_color = arcade.color.BLACK, arcade.color.BLACK

        self.start_color = arcade.color.WHITE
        self.start_screen_x = 640

        # ball starting positions
        self.ball_x = 640
        self.ball_y = 480

        # ball speed
        self.ball_speed_x, self.ball_speed_y = 1, 1

        # player speed
        self.player1_speed, self.player2_speed = 600, 600

        # player starting positions
        self.player1_x, self.player2_x = 100, 1280 - 100
        self.player1_y, self.player2_y = 480, 480

        # score display position
        self.score_display_player1_x = 550
        self.score_display_player1_y = 800

        self.score_display_player2_x = 680
        self.score_display_player2_y = 800

        # moving
        self.up_player1 = False
        self.down_player1 = False

        self.up_player2 = False
        self.down_player2 = False

        # scores
        self.player1_score = 0
        self.player2_score = 0

        # start screen space
        self.space = 0

        # sounds
        self.bounce_sound = arcade.load_sound("bounce.ogg")
        self.collision_sound = arcade.load_sound("collision.ogg")
        self.point_sound = arcade.load_sound("point.ogg")

    def on_draw(self):
        arcade.start_render()
        # player rectangles
        arcade.draw_rectangle_filled(self.player1_x, self.player1_y, 20, 150, self.player1_color)
        arcade.draw_rectangle_filled(self.player2_x, self.player2_y, 20, 150, self.player2_color)

        # ball
        arcade.draw_rectangle_filled(self.ball_x, self.ball_y, 20, 20, self.ball_color)

        #  visible borders
        arcade.draw_rectangle_filled(640, 960 - 25 / 2, 1280, 25, arcade.color.GRAY)
        arcade.draw_rectangle_filled(640, 0 + 25 / 2, 1280, 25, arcade.color.GRAY)

        # score display
        arcade.draw_text(str(self.player1_score), self.score_display_player1_x, self.score_display_player1_y,
                         self.score_display_player1_color, font_size=72, font_name="connection.otf", anchor_x="center", anchor_y="center")
        arcade.draw_text(str(self.player2_score), self.score_display_player2_x, self.score_display_player2_y,
                         self.score_display_player2_color, font_size=72, font_name="connection.otf", anchor_x="center", anchor_y="center")

        # win text display
        if self.player1_score >= 7:
            arcade.draw_text("PLAYER 1 WON!", 640, 460, arcade.color.WHITE, font_size=60, font_name="connection.otf", anchor_x="center", anchor_y="center")

            # clear the players
            self.player1_x = 0 - 100
            self.player2_x = 0 - 100

            # clear the ball
            self.ball_color = arcade.color.BLACK
            self.ball_speed_x, self.ball_speed_y = 0.1, 0.1

            # clear the score display
            self.score_display_player1_x = 0 - 200
            self.score_display_player2_x = 0 - 200

        if self.player2_score >= 7:
            arcade.draw_text("PLAYER 2 WON!", 640, 460, arcade.color.WHITE, font_size=60, font_name="connection.otf", anchor_x="center", anchor_y="center")

            # clear the players
            self.player1_x = 0 - 100
            self.player2_x = 0 - 100

            # clear the ball
            self.ball_color = arcade.color.BLACK
            self.ball_speed_x, self.ball_speed_y = 0.1, 0.1

            # clear the score display
            self.score_display_player1_x = 0 - 200
            self.score_display_player2_x = 0 - 200

        arcade.draw_text("Press SPACE to start!", self.start_screen_x, 460, self.start_color, font_size=60, font_name="connection.otf", anchor_x="center", anchor_y="center")
        if self.space == 1:
            self.player1_color, self.player2_color = arcade.color.WHITE, arcade.color.WHITE

            self.ball_color = arcade.color.WHITE

            self.score_display_player1_color, self.score_display_player2_color = arcade.color.WHITE, arcade.color.WHITE

            self.start_color = arcade.color.BLACK

            self.player1_score, self.player2_score = 0, 0

            self.ball_x, self.ball_y = 640, 480

            self.space = 0

            self.start_screen_x = 0 - 1000

            self.ball_speed_x, self.ball_speed_y = 300, 420

    def on_update(self, delta_time: float):
        # ball move
        self.ball_x += self.ball_speed_x * delta_time
        self.ball_y += self.ball_speed_y * delta_time

        # ball bouncing
        if self.ball_y > 960 - 35:
            self.ball_y = 960 - 35
            self.ball_speed_y *= -1
            arcade.play_sound(self.bounce_sound)
        if self.ball_y < 0 + 35:
            self.ball_y = 0 + 35
            self.ball_speed_y *= -1
            arcade.play_sound(self.bounce_sound)

        # player stops at the top and the bottom of the screen

        # player 1 moving
        if self.up_player1:
            self.player1_y += self.player1_speed * delta_time
        if self.down_player1:
            self.player1_y -= self.player1_speed * delta_time

        # player 2 moving
        if self.up_player2:
            self.player2_y += self.player2_speed * delta_time
        if self.down_player2:
            self.player2_y -= self.player2_speed * delta_time

        # player 1 scores
        if self.ball_x > 1280:
            self.player1_score += 1
            # print(self.player1_score)
            self.ball_x = 640
            self.ball_y = 480
            self.ball_speed_x *= -1
            arcade.play_sound(self.point_sound)

        # player 2 scores
        if self.ball_x < 0:
            self.player2_score += 1
            # print(self.player2_score)
            self.ball_x = 640
            self.ball_y = 480
            self.ball_speed_x *= -1
            arcade.play_sound(self.point_sound)

        # collision between the player 1 and the ball
        if 105 < self.ball_x < 110:
            if self.player1_y - 75 < self.ball_y < self.player1_y + 75:
                self.ball_speed_x *= -1
                arcade.play_sound(self.collision_sound)
                # print("Collision")

        # collision between the player 2 and the ball
        if 1170 < self.ball_x < 1175:
            if self.player2_y - 75 < self.ball_y < self.player2_y + 75:
                self.ball_speed_x *= -1
                arcade.play_sound(self.collision_sound)
                # print("Collision")

        # player collision with border
        if self.player1_y > 960 - 75 - 25:
            self.player1_speed = 1
            if self.down_player1:
                self.player1_speed = 600
        if self.player1_y < 0 + 75 + 25:
            self.player1_speed = 1
            if self.up_player1:
                self.player1_speed = 600

        if self.player2_y > 960 - 75 - 25:
            self.player2_speed = 1
            if self.down_player2:
                self.player2_speed = 600
        if self.player2_y < 0 + 75 + 25:
            self.player2_speed = 1
            if self.up_player2:
                self.player2_speed = 600

    def on_key_press(self, symbol: int, modifiers: int):
        # player 1 control
        if symbol == arcade.key.W:
            self.up_player1 = True
        if symbol == arcade.key.S:
            self.down_player1 = True

        # player 2 control
        if symbol == arcade.key.UP:
            self.up_player2 = True
        if symbol == arcade.key.DOWN:
            self.down_player2 = True

        # start
        if symbol == arcade.key.SPACE:
            self.space = 1

    def on_key_release(self, symbol: int, modifiers: int):
        # player 1 control
        if symbol == arcade.key.W:
            self.up_player1 = False
        if symbol == arcade.key.S:
            self.down_player1 = False

        # player 2 control
        if symbol == arcade.key.UP:
            self.up_player2 = False
        if symbol == arcade.key.DOWN:
            self.down_player2 = False


def main():
    win = GameWindow(1280, 960, "Pong")
    arcade.run()


main()
