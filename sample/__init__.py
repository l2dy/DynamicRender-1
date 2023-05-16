import sys
sys.path.append("/home/dmc/Python/DynamicRender")



import json
import httpx
import asyncio
from bilirpc.api import get_dy_detail
from dynamicrender.Core import DyRender
from dynamicadaptor.DynamicConversion import formate_message
from google.protobuf.json_format import MessageToJson


async def grpc_test():

    message = await get_dy_detail("795938194175557665")

    if message:
        message_str = MessageToJson(message[0])
        message_json = json.loads(message_str)
        message_formate = await formate_message("grpc", message_json)
        # print(message_formate.text)
        img = await DyRender().dyn_render(message_formate)
        img.save("1.png")
        # img.show()


async def web_test():
    dyn_id = "793678186661543957"
    url = f"https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?timezone_offset=-480&id={dyn_id}&features=itemOpusStyle"
    headers = {
        "referer": f"https://t.bilibili.com/{dyn_id}",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    message_json = httpx.get(url, headers=headers).json()
    message_formate = await formate_message("web", message_json["data"]["item"])
    # print(message_formate)
    img = await DyRender().dyn_render(message_formate)
    img.save("1.png")


if __name__ == "__main__":
    asyncio.run(grpc_test())
    # asyncio.run(web_test())
    
    
    
