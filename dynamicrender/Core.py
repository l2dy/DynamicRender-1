from dynamicadaptor.Message import RenderMessage
from DynConfig import ConfigInit, Optional, Union
from PIL import Image

class DyRender(ConfigInit):
    def __init__(self, data_path: Optional[str] = None, font_path: Union[None, str, dict] = None):
        super().__init__(data_path, font_path)

    async def dyn_render(self, message: RenderMessage) -> Image.Image:
        tasks = []
        if message.header:
            pass


if __name__ == "__main__":
    DyRender("/home/dmc/D","123")
