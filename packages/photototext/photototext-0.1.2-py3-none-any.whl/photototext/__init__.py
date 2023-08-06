# 导入'numpy'模块
try:
    import numpy as np
except ImportError:
    raise Exception("No 'numpy' module found, please install it")
# 导入'numpy'模块
try:
    from PIL import Image
except ImportError:
    raise Exception("No 'PIL' module found, please install it")


# 定义函数
def change(image_file):
    # 打开图片文件
    image = Image.open(image_file)
    # 获取图片rect属性
    image_width, image_height = image.size
    # 图片新宽度
    width = 200
    # 图片新高度
    height = int(image_height / (image_width / width) / 2)
    # 压缩图片
    image = image.resize((width, height), Image.ANTIALIAS)
    # 将图片修改为黑白模式
    image = image.convert('L')
    # 获取图片像素值
    pixel = np.array(image)
    # 创建字符组
    str = 'MNHQ$OC?7>!:-;. '
    # 创建字符串
    text = ""
    # 图片转字符
    for h in range(height):
        # 遍历列表
        for w in range(width):
            # 添加字符
            text += str[pixel[h][w] // 16]
        # 换行
        text += '\n'
    # 返回数值
    return text
