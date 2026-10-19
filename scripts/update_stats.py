import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape

login = "andreborges19"
headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"}
if os.environ.get("GH_TOKEN"):
    headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]

def fetch(path):
    with urlopen(Request("https://api.github.com" + path, headers=headers), timeout=20) as resp:
        return json.load(resp)

user = fetch("/users/" + login)
repos = []
page = 1
while page <= 10:
    part = fetch(f"/users/{login}/repos?per_page=100&page={page}&type=owner")
    repos += part
    if len(part) < 100:
        break
    page += 1

public_repos = sum(1 for r in repos if not r.get("private"))
stars = sum(r.get("stargazers_count", 0) for r in repos if not r.get("fork"))
followers = user.get("followers", 0)
updated = datetime.now(timezone.utc).strftime("%d/%m/%Y")
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="550" height="205" viewBox="0 0 550 205" role="img">
<title>Estatísticas públicas do GitHub de André Carvalho</title>
<rect width="550" height="205" rx="12" fill="#0d1117" stroke="#30363d"/>
<rect x="24" y="23" width="5" height="28" rx="2" fill="#20a9c1"/>
<text x="42" y="45" font-family="Arial,Helvetica,sans-serif" fill="#e6edf3" font-size="24" font-weight="bold">GitHub Stats</text>
<text x="25" y="75" font-family="Arial,Helvetica,sans-serif" fill="#8b949e" font-size="14">André Carvalho</text>
<text x="26" y="115" font-family="Arial,Helvetica,sans-serif" fill="#9da7b3" font-size="14">REPOSITÓRIOS PÚBLICOS</text>
<text x="26" y="149" font-family="Arial,Helvetica,sans-serif" fill="#e6edf3" font-weight="bold" font-size="29">{public_repos}</text>
<text x="225" y="115" font-family="Arial,Helvetica,sans-serif" fill="#9da7b3" font-size="14">ESTRELAS RECEBIDAS</text>
<text x="225" y="149" font-family="Arial,Helvetica,sans-serif" fill="#e6edf3" font-weight="bold" font-size="29">{stars}</text>
<text x="445" y="115" font-family="Arial,Helvetica,sans-serif" fill="#9da7b3" font-size="14">SEGUIDORES</text>
<text x="445" y="149" font-family="Arial,Helvetica,sans-serif" fill="#e6edf3" font-weight="bold" font-size="29">{followers}</text>
<line x1="25" y1="164" x2="525" y2="164" stroke="#30363d"/>
<text x="25" y="187" font-family="Arial,Helvetica,sans-serif" fill="#8b949e" font-size="12">Dados públicos · Atualizado em {updated} (UTC)</text>
</svg>
"""
Path("assets").mkdir(exist_ok=True)
Path("assets/github-stats.svg").write_text(svg, encoding="utf-8")
