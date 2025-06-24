
# Final News Recommender with Image Field (v2)

This Flask app returns preferred and serendipitous news articles with image URLs.

## 🔁 POST Request Format

```json
{
  "preferred": 1,
  "non_preferred": 3
}
```

## 🧠 Recommendation Logic

### Preferred (6 articles)
- Internal Topic matches preferred topic
- Random sample of 6
- Fields: Title, Summary, Primary Topic, Picture

### Serendipitous (2 articles)
- Primary Topic matches non-preferred
- Internal Topic = Hybrid
- Top 10% by Relevance_{Preferred}, sample 2
- Fields: Title, Summary, Primary Topic, Picture

## 📦 Files

- `app.py`
- `requirements.txt`
- `Procfile`
- `README.md`

## 🚀 Deployment (Railway)

1. Upload with `Enhanced_Dataset_OpenAI_Simplified_3.xlsx` to GitHub
2. Connect repo to [Railway](https://railway.app)
3. Done!

## 📌 Output

```json
{
  "Prefer_Article1_Title": "...",
  "Prefer_Article1_Picture": "...",
  "Seren_Article1_Picture": "..."
}
```
