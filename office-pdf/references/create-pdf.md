# Create PDF

Use this reference when generating a new PDF from structured content,
Markdown-derived content, or task-specific source data.

## Default Route

Use ReportLab when the PDF needs reliable pagination, tables, headers, footers,
and print-style layout:

```bash
python scripts/pdf_toolkit.py create-demo --out out.pdf
python scripts/pdf_toolkit.py render --input out.pdf --outdir rendered
python scripts/pdf_toolkit.py inspect --input out.pdf
```

For a real task, copy the starter logic from `scripts/pdf_toolkit.py` into a
task-local script and adapt content, typography, tables, and charts.

## Source Artifacts

Keep the source beside the PDF:

- `content.json` for structured reports
- `.md` for prose-heavy inputs
- `.csv` or `.xlsx` for data-backed tables/charts
- a task script when layout is programmatic

## Content Blocks

Recommended structured blocks:

| Block | Use |
| --- | --- |
| `title` | cover or first-page title |
| `section` | major section heading |
| `paragraph` | body copy |
| `bullet` | list item |
| `callout` | key finding |
| `table` | structured rows |
| `chart` | generated chart from source data |
| `image` | external visual asset |
| `pagebreak` | explicit section break |

## Layout Defaults

- A4 or Letter, depending on user context.
- 25-30 mm outer margins for formal reports.
- Header with document title and a thin accent rule.
- Footer with page number and optional author/client.
- Tables use an accent header row, alternating light rows, and no dense grid.

## When HTML Is Better

Use HTML/CSS plus browser PDF output only when the task requires CSS layout,
web-style typography, or a complex cover that ReportLab would make fragile.
Still render and inspect final pages.
