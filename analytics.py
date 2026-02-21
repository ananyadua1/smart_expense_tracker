def spending_insights(df, category_limits):
    insights = []

    if df.empty:
        return insights

    category_totals = df.groupby("category")["amount"].sum()

    for category, total in category_totals.items():
        limit = category_limits.get(category)
        if limit and total > limit:
            insights.append(
                f"🚨 {category} spending exceeded limit of Rs. {limit}"
            )

    top_category = category_totals.idxmax()
    insights.append(f"📌 Highest spending category: {top_category}")

    return insights