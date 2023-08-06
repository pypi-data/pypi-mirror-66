# ����'numpy'ģ��
try:
    import numpy as np
except ImportError:
    raise Exception("No 'numpy' module found, please install it")
# ����'numpy'ģ��
try:
    from PIL import Image
except ImportError:
    raise Exception("No 'PIL' module found, please install it")


# ���庯��
def change(image_file):
    # ��ͼƬ�ļ�
    image = Image.open(image_file)
    # ��ȡͼƬrect����
    image_width, image_height = image.size
    # ͼƬ�¿��
    width = 200
    # ͼƬ�¸߶�
    height = int(image_height / (image_width / width) / 2)
    # ѹ��ͼƬ
    image = image.resize((width, height), Image.ANTIALIAS)
    # ��ͼƬ�޸�Ϊ�ڰ�ģʽ
    image = image.convert('L')
    # ��ȡͼƬ����ֵ
    pixel = np.array(image)
    # �����ַ���
    str = 'MNHQ$OC?7>!:-;. '
    # �����ַ���
    text = ""
    # ͼƬת�ַ�
    for h in range(height):
        # �����б�
        for w in range(width):
            # ����ַ�
            text += str[pixel[h][w] // 16]
        # ����
        text += '\n'
    # ������ֵ
    return text
