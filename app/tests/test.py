# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import httpx
import certifi  # 导入 Poetry 环境的 certifi 库

# 使用 Poetry 环境自带的 SSL 证书（certifi.where() 会返回正确路径）
ssl_cert_path = certifi.where()

# 创建指定证书的 HTTP 客户端
http_client = httpx.Client(verify=ssl_cert_path)

client = OpenAI(
    api_key="sk-bdddcb929db14008a0b4722cd103d967", 
    base_url="https://api.deepseek.com",
    http_client=http_client)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)