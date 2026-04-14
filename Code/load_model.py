import asyncio
import aiohttp
from dotenv import load_dotenv
import os
import json
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


load_dotenv('../.env')
API_KEY = "api_key"
API_URL = "api_url"
MODEL = "model" 

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

total_token_usage=0
async def fetch_response(session, input_text, model=MODEL, max_retries=5):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": input_text}],
        "max_tokens": 8192
    }
    retry_interval = 1

    for attempt in range(max_retries):
        try:
            async with session.post(API_URL, headers=HEADERS, json=payload) as resp:
                if resp.status == 200:
                    if resp.content_type == 'text/plain':
                        data = await resp.text()
                        response = json.loads(data)["choices"][0]["message"]["content"]
                    else:
                        data = await resp.json()
                        response = data["choices"][0]["message"]["content"]
                    return response
                elif resp.status == 429:
                    await asyncio.sleep(retry_interval)
                    retry_interval *= 2
                else:
                    text = await resp.text()
                    break
        except Exception as e:
            await asyncio.sleep(retry_interval)
            retry_interval *= 2
    return "请求失败"

async def batch_llm_response(inputs,model):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_response(session, input_text, model) for input_text in inputs]
        return await asyncio.gather(*tasks)
