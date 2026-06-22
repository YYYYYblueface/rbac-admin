import base64
import io
import random
import string
import uuid

from captcha.image import ImageCaptcha

from app.config import settings
from app.utils.redis_client import redis_client


async def generate_captcha() -> dict:
    """生成图形验证码，存入 Redis"""
    code = "".join(random.choices(string.digits, k=4))
    image = ImageCaptcha(width=120, height=50)
    data = image.generate(code)
    buf = io.BytesIO()
    image.write(code, buf)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")

    captcha_key = f"captcha:{uuid.uuid4().hex}"
    await redis_client.setex(captcha_key, settings.CAPTCHA_EXPIRE_SECONDS, code)

    return {"captcha_key": captcha_key, "captcha_image": f"data:image/png;base64,{img_base64}"}


async def verify_captcha(captcha_key: str, captcha_code: str) -> bool:
    """验证图形验证码"""
    stored_code = await redis_client.get(captcha_key)
    if stored_code is None:
        return False
    if stored_code.lower() != captcha_code.lower():
        return False
    await redis_client.delete(captcha_key)
    return True