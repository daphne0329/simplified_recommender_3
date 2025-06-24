from flask import Flask, request, jsonify
import pandas as pd
import random
from datetime import datetime

app = Flask(__name__)

# 加载数据集（你已设为含标题、摘要、Topic、图片等字段）
dataset = pd.read_excel("Enhanced_Dataset_OpenAI_Simplified_3.xlsx")

@app.route('/generate-recommendation', methods=['POST'])
def generate_recommendation():
    data = request.get_json()

    # 获取来自 Qualtrics 的 POST 字段（字符串类型的主题）
    preferred = data.get("preferred")          # 例："Technology"
    non_preferred = data.get("non_preferred")  # 例："Politics"

    # 安全检查
    if not preferred or not non_preferred:
        return jsonify({"error": "Missing required parameters."}), 400

    # 获取当前日期
    today_str = datetime.today().strftime("%B %d, %Y")

    # 从 Internal Topic == preferred 的文章中随机选 6 篇
    preferred_pool = dataset[dataset["Internal Topic"] == preferred]
    prefer_articles = preferred_pool.sample(n=6, random_state=random.randint(0, 10000))

    # 从 Internal Topic == "Hybrid" 且 Primary Topic == non_preferred 的文章中
    # 选出与 preferred 相关性最高的前10%，再随机抽取2篇
    hybrid_pool = dataset[
        (dataset["Internal Topic"] == "Hybrid") &
        (dataset["Primary Topic"] == non_preferred)
    ]

    top_10_percent = int(0.1 * len(hybrid_pool))
    top_hybrid = hybrid_pool.sort_values(
        by=f"Relevance_{preferred}", ascending=False
    ).head(top_10_percent)

    seren_articles = top_hybrid.sample(n=2, random_state=random.randint(0, 10000))

    # 构建返回 JSON（字段名必须与 Qualtrics 中 Embedded Data 完全一致）
    result = {
        "Today": today_str,
    }

    for i, row in prefer_articles.reset_index(drop=True).iterrows():
        idx = i + 1
        result[f"Prefer_Article{idx}_Title"] = row["Title"]
        result[f"Prefer_Article{idx}_Summary"] = row["Content Summary"]
        result[f"Prefer_Article{idx}_Topic"] = row["Primary Topic"]
        result[f"Prefer_Article{idx}_Picture"] = row["Picture"]

    for i, row in seren_articles.reset_index(drop=True).iterrows():
        idx = i + 1
        result[f"Seren_Article{idx}_Title"] = row["Title"]
        result[f"Seren_Article{idx}_Summary"] = row["Content Summary"]
        result[f"Seren_Article{idx}_Topic"] = row["Primary Topic"]
        result[f"Seren_Article{idx}_Picture"] = row["Picture"]

    return jsonify(result)
