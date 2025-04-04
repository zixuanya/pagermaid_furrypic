import httpx
from pagermaid.listener import listener
from pagermaid.enums import Client, Message
from io import BytesIO
from PIL import Image


@listener(
    command="furrypic",
    description="????????????"
)
async def send_furry_image(client: Client, message: Message):
    try:
        async with httpx.AsyncClient() as client_http:
            response = await client_http.get("https://api.furry.ist/furry-img/")
            response.raise_for_status()
            webp_bytes = response.content

        webp_image = Image.open(BytesIO(webp_bytes)).convert("RGB")
        jpeg_file = BytesIO()
        webp_image.save(jpeg_file, format="JPEG")
        jpeg_file.name = "furry.jpg"
        jpeg_file.seek(0)

        await client.send_photo(
            message.chat.id,
            photo=jpeg_file,
            caption="????????",
            reply_to_message_id=message.reply_to_message_id,
            message_thread_id=message.message_thread_id,
        )
        await message.safe_delete()
    except Exception as e:
        await message.edit(f"????????{e}")
