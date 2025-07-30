"""
调用：soup3D.ui
soup3D的ui子库，用于绘制2D图形，可绘制HUD叠加显示、GUI用户界面等。
"""
from OpenGL.GL import *
from OpenGL.GLU import *
from math import*
from PIL import Image

import soup3D.shader

render_queue : list[tuple["Shape", float, float]] = []  # 全局渲染队列


class Shape:
    def __init__(self, shape_type,
                 texture: soup3D.shader.Texture | soup3D.shader.MixChannel,
                 vertex: list | tuple):
        """
        图形，可以批量生成线段、三角形
        :param shape_type: 绘制方式，可以填写这些内容：
                           "line_b": 不相连线段
                           "line_s": 连续线段
                           "line_l": 头尾相连的连续线段
                           "triangle_b": 不相连三角形
                           "triangle_s": 相连三角形
                           "triangle_l": 头尾相连的连续三角形
        :param texture:    使用的纹理对象，默认为None
        :param vertex:     图形中所有的端点，每个参数的格式为：(x, y, u, v)
        """
        type_menu = {
            "line_b": GL_LINES,
            "line_s": GL_LINE_STRIP,
            "line_l": GL_LINE_LOOP,
            "triangle_b": GL_TRIANGLES,
            "triangle_s": GL_TRIANGLE_STRIP,
            "triangle_l": GL_TRIANGLE_FAN
        }
        if shape_type not in type_menu:
            raise TypeError(f"unknown type: {shape_type}")
        self.type = shape_type
        self.texture = texture
        self.vertex = vertex
        self.display_list = None
        self.tex_id = _pil_to_texture(self.texture.pil_pic)

    def _setup_projection(self) -> None:
        """设置正交投影"""
        viewport = glGetIntegerv(GL_VIEWPORT)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, viewport[2], viewport[3], 0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

    def _restore_projection(self) -> None:
        """恢复投影矩阵"""
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def paint(self, x : float, y : float) -> None:
        """在单帧渲染该图形"""
        global render_queue
        render_queue.append((self, x, y))


class Group:
    def __init__(self, *arg: Shape, origin : tuple[float, float]=(0.0, 0.0)):
        """
        图形组
        :param arg:    组中所有的图形
        :param origin: 图形组在屏幕中的位置
        """
        self.shapes = list(arg)
        self.origin = list(origin)

    def goto(self, x : float, y : float) -> None:
        """设置绝对位置"""
        self.origin[0] = x
        self.origin[1] = y

    def move(self, x : float, y : float) -> None:
        """相对移动"""
        self.origin[0] += x
        self.origin[1] += y

    def display(self) -> None:
        """单帧显示"""
        for shape in self.shapes:
            shape.paint(*self.origin)


def _pil_to_texture(pil_img: Image.Image, texture_id: int | None = None, texture_unit: int = 0) -> int:
    """
    将PIL图像转换为OpenGL纹理
    :param pil_img: PIL图像对象
    :param texture_id: 已有纹理ID（如None则创建新纹理）
    :param texture_unit: 纹理单元编号（0表示GL_TEXTURE0，1表示GL_TEXTURE1等）
    :return: 纹理ID
    """
    # 激活指定纹理单元
    glActiveTexture(GL_TEXTURE0 + texture_unit)

    # 确定图像模式并转换为RGBA格式
    mode = pil_img.mode
    if mode == '1':  # 黑白图像
        pil_img = pil_img.convert('RGBA')
        data = pil_img.tobytes('raw', 'RGBA', 0, -1)
    elif mode == 'L':  # 灰度图像
        pil_img = pil_img.convert('RGBA')
        data = pil_img.tobytes('raw', 'RGBA', 0, -1)
    elif mode == 'RGB':  # RGB图像
        pil_img = pil_img.convert('RGBA')
        data = pil_img.tobytes('raw', 'RGBA', 0, -1)
    elif mode == 'RGBA':  # RGBA图像
        data = pil_img.tobytes('raw', 'RGBA', 0, -1)
    else:
        # 其他格式转换为RGBA
        pil_img = pil_img.convert('RGBA')
        data = pil_img.tobytes('raw', 'RGBA', 0, -1)

    # 获取图像尺寸
    width, height = pil_img.size

    # 创建或绑定纹理
    if texture_id is None:
        texture_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture_id)

    # 设置纹理参数
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

    # 上传纹理数据
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

    # 生成mipmap（提高纹理在远距离的渲染质量）
    glGenerateMipmap(GL_TEXTURE_2D)

    return texture_id
