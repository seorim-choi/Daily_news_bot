import feedparser
import google.generativeai as genai
import telegram
import asyncio
import os

# 깃허브 금고(Secrets)에서 정보 가져오기
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_news():
    # 관심 분야 키워드로 최신 뉴스 수집
    queries = ["반도체 IT 테크", "미국 증시 시황", "국제 정세 전망"]
    all_news = ""
    for q in queries:
        url = f"https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(url)
        all_news += f"\n[{q} 관련 소식]\n" + "\n".join([e.title for e in feed.entries[:7]])
    return all_news

async def main():
    # Gemini 설정 및 요약
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    news_data = get_news()
    prompt = f"""
    너는 경제 및 IT 전문 전략가야. 아래 뉴스 목록을 분석해서 브리핑을 작성해줘.
    1. 반도체/IT, 2. 미 증시, 3. 국외 정세 섹션별로 가장 중요한 소식을 요약할 것.
    단순 요약이 아니라 '투자에 참고할 만한 시사점'을 한 문장씩 덧붙여줘.
    어조는 친절하고 전문적인 비서처럼 해줘.

    뉴스 목록:
    {news_data}
    """

    response = model.generate_content(prompt)

    # 텔레그램으로 전송
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=response.text)

if __name__ == "__main__":
    asyncio.run(main())
