from dynamicadaptor.AddonCard import Additional

from .Core import Image, Optional
from .DynConfig import DynColor, DynFontPath, DynSize


class DynAdditionalRender:
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

    async def run(self, dyn_additional: Additional, type: Optional[str] = None) -> Optional[Image.Image]:
        """Render  additional of the dynamic into image

        Parameters
        ----------
        dyn_additional : Additional
            additional of the dynamic
        type : Optional[str]
            F or None
        Returns
        -------
        Optional[Image.Image]
            Rendered image
        """

        pass
