import pygame

class Event:
    def __init__(self, type: str, args : dict) -> None:
        self.type : str = type;

class WindowCloseEvent(Event):
    def __init__(self, args : dict) -> None:
        super().__init__("on_close", args)

class KeyDownEvent(Event):
    unicode: str | None
    key: int | None
    mod: int | None
    scancode: int | None
    window: pygame.Surface | None

    def __init__(self, args : dict) -> None:
        super().__init__("key_down", args)
        self.unicode = args.get("unicode")
        self.key = args.get("key")
        self.mod = args.get("mod")
        self.scancode = args.get("scancode")
        self.window = args.get("window")

class KeyUpEvent(Event):
    unicode: str | None
    key: int | None
    mod: int | None
    scancode: int | None
    window: pygame.Surface | None

    def __init__(self, args : dict) -> None:
        super().__init__("key_up", args)
        self.unicode = args.get("unicode")
        self.key = args.get("key")
        self.mod = args.get("mod")
        self.scancode = args.get("scancode")
        self.window = args.get("window")

class MouseDownEvent(Event):
    pos : tuple[int, int] | None
    button : int | None
    window: pygame.Surface | None

    def __init__(self, args : dict) -> None:
        super().__init__("mouse_down", args)
        self.pos = args.get("pos")
        self.button = args.get("button")
        self.window = args.get("window") 

class MouseUpEvent(Event):
    pos : tuple[int, int] | None
    button : int | None
    window: pygame.Surface | None

    def __init__(self, args : dict) -> None:
        super().__init__("mouse_up", args)
        self.pos = args.get("pos")
        self.button = args.get("button")
        self.window = args.get("window") 

class MouseMoveEvent(Event):
    pos : tuple[int, int] | None
    rel : tuple[int, int] | None
    buttons : tuple[int, int, int] | None
    window: pygame.Surface | None

    def __init__(self, args : dict) -> None:
        super().__init__("mouse_move", args)
        self.pos = args.get("pos")
        self.rel = args.get("rel")
        self.buttons = args.get("buttons")
        self.window = args.get("window") 

class MouseWheelEvent(Event):
    x : int | None
    y : int | None
    flipped : bool | None

    def __init__(self, args : dict) -> None:
        super().__init__("mouse_wheel", args)
        self.x = args.get("x")
        self.y = args.get("y")
        self.flipped = args.get("flipped")