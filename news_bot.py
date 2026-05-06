import feedparser
import google.generativeai as genai
import telegram
import asyncio
import os
import urllib.parse

# 환경 변수 설정
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
    genai.configure(api_key=GEMINI_API_KEY)
    
    # [핵심] 사용 가능한 모델 목록을 확인하여 에러 방지
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # 1.5 flash가 있으면 쓰고, 없으면 첫 번째 사용 가능한 모델 선택
    target_model = 'models/gemini-1.5-flash'
    if target_model not in available_models:
        target_model = available_models[0] if available_models else None

    if not target_model:
        summary = "사용 가능한 AI 모델을 찾지 못했습니다."
    else:
        model = genai.GenerativeModel(target_model)
        raw_news = get_news()
        prompt = f"투자 비서로서 다음 뉴스를 섹션별로 요약하고 투자 시사점을 알려줘:\n\n{raw_news}"
        
        try:
            response = model.generate_content(prompt)
            summary = response.text
        except Exception as e:
            summary = f"요약 실패 (모델: {target_model}): {str(e)}"

    # 텔레그램 전송
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=summary)

if __name__ == "__main__":
    asyncio.run(main())
