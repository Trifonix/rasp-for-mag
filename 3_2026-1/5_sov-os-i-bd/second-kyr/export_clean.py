# -*- coding: utf-8 -*-
"""Выгрузка основного текста курсовой для антиплагиата."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
tex = (ROOT / "main.tex").read_text(encoding="utf-8")
m = re.search(r"%<\*plagiarism>(.*?)%\*</plagiarism>", tex, re.S)
if not m:
    raise SystemExit("plagiarism markers not found")
body = m.group(1)

lines = []
for line in body.splitlines():
    if "%" in line:
        out = []
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            out.append(line[i])
            i += 1
        line = "".join(out)
    lines.append(line)
body = "\n".join(lines)

for env in ("itemize", "enumerate", "flushleft"):
    body = body.replace("\\begin{" + env + "}", "")
    body = body.replace("\\end{" + env + "}", "")

body = re.sub(r"\\item\s*", "- ", body)
body = re.sub(r"\\(textbf|textit|texttt|emph)\{([^{}]*)\}", r"\2", body)
body = re.sub(r"\\url\{([^{}]*)\}", r"\1", body)
body = re.sub(
    r"\\(chapter|section|subsection)\*?\{([^{}]*)\}",
    lambda mo: "\n\n" + mo.group(2) + "\n\n",
    body,
)
body = re.sub(r"\\addcontentsline\{[^{}]*\}\{[^{}]*\}\{[^{}]*\}", "", body)
body = re.sub(r"\\[a-zA-Z]+\*?", "", body)
body = body.replace("~", " ")
body = body.replace("{", "").replace("}", "")
body = re.sub(r"\n{3,}", "\n\n", body)
body = re.sub(r"[ \t]+\n", "\n", body)

out_name = sys.argv[1] if len(sys.argv) > 1 else "Trifonov_OSiBD_Course-2-work_clean.txt"
out = ROOT / out_name
out.write_text(body.strip() + "\n", encoding="utf-8")
print("written", out, "chars", len(body))
