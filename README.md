这是一个基于`OpenGL`和`pygame`开发的3D引擎，易于新手学习，可  
用于3D游戏开发、数据可视化、3D图形的绘制等开发。

## 安装

如果您的`python`环境中包含`pip`，可使用如下代码进行安装：

```bash
pip install -i https://osoup.top/simple soup3D
```

使用该库还需要`OpenGL`和`pygame`，可使用如下代码安装：

```bash
pip install pygame
pip install pyopengl
pip install pillow
```

## 小试牛刀

安装完成后，您可以试试这段代码：

```python
import soup3D
import soup3D.event
import soup3D.shader
from soup3D.events import *
from soup3D.name import *
from math import *
from time import*


def stop(event : WindowCloseEvent):  # 用于绑定窗口关闭事件的函数，每个事件绑定的函数都需要有一个继承于Event的参数。
    global running
    running = False

running = True


if __name__ == '__main__':
    soup3D.init(bg_color=(0.5, 0.75, 1))       # 初始化窗口
    soup3D.event.bind(stop)          # 绑定关闭窗口事件

    green = soup3D.shader.FPL(soup3D.shader.MixChannel((1, 1), 0, 1, 0))  # 创建绿色材质
    face = soup3D.Face(TRIANGLE_B, green, [                               # 创建面
        (0, 0, 0, 0, 0),  # (R, G, B, U, V)
        (100, 0, 0, 0, 0),
        (0, 100, 0, 0, 0)
    ])

    triangle = soup3D.Model(0, 0, -500, face)  # 将面加入模型
    triangle.show()                            # 显示模型
    while running:  # 主循环
        soup3D.update()  # 更新画面
```

这段代码运行后，您可以看到一个绿色三角形在窗口中

## 更多内容

该库还有很多的方法供您使用，更多内容可参阅[帮助文档](./help.md)
