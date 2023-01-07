from .DynConfig import DynColor, DynFontPath, DynSize
from PIL import ImageDraw, Image, ImageFont
from dynamicadaptor.Header import Head
from .Tools import circle_picture, get_pictures
from os import path
from loguru import logger
from typing import Optional
import asyncio
import time

class DynHeaderRender:
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
        self.cache_path = None
        self.src_path = None
        self.backgroud_img = None
        self.draw = None
        self.head_message = None

    async def run(self, dyn_head: Head) -> Optional[Image.Image]:
        """Render the head of the dynamic into image

        Parameters
        ----------
        dyn_head : Head
            The Head of the dynamic

        Returns
        -------
        Optional[Image.Image]
            Rendered image
        """
        start = time.perf_counter()
        self.cache_path = path.join(self.static_path, "Cache")
        self.src_path = path.join(self.static_path, "Src")
        try:
            self.head_message = dyn_head
            self.backgroud_img = Image.new(
                "RGBA", (1080, 400), self.dyn_color.dyn_white)
            self.draw = ImageDraw.Draw(self.backgroud_img)
            

            #The gather function is executed out of order. 
            # To prevent the pendent and vip images from being under the face image, 
            # draw_pendant() and draw_vip need to be executed separately

            await asyncio.gather(*[
                self.draw_name(),
                self.draw_pub_time(),
                self.draw_face()
            ])
            await self.draw_pendant()
            await self.draw_vip()
            print(time.perf_counter()-start)
            self.backgroud_img.show()
        except Exception as e:
            logger.exception(e)
            return None

    async def draw_name(self) -> None:
        # print(self.dyn_font_path.text)
        font = ImageFont.truetype(
            font=self.dyn_font_path.text, size=self.dyn_size.uname)
        # 如果是大会员的话
        if self.head_message.vip and self.head_message.vip.status == 1:
            # 如果是大会员名字是粉色
            if self.head_message.vip.avatar_subscript == 1:
                color = self.dyn_color.dyn_pink
            else:
                # 到了愚人节大会员名字会变成绿色
                color = self.dyn_color.dyn_green
        else:
            color = self.dyn_color.dyn_black

        self.draw.text((200, 250), self.head_message.name, fill=color,font=font)
        logo =  Image.open(path.join(self.src_path, "bilibili.png")).convert("RGBA").resize((231, 105))
        self.backgroud_img.paste(logo,(433, 20),logo)


    async def draw_face(self) -> None:
        face = await self.get_face_and_pendant("face")
        if face:
            face = await circle_picture(face)
            self.backgroud_img.paste(face,(45, 245),face)

    async def draw_pub_time(self) -> None:
        if self.head_message.pub_time:
            pub_time = self.head_message.pub_time
        elif self.head_message.pub_ts:
            pub_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.head_message.pub_ts))
        else:
            pub_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time))
        font = ImageFont.truetype(self.dyn_font_path.text,self.dyn_size.sub_text) 
        self.draw.text((200, 320),pub_time,self.dyn_color.dyn_silver_gray,font)


    async def draw_pendant(self) -> None:
        if self.head_message.pendant and self.head_message.pendant.image:
            pendant = await self.get_face_and_pendant("pendant")
            if pendant:
                self.backgroud_img.paste(pendant,(10,210),pendant)

    async def draw_vip(self):
        if self.head_message.official_verify and self.head_message.official_verify.type != -1:
            if self.head_message.official_verify.type == 0:
                img_path = path.join(self.src_path,"official_yellow.png")
            else:
                img_path = path.join(self.src_path,"official_blue.png")
            official_img = Image.open(img_path).resize((45, 45)).convert("RGBA")
            self.backgroud_img.paste(official_img,(120, 330),official_img)
        elif self.head_message.vip and self.head_message.vip.status == 1:
            if self.head_message.vip.avatar_subscript == 1:
                img_path = path.join(self.src_path,"big_vip.png")
            else:
                img_path = path.join(self.src_path,"small_vip.png")
            vip_image = Image.open(img_path).resize((45, 45)).convert("RGBA")
            self.backgroud_img.paste(vip_image,(120, 330),vip_image)


            

    async def get_face_and_pendant(self, img_type: str) -> Optional[Image.Image]:
        if img_type == "face":
            img_name = f"{self.head_message.name}.webp"
            img_url = f"{self.head_message.face}@120w_120h_1c_1s.webp"
            img_path = path.join(self.cache_path,"Face",img_name) 
        else:
            img_name =  f"{self.head_message.pendant.pid}.png"
            img_url = f"{self.head_message.pendant.image}@190w_190h.webp"
            img_path = path.join(self.cache_path,"Pendant",img_name)

        if path.exists(img_path):
            if img_type == "face" and time.time() - int(path.getmtime(img_path)) > 43200:
                img = await get_pictures(img_url)
                if isinstance(img,Image.Image):
                    img.save(img_path)
                    return img
                else:
                    return None
            else:
                img = Image.open(img_path)
                return img
        else:
            img = await get_pictures(img_url)
            if isinstance(img,Image.Image):
                img.save(img_path)
                return img
            else:
                return None

                    





class DynForwardHeaderRender:
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

    async def run(self, forward_dyn_head: Head) -> Image.Image:
        """Render the forward head of the dynamic into image

        Parameters
        ----------
        forward_dyn_head : Head
            The Head of the forward dynamic

        Returns
        -------
        Image.Image
            Rendered image

        """

        pass
