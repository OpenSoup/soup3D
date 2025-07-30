"""
调用：soup3D.event
事件处理方法库，可添加如鼠标、键盘等事件的处理方式
"""

import inspect
import typing
import pygame
from pygame.locals import *
from soup3D.events import *

__all__ : list[str] = [
    "bind", "check_event"
]

event_menu : dict[type, int] = {
    WindowCloseEvent: pygame.QUIT,
    KeyDownEvent: pygame.KEYDOWN,
    KeyUpEvent: pygame.KEYUP,
    MouseDownEvent: pygame.MOUSEBUTTONDOWN,
    MouseUpEvent: pygame.MOUSEBUTTONUP,
    MouseMoveEvent: pygame.MOUSEMOTION,
    MouseWheelEvent: pygame.MOUSEWHEEL
}

bind_event_dic: dict[int, tuple[typing.Callable[..., None], type]] = {}
T = typing.TypeVar('T', bound=Event, contravariant=True)

def bind(funk : typing.Callable[[T], None]) -> None:
    """
    事件绑定函数
    :param event: 事件名称
    :param funk:  绑定的函数，每个事件只能绑定一个函数，函数
                  需要有1个参数
    :return: None
    """

    sig = inspect.signature(funk)
    first_param = next(iter(sig.parameters.values()))
    ann = first_param.annotation
    if (ann is inspect._empty):
        raise TypeError(f"{funk.__name__} is missing a type annotation for the first parameter")
    
    if not isinstance(ann, type):
        raise TypeError(f"The annotation of {funk.__name__} is not a type: {ann}")

    if not issubclass(ann, Event):
        raise TypeError(f"The first parameter type of {funk.__name__} must be a subclass of {Event.__name__}, but got {ann.__name__}")
    bind_event_dic[event_menu[ann]] = (funk, ann)


def check_event(events: list[pygame.event.Event]) -> None:
    for event in events:
        if event.type in bind_event_dic:
            funk, event_cls = bind_event_dic[event.type]
            event_instance = event_cls(args=event.dict)
            funk(event_instance)
