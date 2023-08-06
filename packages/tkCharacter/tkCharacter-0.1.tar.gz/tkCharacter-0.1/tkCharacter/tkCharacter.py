from tkinter import PhotoImage


class TkCharacter:
    # added variables
    DOWN_ANIMATION = ["0", "1", "2"]
    LEFT_ANIMATION = ["3", "4", "5"]
    RIGHT_ANIMATION = ["6", "7", "8"]
    UP_ANIMATION = ["9", "10", "11"]
    STANCE_ANIMATION = ["0", "13", "14"]
    animation_number = 0

    def __init__(self, canvas, x, y, directory, **kwargs):
        self.sprite = PhotoImage(file=directory + r"\0.png")
        self.canvas_sprite = canvas.create_image(x, y, image=self.sprite)
        self.canvas = canvas
        self.image_dir = directory
        self.speed = 10

        print(kwargs)
        if "left" in kwargs.keys():
            self.LEFT_ANIMATION = kwargs["left"]
        if "right" in kwargs.keys():
            self.RIGHT_ANIMATION = kwargs["right"]
        if "down" in kwargs.keys():
            self.DOWN_ANIMATION = kwargs["down"]
        if "up" in kwargs.keys():
            self.UP_ANIMATION = kwargs["up"]
        if "speed" in kwargs.keys():
            self.speed = kwargs["speed"]

    def move(self, direction):
        if direction == "left":
            self.canvas.move(self.canvas_sprite, -self.speed, 0)
        elif direction == "right":
            self.canvas.move(self.canvas_sprite, self.speed, 0)
        elif direction == "up":
            self.canvas.move(self.canvas_sprite, 0, -self.speed)
        elif direction == "down":
            self.canvas.move(self.canvas_sprite, 0, self.speed)
        self.animate(direction)

    def pos(self):
        return self.canvas.coords(self.canvas_sprite)

    # added function
    def animate(self, direction):
        current_animation = self.STANCE_ANIMATION
        if direction == "up":
            current_animation = self.UP_ANIMATION
        elif direction == "down":
            current_animation = self.DOWN_ANIMATION
        elif direction == "left":
            current_animation = self.LEFT_ANIMATION
        elif direction == "right":
            current_animation = self.RIGHT_ANIMATION

        self.sprite = PhotoImage(file=self.image_dir + r'\\' + current_animation[self.animation_number] + ".png")
        self.animation_number = (self.animation_number + 1) % len(current_animation)

        self.canvas.itemconfig(self.canvas_sprite, image=self.sprite)
