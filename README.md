# AI-powered D&D by hyhrya team

## Софт

#### Скомпилированно на
 - Python 3.12
 - Node 22.6.0
 - Git 2.43.0

## Запуск

### Для первоначальной настройки

**В любой пустой директории**
```bash
git clone https://github.com/huhrya/suno-api-multy-account.git
cd suno-api-multy-account
npm i
```

Перейдите на [https://suno.com/create](https://suno.com/create) и авторизуйтесь. Получите Cookie по инструкции:
![cookie get](https://github.com/gcui-art/suno-api/raw/main/public/get-cookie-demo.gif)

Можете повторить несколько раз с разных аккаунтов, для увеличения лимита (по умолчанию для 1 аккаунта это 10 песен)

---

Скопируйте файл .env.example в .env

UNIX:
```bash
cp .env.example .env
```

Win cmd:
```bash
copy .env.example .env
```

Win PowerShell:
```bash
Copy-Item .env.example .env
```

Отредактируйте полученный файл .env:
```bash
SUNO_COOKIES='["<Полученный Cookie>", "<Полученный Cookie 2>", ... "<Полученный Cookie X>"]'
```
Cookie может быть сколько угодно, можно один, можно десяток. Главное хотя бы один, но тогда будет ограничение (1 Cookie = 10 песен)

---

Затем надо ввести в консоли, там же где и прописывали `npm i`:

```bash
npm run build
```

**В этой директории**
```bash
pip install -r req.txt
```
---
Скопируйте файл cfg.example.json в cfg.json

UNIX:
```bash
cp cfg.example.json cfg.json
```

Win cmd:
```bash
copy cfg.example.json cfg.json
```

Win PowerShell:
```bash
Copy-Item cfg.example.json cfg.json
```

Отредактируйте полученный файл, добавьте туда ключ с сайта openai.
```json
{"openai": "OPEN AI KEY"}
```

### Для запуска

В директории suno-api-multy-account
```bash
npx next start -p 45540
```

В этой директории
```bash
python main.py
```
