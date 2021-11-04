import tkinter
import sys

from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTkButton(tkinter.Frame):
    """ tkinter custom button with border, rounded corners and hover effect """

    def __init__(self,
                 bg_color=None,
                 fg_color=CTkColorManager.MAIN,
                 hover_color=CTkColorManager.MAIN_HOVER,
                 border_color=None,
                 border_width=0,
                 command=None,
                 width=120,
                 height=32,
                 corner_radius=8,
                 text_font=None,
                 text_color=CTkColorManager.TEXT,
                 text="CTkButton",
                 hover=True,
                 image=None,
                 state=tkinter.NORMAL,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        AppearanceModeTracker.add(self.set_appearance_mode)

        self.gridConfigure()

        if bg_color is None:
            if isinstance(self.master, CTkFrame):
                self.bg_color = self.master.fg_color
            else:
                self.bg_color = self.master.cget("bg")
        else:
            self.bg_color = bg_color

        self.fg_color = self.bg_color if fg_color is None else fg_color
        self.hover_color = self.bg_color if hover_color is None else hover_color

        self.fg_color = self.bg_color if self.fg_color is None else self.fg_color

        self.border_color = border_color
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.width = width
        self.height = height

        if corner_radius * 2 > self.height:
            self.corner_radius = self.height / 2
        elif corner_radius * 2 > self.width:
            self.corner_radius = self.width / 2
        else:
            self.corner_radius = corner_radius

        self.border_width = border_width

        if self.corner_radius >= self.border_width:
            self.inner_corner_radius = self.corner_radius - self.border_width
        else:
            self.inner_corner_radius = 0

        self.text = text
        self.text_color = text_color
        if text_font is None:
            if sys.platform == "darwin":  # macOS
                self.text_font = ("Avenir", 13)
            elif "win" in sys.platform:  # Windows
                self.text_font = ("Century Gothic", 11)
            else:
                self.text_font = ("TkDefaultFont")
        else:
            self.text_font = text_font

        self.function = command
        self.state = state
        self.hover = hover
        self.image = image

        self.configure(width=self.width, height=self.height)

        if sys.platform == "darwin" and self.function is not None:
            self.configure(cursor="pointinghand")

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     width=self.width,
                                     height=self.height)
        self.canvas.grid(row=0, column=0)

        if self.hover is True:
            self.canvas.bind("<Enter>", self.on_enter)
            self.canvas.bind("<Leave>", self.on_leave)

        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<Button-1>", self.clicked)

        self.canvas_fg_parts = []
        self.canvas_border_parts = []
        self.text_label = None
        self.image_label = None

        # Each time an item is resized due to pack position mode, the binding Configure is called on the widget
        self.bind('<Configure>', self.updateDimensions)
        self.draw()

    def gridConfigure(self):
        # Configuration of a basic grid  in which all elements of CTkButtons are centered on one row and one column
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def updateDimensions(self, event):
        # We update the dimensions of the internal elements of CTkButton Widget
        self.canvas.config(width=event.width, height=event.height)
        self.width = event.width
        self.height = event.height
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.canvas_fg_parts = []
        self.canvas_border_parts = []

        if type(self.bg_color) == tuple and len(self.bg_color) == 2:
            self.canvas.configure(bg=self.bg_color[self.appearance_mode])
        else:
            self.canvas.configure(bg=self.bg_color)

        # border button parts
        if self.border_width > 0:

            if self.corner_radius > 0:
                self.canvas_border_parts.append(self.canvas.create_oval(0,
                                                                        0,
                                                                        self.corner_radius * 2,
                                                                        self.corner_radius * 2))
                self.canvas_border_parts.append(self.canvas.create_oval(self.width - self.corner_radius * 2,
                                                                        0,
                                                                        self.width,
                                                                        self.corner_radius * 2))
                self.canvas_border_parts.append(self.canvas.create_oval(0,
                                                                        self.height - self.corner_radius * 2,
                                                                        self.corner_radius * 2,
                                                                        self.height))
                self.canvas_border_parts.append(self.canvas.create_oval(self.width - self.corner_radius * 2,
                                                                        self.height - self.corner_radius * 2,
                                                                        self.width,
                                                                        self.height))

            self.canvas_border_parts.append(self.canvas.create_rectangle(0,
                                                                         self.corner_radius,
                                                                         self.width,
                                                                         self.height - self.corner_radius))
            self.canvas_border_parts.append(self.canvas.create_rectangle(self.corner_radius,
                                                                         0,
                                                                         self.width - self.corner_radius,
                                                                         self.height))

        # inner button parts

        if self.corner_radius > 0:
            self.canvas_fg_parts.append(self.canvas.create_oval(self.border_width,
                                                                self.border_width,
                                                                self.border_width + self.inner_corner_radius * 2,
                                                                self.border_width + self.inner_corner_radius * 2))
            self.canvas_fg_parts.append(self.canvas.create_oval(self.width - self.border_width - self.inner_corner_radius * 2,
                                                                self.border_width,
                                                                self.width - self.border_width,
                                                                self.border_width + self.inner_corner_radius * 2))
            self.canvas_fg_parts.append(self.canvas.create_oval(self.border_width,
                                                                self.height - self.border_width - self.inner_corner_radius * 2,
                                                                self.border_width + self.inner_corner_radius * 2,
                                                                self.height-self.border_width))
            self.canvas_fg_parts.append(self.canvas.create_oval(self.width - self.border_width - self.inner_corner_radius * 2,
                                                                self.height - self.border_width - self.inner_corner_radius * 2,
                                                                self.width - self.border_width,
                                                                self.height - self.border_width))

        self.canvas_fg_parts.append(self.canvas.create_rectangle(self.border_width + self.inner_corner_radius,
                                                                 self.border_width,
                                                                 self.width - self.border_width - self.inner_corner_radius,
                                                                 self.height - self.border_width))
        self.canvas_fg_parts.append(self.canvas.create_rectangle(self.border_width,
                                                                 self.border_width + self.inner_corner_radius,
                                                                 self.width - self.border_width,
                                                                 self.height - self.inner_corner_radius - self.border_width))

        for part in self.canvas_fg_parts:
            if type(self.fg_color) == tuple and len(self.fg_color) == 2:
                if self.state == tkinter.DISABLED:
                    self.canvas.itemconfig(part,
                                           fill=CTkColorManager.darken_hex_color(self.fg_color[self.appearance_mode]), width=0)
                else:
                    self.canvas.itemconfig(part, fill=self.fg_color[self.appearance_mode], width=0)
            else:
                if self.state == tkinter.DISABLED:
                    self.canvas.itemconfig(part,
                                           fill=CTkColorManager.darken_hex_color(self.fg_color),
                                           outline=self.fg_color, width=0)
                else:
                    self.canvas.itemconfig(part, fill=self.fg_color, outline=self.fg_color, width=0)

        for part in self.canvas_border_parts:
            if type(self.border_color) == tuple and len(self.border_color) == 2:
                self.canvas.itemconfig(part, fill=self.border_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=self.border_color, outline=self.border_color, width=0)

        # no image provided
        if self.image is None:
            self.text_label = tkinter.Label(master=self,
                                            text=self.text,
                                            font=self.text_font)
            self.text_label.grid(row=0, column=0)

            self.text_label.bind("<Enter>", self.on_enter)
            self.text_label.bind("<Leave>", self.on_leave)

            self.text_label.bind("<Button-1>", self.clicked)
            self.text_label.bind("<Button-1>", self.clicked)

            if type(self.text_color) == tuple and len(self.text_color) == 2:
                self.text_label.configure(fg=self.text_color[self.appearance_mode])
            else:
                self.text_label.configure(fg=self.text_color)

            if type(self.fg_color) == tuple and len(self.fg_color) == 2:
                if self.state == tkinter.DISABLED:
                    self.text_label.configure(bg=CTkColorManager.darken_hex_color(self.fg_color[self.appearance_mode]))
                else:
                    self.text_label.configure(bg=self.fg_color[self.appearance_mode])
            else:
                if self.state == tkinter.DISABLED:
                    self.text_label.configure(bg=CTkColorManager.darken_hex_color(self.fg_color))
                else:
                    self.text_label.configure(bg=self.fg_color)

            self.set_text(self.text)

        # use image for button
        else:
            self.image_label = tkinter.Label(master=self,
                                             image=self.image)
            self.image_label.grid(row=0, column=0)

            self.image_label.bind("<Enter>", self.on_enter)
            self.image_label.bind("<Leave>", self.on_leave)

            self.image_label.bind("<Button-1>", self.clicked)
            self.image_label.bind("<Button-1>", self.clicked)

            if type(self.fg_color) == tuple and len(self.fg_color) == 2:
                if self.state == tkinter.DISABLED:
                    self.image_label.configure(bg=CTkColorManager.darken_hex_color(self.fg_color[self.appearance_mode]))
                else:
                    self.image_label.configure(bg=self.fg_color[self.appearance_mode])
            else:
                if self.state == tkinter.DISABLED:
                    self.image_label.configure(bg=CTkColorManager.darken_hex_color(self.fg_color))
                else:
                    self.image_label.configure(bg=self.fg_color)

    def configure_color(self, bg_color=None, fg_color=None, hover_color=None, text_color=None):
        if bg_color is not None:
            self.bg_color = bg_color
        else:
            self.bg_color = self.master.cget("bg")

        if fg_color is not None:
            self.fg_color = fg_color

        if hover_color is not None:
            self.hover_color = hover_color

        if text_color is not None:
            self.text_color = text_color

        self.draw()

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        if "text" in kwargs:
            self.set_text(kwargs["text"])
            del kwargs["text"]

        if "state" in kwargs:
            self.set_state(kwargs["state"])
            del kwargs["state"]

        super().configure(*args, **kwargs)

    def set_state(self, state):
        self.state = state

        if self.state == tkinter.DISABLED:
            self.hover = False
            if sys.platform == "darwin" and self.function is not None:
                self.configure(cursor="arrow")

        elif self.state == tkinter.NORMAL:
            self.hover = True
            if sys.platform == "darwin" and self.function is not None:
                self.configure(cursor="pointinghand")

        self.draw()

    def set_text(self, text):
        self.text = text
        if self.text_label is not None:
            self.text_label.configure(text=self.text)  #, width=len(self.text))
        else:
            sys.stderr.write("ERROR (CTkButton): Cant change text because button has no text.")

    def change_image(self, image):
        if self.image_label is not None:
            self.image = image
            self.image_label.configure(image=self.image)
        else:
            sys.stderr.write("ERROR (CTkButton): Cant change image because button has no image.")

    def on_enter(self, event=0):
        if self.hover is True:
            for part in self.canvas_fg_parts:
                if type(self.hover_color) == tuple and len(self.hover_color) == 2:
                    self.canvas.itemconfig(part, fill=self.hover_color[self.appearance_mode], width=0)
                else:
                    self.canvas.itemconfig(part, fill=self.hover_color, width=0)

            if self.text_label is not None:
                if type(self.hover_color) == tuple and len(self.hover_color) == 2:
                    self.text_label.configure(bg=self.hover_color[self.appearance_mode])
                else:
                    self.text_label.configure(bg=self.hover_color)

            if self.image_label is not None:
                if type(self.hover_color) == tuple and len(self.hover_color) == 2:
                    self.image_label.configure(bg=self.hover_color[self.appearance_mode])
                else:
                    self.image_label.configure(bg=self.hover_color)

    def on_leave(self, event=0):
        if self.hover is True:
            for part in self.canvas_fg_parts:
                if type(self.fg_color) == tuple and len(self.fg_color) == 2:
                    self.canvas.itemconfig(part, fill=self.fg_color[self.appearance_mode], width=0)
                else:
                    self.canvas.itemconfig(part, fill=self.fg_color, width=0)

            if self.text_label is not None:
                if type(self.fg_color) == tuple and len(self.fg_color) == 2:
                    self.text_label.configure(bg=self.fg_color[self.appearance_mode])
                else:
                    self.text_label.configure(bg=self.fg_color)

            if self.image_label is not None:
                if type(self.fg_color) == tuple and len(self.fg_color) == 2:
                    self.image_label.configure(bg=self.fg_color[self.appearance_mode])
                else:
                    self.image_label.configure(bg=self.fg_color)

    def clicked(self, event=0):
        if self.function is not None:
            if self.state is not tkinter.DISABLED:
                self.function()
                self.on_leave()

    def set_appearance_mode(self, mode_string):
        if mode_string.lower() == "dark":
            self.appearance_mode = 1
        elif mode_string.lower() == "light":
            self.appearance_mode = 0

        self.draw()
