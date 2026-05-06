import feedparser
import google.generativeai as genai
import telegram
import asyncio
import os
import urllib.parse

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_news():
    queries = ["반도체", "미국증시", "국제정세"]
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
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    raw_news = get_news()
    prompt = f"투자 전문가로서 다음 뉴스들을 요약하고 인사이트를 알려줘:\n\n{raw_news}"
    response = model.generate_content(prompt)
    
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=response.text)

if __name__ == "__main__":
    asyncio.run(main())
