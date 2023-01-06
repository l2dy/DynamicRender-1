from .DynConfig import DynColor, DynFontPath, DynSize
from .Core import Image
from dynamicadaptor.Header import Head
from .Tools import circle_picture
from os import path


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
        self.cache_path = path.join(self.static_path, "Cache")
        self.src_path = path.join(self.static_path, "Src")

    async def run(self, dyn_head: Head) -> Image.Image:
        """Render the head of the dynamic into image

        Parameters
        ----------
        dyn_head : Head
            The Head of the dynamic

        Returns
        -------
        Image.Image
            Rendered image
        """
        pass

    async def get_pic(self, img_type: str, img_name: str, img_url: str):
        """
        get picture by name
        :param img_url:
        :param img_type:
        :param img_name:
        :return:
        """
        pass


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
