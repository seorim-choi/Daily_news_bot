import feedparser
import google.generativeai as genai
import telegram
import asyncio
import os
import urllib.parse

# 환경 변수 가져오기
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_news():
    queries = ["반도체", "미국 증시", "국제 정세"]
    news_text = ""
    for q in queries:
        encoded_q = urllib.parse.quote(q)
        url = f"https://news.google.com/rss/search?q={encoded_q}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(url)
        news_text += f"\n[{q} 뉴스]\n"
        for entry in feed.entries[:5]:
            news_text += f"- {entry.title}\n"
    return news_text

async def main():
    # 1. Gemini 설정 (안전한 버전으로 강제 지정)
    genai.configure(api_key=GEMINI_API_KEY)
    
    # 여러 이름 중 가장 범용적인 이름을 시도합니다.
    model_name = 'gemini-pro' # 👈 flash 대신 더 안정적인 pro로 잠시 바꿔봅시다.
    model = genai.GenerativeModel(model_name)
    
    raw_news = get_news()
    prompt = f"투자 전문가로서 다음 뉴스들을 요약하고 투자 포인트 알려줘:\n\n{raw_news}"
    
    try:
        response = model.generate_content(prompt)
        content = response.text
    except Exception as e:
        content = f"모델 '{model_name}' 호출 실패. 다시 시도해볼게요. 에러: {str(e)}"
    
    # 2. 텔레그램 전송
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=content)

if __name__ == "__main__":
    asyncio.run(main())
