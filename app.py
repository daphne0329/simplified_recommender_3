from flask import Flask, request, jsonify
import pandas as pd
import random
import os
from datetime import datetime

app = Flask(__name__)

# 读取数据集
df = pd.read_excel("Enhanced_Dataset_OpenAI_Simplified_3.xlsx")

@app.route("/generate-recommendation", methods=["POST"])
def generate_recommendation():
    data = request.get_json()

    # 直接获取字符串格式的主题名（如 "Technology"、"Politics"）
    preferred_topic = data.get("preferred")
    non_preferred_topic = data.get("non_preferred")

    if not preferred_topic or not non_preferred_topic:
        return jsonify({"error": "Invalid topic string(s)."}), 400

    # Preferred 推荐逻辑
    prefer_df = df[df["Internal Topic"] == preferred_topic]
    if len(prefer_df) < 6:
        return jsonify({"error": "Not enough preferred articles."}), 400
    prefer_selected = prefer_df.sample(n=6, random_state=random.randint(1, 10000))

    # Serendipitous 推荐逻辑
    seren_df = df[
        (df["Primary Topic"] == non_preferred_topic) &
        (df["Internal Topic"] == "Hybrid")
    ]
    relevance_col = f"Relevance_{preferred_topic}"
    if relevance_col not in seren_df.columns:
        return jsonify({"error": f"Missing relevance score: {relevance_col}"}), 400

    seren_df_sorted = seren_df.sort_values(by=relevance_col, ascending=False)
    top_10pct_count = max(1, int(len(seren_df_sorted) * 0.10))
    top_seren_df = seren_df_sorted.head(top_10pct_count)

    if len(top_seren_df) < 2:
        return jsonify({"error": "Not enough serendipitous articles."}), 400
    seren_selected = top_seren_df.sample(n=2, random_state=random.randint(1, 10000))

    # 构建返回结果
    response = {}
    for i, (_, row) in enumerate(prefer_selected.iterrows(), 1):
        response[f"Prefer_Article{i}_Title"] = row["Title"]
        response[f"Prefer_Article{i}_Summary"] = row["Content Summary"]
        response[f"Prefer_Article{i}_Topic"] = row["Primary Topic"]
        response[f"Prefer_Article{i}_Picture"] = row["Picture"]

    for i, (_, row) in enumerate(seren_selected.iterrows(), 1):
        response[f"Seren_Article{i}_Title"] = row["Title"]
        response[f"Seren_Article{i}_Summary"] = row["Content Summary"]
        response[f"Seren_Article{i}_Topic"] = row["Primary Topic"]
        response[f"Seren_Article{i}_Picture"] = row["Picture"]

    # 添加当前日期（格式为 YYYY-MM-DD）
    response["Today"] = datetime.today().strftime("%Y-%m-%d")

    return jsonify(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
