# ⭐️ misscore

A third-party RESTful API for the "MissAV" website, designed to scrape and structure website data.

## ⚙️ Quick Start

To install misscore from the Python Package Index (PyPI) run:

```
pip install -r requirements.txt
```

```
uvicorn api.main:misscore --reload
```

## 📖 API docs

```
http://localhost:8000/docs
```

## 📖 Localization

Localized responses can be achieved by switching the `Accept-Language` in the request header.

```curl
curl -X 'GET' \
  'http://localhost:8000/api/v1/movie/uncensored/fc2?page=1' \
  -H 'Accept-Language: zh-CN' \
  -H 'accept: application/json' \
  -H 'auth-key: key from login'
```
