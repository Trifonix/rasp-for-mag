"""Минимальный Web-UI: HTML-форма, JS-валидация, поиск фильмов (аналог servlet/JSP)."""
from __future__ import annotations

import html
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

# Вымышленная БД MovieActor
MOVIES = [
    {"title": "Birdcage", "actor": "Robin Williams", "director": "Mike Nichols"},
    {"title": "The Matrix", "actor": "Keanu Reeves", "director": "Wachowski"},
    {"title": "Inception", "actor": "Leonardo DiCaprio", "director": "Christopher Nolan"},
    {"title": "Pulp Fiction", "actor": "John Travolta", "director": "Quentin Tarantino"},
    {"title": "Amelie", "actor": "Audrey Tautou", "director": "Jean-Pierre Jeunet"},
    {"title": "The Godfather", "actor": "Marlon Brando", "director": "Francis Coppola"},
    {"title": "Interstellar", "actor": "Matthew McConaughey", "director": "Christopher Nolan"},
    {"title": "La La Land", "actor": "Ryan Gosling", "director": "Damien Chazelle"},
]

HOST, PORT = "127.0.0.1", 8765


def page_shell(title: str, body: str) -> bytes:
    doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
  body {{ font-family: Segoe UI, Arial, sans-serif; margin: 24px; background: #f6f7f9; color: #222; }}
  .box {{ background: #fff; border: 1px solid #ccd; padding: 18px 22px; max-width: 820px; }}
  h1 {{ font-size: 1.35rem; margin: 0 0 12px; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 10px; }}
  th, td {{ border: 1px solid #99a; padding: 6px 10px; text-align: left; }}
  th {{ background: #e8ecf2; }}
  .nav a {{ margin-right: 12px; }}
  .muted {{ color: #555; font-size: 0.92rem; }}
  .err {{ color: #a00; font-weight: 600; }}
</style>
</head>
<body>
<div class="box">
{body}
</div>
</body>
</html>"""
    return doc.encode("utf-8")


INDEX_BODY = """
  <div class="nav">
    <a href="/">Поиск</a>
    <a href="/movies">Все фильмы (JSP-вид)</a>
    <a href="/validate">Проверка процента (JS)</a>
  </div>
  <h1>Testing MovieSearcher Servlet</h1>
  <p class="muted">Аналог листинга 1 методички: HTML-форма → POST /SearchMovie</p>
  <form method="post" action="/SearchMovie" name="searchForm"
        onsubmit="return checkSearch();">
    <table border="0" width="70%">
      <tr>
        <td>Search movies by:</td>
        <td>
          <select name="searchBy">
            <option value="TitleV">Title</option>
            <option value="ActorV">Actor</option>
            <option value="DirectorV">Director</option>
          </select>
        </td>
        <td><input name="searchField" type="text" size="28"></td>
      </tr>
      <tr>
        <td></td>
        <td>
          <input type="submit" value="Submit">
          <input type="reset" value="Clear">
        </td>
      </tr>
    </table>
  </form>
  <script>
  function checkSearch() {
    var v = document.searchForm.searchField.value.trim();
    if (!v) {
      alert("Введите значение поиска (клиентская проверка JavaScript)");
      return false;
    }
    if (v.length < 2) {
      alert("Слишком короткое значение: минимум 2 символа");
      return false;
    }
    return true;
  }
  </script>
"""

VALIDATE_BODY = """
  <div class="nav">
    <a href="/">Поиск</a>
    <a href="/movies">Все фильмы (JSP-вид)</a>
    <a href="/validate">Проверка процента (JS)</a>
  </div>
  <h1>Form Validation (JavaScript)</h1>
  <p class="muted">Аналог листинга 2: onSubmit → checkIt(0, 100)</p>
  <script>
  function checkIt(lower, upper) {
    var strval = document.sampleForm.percent.value;
    var intval = parseInt(strval, 10);
    if (lower < intval && intval < upper) {
      return true;
    }
    alert("Input " + strval + " is out of " + lower + "-" + upper + " range");
    return false;
  }
  </script>
  <form name="sampleForm" method="post" action="/percentOK"
        onsubmit="return checkIt(0, 100);">
    Percentage given:
    <input type="text" name="percent" value="1">
    <input type="submit" value="Submit">
  </form>
"""


def search_movies(by: str, field: str) -> list[dict]:
    q = field.strip().lower()
    key = {"TitleV": "title", "ActorV": "actor", "DirectorV": "director"}.get(by, "title")
    return [m for m in MOVIES if q in m[key].lower()]


def render_results(by: str, field: str, rows: list[dict]) -> bytes:
    label = {"TitleV": "Title", "ActorV": "Actor", "DirectorV": "Director"}.get(by, by)
    if rows:
        trs = "".join(
            f"<tr><td>{html.escape(m['title'])}</td>"
            f"<td>{html.escape(m['actor'])}</td>"
            f"<td>{html.escape(m['director'])}</td></tr>"
            for m in rows
        )
        table = (
            "<table><tr><th>Movie Title</th><th>Main actor</th><th>Director</th></tr>"
            f"{trs}</table>"
        )
    else:
        table = '<p class="err">Ничего не найдено.</p>'
    body = f"""
  <div class="nav">
    <a href="/">Поиск</a>
    <a href="/movies">Все фильмы (JSP-вид)</a>
  </div>
  <h1>SearchMovie (servlet-ответ)</h1>
  <p>Критерий: <b>{html.escape(label)}</b>, значение: <b>{html.escape(field)}</b>,
     найдено: <b>{len(rows)}</b></p>
  {table}
  <p><a href="/">Вернуться к форме</a></p>
"""
    return page_shell("Search results", body)


def render_all_movies() -> bytes:
    trs = "".join(
        f"<tr><td>{html.escape(m['title'])}</td>"
        f"<td>{html.escape(m['actor'])}</td>"
        f"<td>{html.escape(m['director'])}</td></tr>"
        for m in MOVIES
    )
    body = f"""
  <div class="nav">
    <a href="/">Поиск</a>
    <a href="/movies">Все фильмы (JSP-вид)</a>
    <a href="/validate">Проверка процента (JS)</a>
  </div>
  <h1>The database content</h1>
  <p class="muted">Аналог HTML-выхода JSP (листинг 4 / рис. 11): таблица фильмов</p>
  <table border="2">
    <tr><th>Movie Title</th><th>Main actor</th><th>Director</th></tr>
    {trs}
  </table>
  <p>Click <a href="/">here</a> to go to main page.</p>
"""
    return page_shell("Movie JSP", body)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def _send(self, data: bytes, code: int = 200, ctype: str = "text/html; charset=utf-8") -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send(page_shell("Testing MovieSearcher Servlet", INDEX_BODY))
        elif path == "/movies":
            self._send(render_all_movies())
        elif path == "/validate":
            self._send(page_shell("Form Validation", VALIDATE_BODY))
        else:
            self._send(page_shell("404", "<h1>404</h1><p><a href='/'>Home</a></p>"), 404)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        form = urllib.parse.parse_qs(raw)
        path = urllib.parse.urlparse(self.path).path

        if path == "/SearchMovie":
            by = (form.get("searchBy") or ["TitleV"])[0]
            field = (form.get("searchField") or [""])[0]
            rows = search_movies(by, field)
            self._send(render_results(by, field, rows))
            return

        if path == "/percentOK":
            percent = (form.get("percent") or [""])[0]
            body = f"""
  <h1>Процент принят</h1>
  <p>Значение <b>{html.escape(percent)}</b> прошло клиентскую проверку checkIt(0, 100)
     и отправлено на сервер (method=post).</p>
  <p><a href="/validate">Назад</a></p>
"""
            self._send(page_shell("OK", body))
            return

        self._send(b"Bad request", 400, "text/plain; charset=utf-8")


def main() -> None:
    server = HTTPServer((HOST, PORT), Handler)
    print(f"MovieSearcher demo: http://{HOST}:{PORT}/")
    print("Ctrl+C to stop")
    server.serve_forever()


if __name__ == "__main__":
    main()
