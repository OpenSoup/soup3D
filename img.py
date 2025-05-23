"""
调用：soup3D
用于管理材质贴图
"""
from OpenGL.GL import *


class Texture:
    def __init__(self, img, width, height, img_type="rgb", wrap_x="edge", wrap_y="edge", linear=False):
        """
        材质纹理贴图，当图形需要贴图时，在Shape的texture
        赋值该类型

        :param img:    贴图的二进制数据
        :param width:  贴图的宽度（像素）
        :param height: 贴图的高度（像素）
        :param img_type: 图像模式，可为"rgb"或"rgba"
        :param wrap_x: x轴环绕方式，当取色坐标超出图片范
                       围时的取色方案，可为：
                       "repeat" -> 重复图像
                       "mirrored" -> 镜像图像
                       "edge" -> 延生边缘像素
                       "border" -> 纯色图像
        :param wrap_y: y轴环绕方式（参数同wrap_x）
        :param linear: 是否使用抗锯齿，True使用
                       GL_LINEAR插值，False使用
                       GL_NEAREST
        """
        # 转换参数为OpenGL常量
        wrap_map = {
            "repeat": GL_REPEAT,
            "mirrored": GL_MIRRORED_REPEAT,
            "edge": GL_CLAMP_TO_EDGE,
            "border": GL_CLAMP_TO_BORDER
        }

        type_map = {
            "rgb": GL_RGB,
            "rgba": GL_RGBA
        }

        # 生成纹理对象
        self.tex_id = glGenTextures(1)  # 生成纹理ID[6,7](@ref)
        glBindTexture(GL_TEXTURE_2D, self.tex_id)

        # 设置纹理参数
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap_map[wrap_x])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap_map[wrap_y])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                        GL_LINEAR if linear else GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                        GL_LINEAR if linear else GL_NEAREST)

        # 加载纹理数据
        glTexImage2D(GL_TEXTURE_2D, 0, type_map[img_type], width, height,
                     0, type_map[img_type], GL_UNSIGNED_BYTE, img)

        # 记录纹理是否透明（RGBA模式）
        self.transparent = (img_type == "rgba")
