from DynConfig import DynColor, DynFontPath, DynSize
from Core import Image,Optional
from dynamicadaptor.Content import Text

class DynTextRender:
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
        self.static_path = static_path
        self.dyn_color =dyn_color
        self.dyn_font_path = dyn_font_path
        self.dyn_size = dyn_size
    

    async def run(dyn_text:Text,type:Optional[str]=None) -> Optional[Image.Image]:
        """Render the text of the dynamic into image

        Parameters
        ----------
        dyn_text : Text
            The text of the dynamic
        type : Optional[str]
            F or None
        Returns
        -------
        Optional[Image.Image]
            Rendered image
        """

        pass
