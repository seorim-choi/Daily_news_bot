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
    # 1. Gemini 요약 (모델 명칭을 최신 안정화 버전으로 변경)
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest') # 👈 명칭 수정됨
    
    raw_news = get_news()
    prompt = f"투자 전문가로서 다음 뉴스들을 섹션별로 요약하고 투자 인사이트를 알려줘:\n\n{raw_news}"
    
    # 예외 처리 추가 (에러 발생 시 확인용)
    try:
        response = model.generate_content(prompt)
        content = response.text
    except Exception as e:
        content = f"요약 중 에러가 발생했습니다: {str(e)}"
    
    # 2. 텔레그램 전송
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=content)

if __name__ == "__main__":
    asyncio.run(main())
