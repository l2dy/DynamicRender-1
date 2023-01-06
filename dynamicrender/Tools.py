import asyncio

from PIL import Image, ImageDraw
import numpy as np
from typing import Optional, Union
import httpx
from loguru import logger
from io import BytesIO


async def merge_pictures(pic_list: list) -> Image.Image:
    img_list = [i for i in pic_list if i is not None]
    temp = np.array(Image.new("RGBA", (1080, 0), (255, 255, 255)))
    for i in img_list:
        temp = np.concatenate((temp, np.array(i)))
    return Image.fromarray(temp)


async def circle_picture(img: Image.Image, scal_size: Optional[int] = None) -> Image.Image:
    """
     Make the picture round
    :param img:
    :param scal_size:
    :return:
    """
    img_size = img.size
    mask = Image.new("L", (img_size[0] * 3, img_size[1] * 3), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, img_size[0] * 3, img_size[1] * 3), fill=255)
    mask = mask.resize(img_size)
    img.putalpha(mask)
    if scal_size:
        img = img.resize((scal_size, scal_size))
    return img


async def get_pictures(url: Union[str, list], img_size: Union[int, list, None] = None) -> Union[
    None, Image.Image, list]:
    """
    get images from net
    :param img_size: If the image needs to be scaled, this parameter is the size of the scaled image
    :param url:
    :return:
    """
    async with httpx.AsyncClient() as client:
        if isinstance(url, str):
            img = await send_request(client, url)
            if img_size and isinstance(img_size, int):
                img = img.resize((img_size, img_size))
            return img
        if isinstance(url, list):
            task = [send_request(client, i) for i in url]
            result = await asyncio.gather(*task)
            return result
        else:
            return None


async def send_request(client: httpx.AsyncClient, url: str, img_size: Optional[int] = None) -> Optional[
    Image.Image, None]:
    """
    发送网络请求
    :param img_size: If the image needs to be scaled, this parameter is the size of the scaled image
    :param client: client
    :param url: image url
    :return:
    """
    try:
        response = await client.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        if img_size:
            img = img.resize((img_size, img_size))
        return img
    except Exception:
        logger.exception("error")
        return None
