import feedparser
import google.generativeai as genai
import telegram
import asyncio
import os

# 환경 변수 가져오기
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_news():
    # 검색 키워드 최적화
    queries = ["반도체", "미국 증시", "국제 정세"]
    news_text = ""
    for q in queries:
        url = f"https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(url)
        news_text += f"\n[{q} 뉴스]\n"
        for entry in feed.entries[:5]:
            news_text += f"- {entry.title}\n"
    return news_text

async def main():
    # 1. Gemini 요약
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    raw_news = get_news()
    prompt = f"투자 비서로서 다음 뉴스를 섹션별로 요약하고 투자 시사점을 알려줘:\n\n{raw_news}"
    
    response = model.generate_content(prompt)
    
    # 2. 텔레그램 전송 (최신 버전 방식)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=response.text)

if __name__ == "__main__":
    asyncio.run(main())
