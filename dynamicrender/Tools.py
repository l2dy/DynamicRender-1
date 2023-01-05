from PIL import Image
import numpy as np


async def merge_pictures(pic_list:list) -> Image.Image:
    img_list = [i for i in pic_list if i is not None]
    temp = np.array(Image.new("RGBA",(1080,0),(255,255,255)))
    for i in img_list:
        temp = np.concatenate((temp,np.array(i)))
    return Image.fromarray(temp)

