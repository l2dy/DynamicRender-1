import json
import httpx
import asyncio
from bilirpc.api import get_dy_detail
from dynamicrender.Core import DyRender
from dynamicadaptor.DynamicConversion import formate_message
from google.protobuf.json_format import MessageToJson

async def grpc_test():
    message  = await get_dy_detail("753550783931219987")
    if message:
        message_str = MessageToJson(message[0])
        message_json = json.loads(message_str)
        message_formate = await formate_message("grpc",message_json)
        img  = await DyRender().dyn_render(message_formate)
        img.show()

async def web_test():
    dyn_id = "753550783931219987"
    url = f"https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?timezone_offset=-480&id={dyn_id}&features=itemOpusStyle"
    headers = {
        "referer":f"https://t.bilibili.com/{dyn_id}"
    }
    message_json = httpx.get(url,headers=headers).json()
    message_formate = await formate_message("web",message_json["data"]["item"])
    img  = await DyRender().dyn_render(message_formate)
    img.show()


    # print(result)



if __name__ == "__main__":
    # asyncio.run(grpc_test())
    asyncio.run(web_test())


