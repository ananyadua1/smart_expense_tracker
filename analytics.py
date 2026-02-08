import pandas as pd

def spending_insights(df):
    insights = []

    if df.empty:
        return insights

    food_avg = df[df["category"] == "Food"]["amount"].mean()
    if food_avg > 3000:
        insights.append("🚨 You are overspending on Food")

    top_category = df.groupby("category")["amount"].sum().idxmax()
    insights.append(f"📌 Highest spending category: {top_category}")

    return insights
