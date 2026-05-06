import feedparser
import google.generativeai as genai
import telegram
import asyncio
import os
import urllib.parse # 주소 변환 라이브러리 추가

# 환경 변수 가져오기
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_news():
    # 검색 키워드 (공백이 있어도 안전하게 처리하도록 수정)
    queries = ["반도체", "미국 증시", "국제 정세"]
    news_text = ""
    for q in queries:
        # 공백 등을 주소용 글자로 변환 (예: 공백 -> %20)
        encoded_q = urllib.parse.quote(q)
        url = f"https://news.google.com/rss/search?q={encoded_q}&hl=ko&gl=KR&ceid=KR:ko"
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
    
    # 2. 텔레그램 전송
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=response.text)

if __name__ == "__main__":
    asyncio.run(main())
