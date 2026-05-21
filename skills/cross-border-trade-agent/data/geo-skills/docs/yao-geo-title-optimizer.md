<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-title-optimizer
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# yao-geo-title-optimizer

`yao-geo-title-optimizer` generates GEO title systems for Chinese content production. It is designed for article, FAQ, comparison, brand validation, and topic-hub titles that need to be understood, classified, retrieved, and cited by domestic AI platforms.

The skill outputs Markdown, HTML, Word DOCX, and PDF reports. Word output uses a dedicated fixed-width layout with DOCX table-width inspection to prevent right-side overflow.

The renderer consumes a render-ready `report_input.json`. A raw keyword brief should first be converted into title candidates, scoring, compliance checks, article-structure mapping, and self-review records. The generated quality report now records both DOCX table-width checks and PDF parse/page checks.

The current report standard requires a deeper analysis layer: authoritative reference framework, analysis dimensions, entity-intent matrix, title pattern library, coverage gaps, and publication checklist. HTML reports include sticky section navigation for long-form review.

The skill now includes a public evidence collection helper, `scripts/collect_yao_geo_title_evidence.py`, for lightweight URL snapshots. Reports must distinguish fetched public evidence, user-supplied private evidence, platform answer exports, and unavailable data.
