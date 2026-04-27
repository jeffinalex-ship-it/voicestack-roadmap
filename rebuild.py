import csv, json, re
from datetime import datetime

def norm_area(a):
    a = (a or "").strip()
    if "phone" in a.lower(): return "Phone System"
    if "call intel" in a.lower(): return "Call Intelligence"
    if a.lower() == "crm": return "CRM"
    if "voicebot" in a.lower() or "ai agent" in a.lower(): return "AI Agents"
    if "platform" in a.lower(): return "Platform"
    return "Other" if not a else a

def norm_qtr(q):
    q = (q or "").strip().upper()
    if q in ["Q1","Q2","Q3","Q4"]: return q
    if "ONGOING" in q or "ON-GOING" in q: return "Ongoing"
    return "TBD"

def norm_status(s):
    s = (s or "").strip()
    if s.lower() == "deployed": return "Deployed"
    if "progress" in s.lower(): return "In Progress"
    if "backlog" in s.lower(): return "Backlog"
    if "hold" in s.lower(): return "On Hold"
    if "ongoing" in s.lower(): return "Ongoing"
    return "TBD"

def clean(d):
    return " ".join((d or "").replace("\n", " ").split())[:300]

with open("roadmap.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

items = []
for r in rows:
    name = (r.get("Offering") or "").strip()
    if not name:
        continue
    items.append({
        "name": name,
        "area": norm_area(r.get("Area", "")),
        "quarter": norm_qtr(r.get("Which Quarter", "")),
        "status": norm_status(r.get("Status", "")),
        "type": (r.get("Sub-Area") or "").strip(),
        "geo": (r.get("Release Geographies") or "").strip(),
        "vertical": (r.get("Vertical") or "").strip(),
        "desc": clean(r.get("Description", ""))
    })

print(f"Parsed {len(items)} items from CSV")

with open("template_before.html", encoding="utf-8") as f:
    before = f.read()
with open("template_after.html", encoding="utf-8") as f:
    after = f.read()

today = datetime.now().strftime("%B %Y")
data_js = "const DATA = " + json.dumps(items, ensure_ascii=False) + ";"
html = before + data_js + after
html = re.sub(r"Last updated \w+ \d{4}", f"Last updated {today}", html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"index.html rebuilt ({len(html):,} bytes)")
