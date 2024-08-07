# AI-powered D&D by hyhrya team

## Софт

#### Скомпилированно на
 - Python 3.12
 - Node 22.6.0
 - Git 2.43.0

## Запуск

### Для первоначальной настройки

В любой пустой директории
```bash
git clone https://github.com/gcui-art/suno-api.git
cd suno-api
npm i
```

Перейдите на [https://suno.com/create](https://suno.com/create) и авторизуйтесь. Получите Cookie по инструкции:
![cookie get](https://github.com/gcui-art/suno-api/raw/main/public/get-cookie-demo.gif)

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
SUNO_COOKIE=<Полученный Cookie>
```

---

```bash
npm run build
```

В этой директории
```bash
pip install -r req.txt
```

### Для запуска

В директории suno-api
```bash
npx next start -p 45540
```

В этой директории
```bash
python main.py
```
