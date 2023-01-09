from .DynConfig import DynColor, DynFontPath, DynSize
from .Core import Image, Optional
from dynamicadaptor.Majors import Major
from loguru import logger
from .Tools import get_pictures
from math import ceil


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
            print(major_type)
            if major_type == "MAJOR_TYPE_DRAW":
                return await DynMajorDraw(dyn_maojor, dyn_type, self.dyn_color).run()
            if major_type == "MAJOR_TYPE_ARCHIVE":
                return await DynMajorArchive(self.static_path, self.dyn_color, self.dyn_font_path, self.dyn_size).run(dyn_maojor, dyn_type)
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
                "RGBA", (1080, img_size[1]+20), backgroud_color)
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
        self.backgroud_img = None

    async def run(self, dyn_maojor: Major, dyn_type) -> Optional[Image.Image]:
        backgroud_color = self.dyn_color.dyn_gray if dyn_type == "F" else self.dyn_color.dyn_white
        self.backgroud_img = Image.new("RGBA", (1080, 695), backgroud_color)
        cover = dyn_maojor.archive.cover
        title = dyn_maojor.archive.title
        duration = dyn_maojor.archive.duration_text
        


        return self.backgroud_img
        
