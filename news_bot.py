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
    # 1. Gemini 설정 (가장 단순한 호출 방식으로 변경)
    genai.configure(api_key=GEMINI_API_KEY)
    
    # 모델 이름을 'gemini-1.5-flash'로 고정
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    raw_news = get_news()
    prompt = f"투자 비서로서 다음 뉴스를 섹션별로 요약하고 투자 시사점을 알려줘:\n\n{raw_news}"
    
    try:
        # 부가 옵션 없이 가장 기본 기능만 실행합니다.
        response = model.generate_content(prompt)
        content = response.text
    except Exception as e:
        content = f"죄송합니다. 요약 중 오류가 발생했습니다: {str(e)}"
    
    # 2. 텔레그램 전송
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=content)

if __name__ == "__main__":
    asyncio.run(main())
