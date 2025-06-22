from httpx import AsyncClient
from bs4 import BeautifulSoup
import asyncio

URL = 'https://www.zhiyuanyun.com/app/api/view.php?m=get_login_yzm'
UA = 'Mozilla/5.0 (Linux; Android 15; PJF110 Build/UKQ1.231108.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/135.0.7043.0 Mobile Safari/537.36 MMWEBID/1532 MicroMessenger/8.0.49.2600(0x28003133) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64'

async def get_captcha_html(url: str, client: AsyncClient):
    return (await client.get(url, headers = {'User-Agent': UA}))\
        .raise_for_status()\
        .text

def get_captcha(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    # 查找所有符合条件的 <p> 标签
    captcha_p = soup.find('p', style='font-size:28px;font-weight:bold;letter-spacing:5px;')
    if not captcha_p:
        raise CaptchaNotFound(html)

    # 提取验证码文本
    return captcha_p.get_text()

class CaptchaNotFound(Exception):
    pass

async def main() -> str:
    async with AsyncClient() as client:
        html = await get_captcha_html(URL, client)
    captcha = get_captcha(html)
    return captcha

if __name__ == '__main__':
    print(
        asyncio.run(main())
    )
