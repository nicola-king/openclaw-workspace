# 🏪 开店选址分析MVP

城市：
最小面积(m²)：
最大面积(m²)：
最大租金(元/月)：

{% if heatmap\_file %}

## 🗺️ 商圈与候选店铺分布

{% if results %}

## 📊 ROI排名

| 排名 | 名称 | 面积 | 月租 | 人流 | 竞品 | 预测ROI |
| --- | --- | --- | --- | --- | --- | --- |
{% for r in results %}| {{ loop.index }} | {{ r.name }} | {{ r.area }}m² | ¥{{ r.rent }} | {{ r.foot\_traffic }} | {{ r.competitors\_count }} | {{ "%.1f"|format(r.predicted\_roi) }}% |
{% endfor %}

{% endif %}

### 📈 经济数据: {{ city }}

GDP: {{ eco.gdp\_亿 }}亿 · 人口: {{ eco.人口\_万 }}万 · 人均消费: {{ eco.人均消费\_元 }}元

{% if report %}

### 💼 投资建议: {{ report.investment\_level }}

{% endif %}
[📥 下载ROI排序Excel](%7B%7B%20excel_file%20%7D%7D)
{% endif %}