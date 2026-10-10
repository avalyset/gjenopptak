import json, re, sys, random
from pathlib import Path
sys.path.insert(0,'src')
from gjenopptak.classify.reliabilitet import cohen_kappa, kappa_bootstrap, ra_enighet
REPO=Path.home()/"dev/gjenopptak"; U=Path('/Volumes/Vault/gjenopptak-kilder/ekstraksjon/2026-09-26')
rows=[json.loads(x) for x in (REPO/'data/port-presisjonssett-ADDENDUM10.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
k1={r['id']:bool(r.get('ekte_treff')) for r in rows}; typ={r['id']:r['utvalgstype'] for r in rows}
def parse(s):
    m=re.search(r'\{.*?\}', s.strip(), re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None
def les(p, ekstra=None):
    rader=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
    if ekstra and ekstra.is_file():
        rader += [json.loads(x) for x in ekstra.read_text(encoding='utf-8').splitlines() if x.strip()]
    d={}; up=0; avk=0
    for r in rader:
        q=parse(r['raasvar'])
        if q is None or 'treff' not in q:
            up+=1
            if (r['usage'].get('output_tokens',0) or 0) >= r['signatur'].get('max_tokens',300): avk+=1
            continue
        d[r['id']]=bool(q['treff'])   # rekjørt rad kommer sist og overskriver
    return d, up, avk, rader
def mål(navn, d, up, avk, rader, tak):
    felles=sorted(i for i in d if i in k1)
    a=[k1[i] for i in felles]; b=[d[i] for i in felles]
    kap=cohen_kappa(a,b); lo,hi=kappa_bootstrap(a,b,n_rep=10_000,seed=734248)
    t={(True,True):0,(True,False):0,(False,True):0,(False,False):0}
    for x,y in zip(a,b): t[(x,y)]+=1
    ut=sorted(r['usage'].get('output_tokens',0) or 0 for r in rader)
    print(f"{navn:34}{tak:>7}{len(rader):>7}{up:>8}{avk:>6}{len(felles):>6}{100*ra_enighet(a,b):>7.1f}{kap:>8.3f}  [{lo:.3f}–{hi:.3f}]")
    print(f"{'':34}2×2: k1+k+ {t[(True,True)]} · k1+k− {t[(True,False)]} · k1−k+ {t[(False,True)]} · begge− {t[(False,False)]}"
          f" · flagget {sum(b)} · median ut {ut[len(ut)//2]} · maks ut {ut[-1]}")
    return dict(kappa=round(kap,4), bootstrap=[round(lo,4),round(hi,4)], n=len(felles), uparsede=up,
                avkuttede=avk, flagget=sum(b), domt=len(rader),
                tabell={"k1+k+":t[(True,True)],"k1+k-":t[(True,False)],"k1-k+":t[(False,True)],"k1-k-":t[(False,False)]}), d
print(f"\n{'kjøring':34}{'tak':>7}{'rader':>7}{'upars':>8}{'avk':>6}{'n':>6}{'rå':>7}{'κ':>8}  95 % KI")
print("-"*105)
res={}
d,up,avk,r_ = les(U/'addendum-19/opus5-dommer.jsonl');            res['opus_300'],_ = mål("ADDENDUM-19 Opus, tak 300 UGYLDIG", d,up,avk,r_,300)
d,up,avk,r_ = les(U/'addendum-19/opus5-b-dommer.jsonl');          res['opus_2000'],dop = mål("ADDENDUM-19b Opus, tak 2 000", d,up,avk,r_,2000)
d,up,avk,r_ = les(U/'addendum-18/sonnet5-pass1-dommer.jsonl');    res['sonnet18_før'],_ = mål("ADDENDUM-18 Sonnet p1, før rekjøring", d,up,avk,r_,300)
d,up,avk,r_ = les(U/'addendum-18/sonnet5-pass1-dommer.jsonl', U/'addendum-18/sonnet5-pass1-avkuttet-rekjort.jsonl')
res['sonnet18_etter'],_ = mål("ADDENDUM-18 Sonnet p1, MED rekjørte", d,up,avk,r_,'300→2000')
d,up,avk,r_ = les(U/'addendum-18/haiku45-dommer.jsonl');          res['haiku18_før'],_ = mål("ADDENDUM-18 Haiku, før rekjøring", d,up,avk,r_,300)
d,up,avk,r_ = les(U/'addendum-18/haiku45-dommer.jsonl', U/'addendum-18/haiku45-avkuttet-rekjort.jsonl')
res['haiku18_etter'],_ = mål("ADDENDUM-18 Haiku, MED rekjørt", d,up,avk,r_,'300→2000')
print("-"*105)
print(f"\n=== ADDENDUM-19s KRITERIUM anvendt på 19b (κ = {res['opus_2000']['kappa']}) ===")
k=res['opus_2000']['kappa']
if 0.712<=k<=0.917: dom="INNENFOR koder 2s intervall 0,712–0,917 → MODELLEN er forklaringen"
elif k>=0.70: dom="≥ 0,70 men utenfor intervallet → modellen bærer det meste"
elif k>=0.30: dom="0,30–0,70 → begge bidrar, ingen enkel forklaring står"
else: dom="UNDER 0,30 → ØKTFORMEN er forklaringen"
print(f"  {dom}")
print(f"  koder 2 (Opus, samme regelfil, ÉN SAMMENHENGENDE ØKT): κ = 0,812 [0,712–0,917]")
print(f"  ADDENDUM-19b (Opus, samme regelfil, 320 UAVHENGIGE KALL): κ = {k:.3f} {res['opus_2000']['bootstrap']}")
(U/'a19b-utfall.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print(f"\nskrevet {U/'a19b-utfall.json'}")
