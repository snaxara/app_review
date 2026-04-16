# -*- coding: utf-8 -*-
import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "tcc" / "TCC_31_03.md"
t = p.read_text(encoding="utf-8")
m = re.search(r"## Resumo\s*\n\n(.+?)\n\nPalavras-chave:", t, re.DOTALL)
if m:
    r = m.group(1).strip()
    words = re.findall(r"[\w'-]+", r, flags=re.UNICODE)
    print("Palavras (resumo):", len(words))

start, end = t.find("## Introdução"), t.find("## Referências")
body = t[start:end] if start >= 0 and end >= 0 else t
wbody = re.findall(r"[\w'-]+", body, flags=re.UNICODE)
print("Palavras corpo (Intro ate Referencias):", len(wbody))
for wpp in (250, 280, 300):
    print("  ~{:.1f} pags (aprox. {} palavras/pag., so texto)".format(len(wbody) / wpp, wpp))
