import feedparser
import google.generativeai as genai
from google.generativeai.types import RequestOptions # 설정 옵션 추가
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
    # 1. Gemini 설정 (API 버전을 v1으로 강제 고정하여 404 에러 차단)
    genai.configure(api_key=GEMINI_API_KEY)
    
    # 가장 대중적인 gemini-1.5-flash를 사용하되, 경로 설정을 보강합니다.
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    raw_news = get_news()
    prompt = f"투자 비서로서 다음 뉴스를 섹션별로 요약하고 투자 시사점을 알려줘:\n\n{raw_news}"
    
    try:
        # v1 버전을 사용하도록 명시적으로 요청 옵션을 넣습니다.
        response = model.generate_content(
            prompt,
            request_options=RequestOptions(api_version='v1') # 👈 핵심 해결책
        )
        content = response.text
    except Exception as e:
        content = f"최종 시도 실패. 에러 내용: {str(e)}"
    
    # 2. 텔레그램 전송
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=content)

if __name__ == "__main__":
    asyncio.run(main())
