"""
调用：soup3D
命名空间
"""

# shape_type
LINE_B = "line_b"          # 不相连线段
LINE_S = "line_s"          # 连续线段
LINE_L = "line_l"          # 头尾相连的连续线段
TRIANGLE_B = "triangle_b"  # 不相连三角形
TRIANGLE_S = "triangle_s"  # 相连三角形
TRIANGLE_L = "triangle_l"  # 头尾相连的连续三角形

# light_type
POINT = "point"    # 点光源
DIRECT = "direct"  # 方向光源

# img_type
RGB = "rgb"    # 红、绿、蓝通道
RGBA = "rgba"  # 红、绿、蓝、不透明度通道

# wrap
REPEAT = "repeat"      # 超出边缘后重复
MIRRORED = "mirrored"  # 超出边缘后镜像
EDGE = "edge"          # 超出边缘后延伸边缘颜色
BORDER = "border"      # 超出边缘后