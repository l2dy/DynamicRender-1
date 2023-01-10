import emoji
import asyncio
from loguru import logger
from math import ceil
from os import path
from fontTools.ttLib import TTFont
from dynamicadaptor.Majors import Major
from PIL import Image, ImageDraw, ImageFont

from .Core import Image, Optional
from .DynConfig import DynColor, DynFontPath, DynSize
from .Tools import get_pictures



class DynMajorRender:
    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize) -> None:
        """Initial configuration

        Parameters
        ----------
        static_path : str
            path to the static file
        dyn_color : DynColor
            color information in the configuration
        dyn_font_path : DynFontPath
            font_path information in the configuration
        dyn_size : DynSize
            size information in the configuration
        """
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font_path: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size

    async def run(self, dyn_maojor: Major, dyn_type: Optional[str] = None) -> Optional[Image.Image]:
        """Render the major of the dynamic into image

        Parameters
        ----------
        dyn_text : Head
            The major of the dynamic
        dyn_type : Optional[str]
            F or None

        Returns
        -------
        Optional[Image.Image]
            Rendered image
        """
        try:
            major_type = dyn_maojor.type
            if major_type == "MAJOR_TYPE_DRAW":
                return await DynMajorDraw(dyn_maojor, dyn_type, self.dyn_color).run()
            if major_type == "MAJOR_TYPE_ARCHIVE":
                return await DynMajorArchive(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(
                    dyn_maojor, dyn_type)
        except Exception as e:
            logger.exception(e)
            return None


class DynMajorDraw:
    def __init__(self, major_draw: Major, dyn_type: str, dyn_color: DynColor) -> None:
        self.major_draw: Major = major_draw
        self.dyn_type = dyn_type
        self.dyn_color = dyn_color
        self.backgroud_img = None
        self.items = None

    async def run(self) -> Optional[Image.Image]:
        """make the image of the draw

        Returns
        -------
        Optional[Image.Image]
            img
        """
        self.items = self.major_draw.draw.items
        item_count = len(self.items)
        backgroud_color = self.dyn_color.dyn_gray if self.dyn_type == "F" else self.dyn_color.dyn_white
        if item_count == 1:
            await self.single_img(backgroud_color)
        elif item_count in {2, 4}:
            await self.dual_img(backgroud_color)
        else:
            await self.triplex_img(backgroud_color)
        return self.backgroud_img

    async def single_img(self, backgroud_color: str):
        src = self.items[0].src
        img_height = self.items[0].height
        img_width = self.items[0].width
        if img_height / img_width > 4:
            # img_url = f"{src}@{img_width}w_{img_width}h_!header.webp"
            img_url = f"{src}@{600}w_{800}h_!header.webp"
        else:
            img_url = src
        img = await get_pictures(img_url)
        if img is not None:
            img_ori_size = img.size
            img = img.resize(
                (1008, int(img_ori_size[1] * 1008 / img_ori_size[0])))
            img_size = img.size
            self.backgroud_img = Image.new(
                "RGBA", (1080, img_size[1] + 20), backgroud_color)
            self.backgroud_img.paste(img, (36, 10), img)

    async def dual_img(self, backgroud_color: str):
        url_list = []
        for item in self.items:
            src = item.src
            img_height = item.height
            img_width = item.width
            # url_list.append(f"{src}@540w_540h_1c.webp")
            if img_height / img_width > 3:
                url_list.append(f"{src}@520w_520h_!header.webp")
            else:
                url_list.append(f"{src}@520w_520h_1e_1c.webp")
        imgs = await get_pictures(url_list, 520)
        num = len(url_list) / 2
        back_size = int(num * 520 + 20 * num)
        self.backgroud_img = Image.new(
            "RGBA", (1080, back_size), backgroud_color)
        x, y = 15, 10
        for i in imgs:
            if i is not None:
                self.backgroud_img.paste(i, (x, y), i)
            x += 530
            if x > 1000:
                x = 15
                y += 530

    async def triplex_img(self, backgroud_color: str):
        url_list = []
        for item in self.items:
            src = item.src
            img_height = item.height
            img_width = item.width
            if img_height / img_width > 3:
                url_list.append(f"{src}@260w_260h_!header.webp")
            else:
                url_list.append(f"{src}@260w_260h_1e_1c.webp")
        num = ceil(len(self.items) / 3)
        imgs = await get_pictures(url_list, 346)
        back_size = int(num * 346 + 20 * num)
        self.backgroud_img = Image.new(
            "RGBA", (1080, back_size), backgroud_color)
        x, y = 11, 10
        for img in imgs:
            if img is not None:
                self.backgroud_img.paste(img, (x, y), img)
            x += 356
            if x > 1000:
                x = 11
                y += 356


class DynMajorArchive:
    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize) -> None:
        """Initial configuration

        Parameters
        ----------
        static_path : str
            path to the static file
        dyn_color : DynColor
            color information in the configuration
        dyn_font_path : DynFontPath
            font_path information in the configuration
        dyn_size : DynSize
            size information in the configuration
        """
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font_path: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size
        self.background_img = None
        self.background_color = None
        self.text_font = None
        self.extra_font = None
        self.emoji_font = None
        self.key_map = None
        self.src_path = None

    async def run(self, dyn_maojor: Major, dyn_type) -> Optional[Image.Image]:
        self.background_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
        self.background_img = Image.new("RGB", (1080, 695), self.background_color)
        self.draw = ImageDraw.Draw(self.background_img)
        self.text_font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.text)
        self.extra_font = ImageFont.truetype(self.dyn_font_path.extra_text,self.dyn_size.text)
        self.emoji_font = ImageFont.truetype(self.dyn_font_path.emoji,self.dyn_size.emoji)
        self.key_map = TTFont(self.dyn_font_path.text,fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()
        self.src_path = path.join(self.static_path,"Src")
        cover = f"{dyn_maojor.archive.cover}@505w_285h_1c.webp"
        title = dyn_maojor.archive.title
        duration = dyn_maojor.archive.duration_text
        badge = dyn_maojor.archive.badge
        try:
            await asyncio.gather(
                self.make_cover(cover,duration,badge),
                self.make_title(title)
            )
            self.background_img = self.background_img.convert("RGBA")
            return self.background_img
        except Exception as e:
            logger.exception("error")
            return None

    async def make_cover(self,cover:str,duration:str,badge):
        cover = await get_pictures(cover,(1010, 570))
        self.background_img.paste(cover,(35, 25),cover)
        play_icon = Image.open(path.join(self.src_path,"tv.png")).convert("RGBA").resize((130, 130))
        font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.sub_title)
        
        duration_size = font.getsize(duration)
        duration_pic_size = (duration_size[0] + 20, duration_size[1] + 20)
        duration_pic = Image.new("RGBA",duration_pic_size, (0, 0, 0, 90))
        draw = ImageDraw.Draw(duration_pic)
        draw.text((10, 5), duration, fill=self.dyn_color.dyn_white, font=font)
        self.background_img.paste(duration_pic,(80, 525),duration_pic)
        self.background_img.paste(play_icon,(905, 455),play_icon)
        if badge !=None:
            badge_text = badge.text
            bg_color = badge.bg_color
            badge_size = font.getsize(duration)
            badge_pic_size = (badge_size[0] + 50, badge_size[1] + 20)
            badge_pic = Image.new("RGBA",badge_pic_size, bg_color)
            draw = ImageDraw.Draw(badge_pic)
            draw.text((10, 5), badge_text, self.dyn_color.dyn_white, font=font)
            self.background_img.paste(badge_pic,(905, 50),badge_pic)

    async def make_title(self,title):
        emoji = await self.get_emoji(title)
        offset = 0
        position = 35
        total = len(title) - 1
        while offset <= total:
            if offset in emoji:
                emoji_img = emoji[offset]["emoji"]
                self.background_img.paste(emoji_img, (int(position), 606), emoji_img)
                position += (emoji_img.size[0] - 15)
                offset = emoji[offset]["match_end"]
                if position >= 1020:
                    self.draw.text((int(position),600),"...",fill=self.dyn_color.dyn_black,font=self.text_font)
                    break
            else:
                text = title[offset]
                if ord(text) not in self.key_map:
                    self.draw.text((int(position),600),text,fill=self.dyn_color.dyn_black,font=self.extra_font)
                    next_offset = self.extra_font.getbbox(text)[2]
                else:
                    self.draw.text((int(position),600),text,fill=self.dyn_color.dyn_black,font=self.text_font)
                    next_offset = self.text_font.getbbox(text)[2]
                position += next_offset
                offset += 1
                if position >= 1020:
                    self.draw.text((int(position),600),"...",fill=self.dyn_color.dyn_black,font=self.text_font)
                    break



    
    async def get_emoji(self,title):
        result = emoji.emoji_list(title)
        duplicate_removal_result = {i["emoji"] for i in result}
        emoji_dic = {}
        for i in duplicate_removal_result:
            emoji_origin_text = self.emoji_font.getbbox(i)
            emoji_img = Image.new(
                "RGBA", (emoji_origin_text[2], emoji_origin_text[3]), self.background_color)
            draw = ImageDraw.Draw(emoji_img)
            draw.text((0, 0), i, embedded_color=True, font=self.emoji_font)
            emoji_img = emoji_img.resize((self.dyn_size.text, self.dyn_size.text))
            emoji_dic[i] = emoji_img
        temp = {}
        for i in result:
            temp[i["match_start"]] = i
            temp[i["match_start"]]["emoji"] = emoji_dic[temp[i["match_start"]]["emoji"]]
        return temp