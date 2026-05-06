name: Daily News Briefing
on:
  schedule:
    - cron: '0 0 * * *' # UTC 00:00은 한국 시간 오전 9:00입니다.
  workflow_dispatch: # 직접 실행해볼 수 있는 버튼을 만듭니다.

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install feedparser google-generativeai python-telegram-bot
      - name: Run script
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
        run: python news_bot.py
