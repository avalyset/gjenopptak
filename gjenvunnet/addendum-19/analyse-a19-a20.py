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
def les(p):
    if not p.is_file(): return None,0,None
    rader=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
    d={}; up=0
    for r in rader:
        q=parse(r['raasvar'])
        if q is None or 'treff' not in q: up+=1; continue
        d[r['id']]=bool(q['treff'])
    return d, up, rader
print("=== FULL REGELFIL (234695dd), ETT KALL PER PASSASJE — mot koder 1 ===")
print(f"{'modell':16}{'dømt':7}{'upars':7}{'n':6}{'rå':8}{'κ':8}{'95 % KI':18}{'utfall'}")
ut={}
for navn,p in (("Opus 5", U/'addendum-19/opus5-dommer.jsonl'),
               ("Sonnet 5", U/'addendum-20/sonnet5-dommer.jsonl'),
               ("Haiku 4.5", U/'addendum-20/haiku45-dommer.jsonl')):
    d,up,rader=les(p)
    if d is None: print(f"{navn:16}mangler"); continue
    felles=sorted(i for i in d if i in k1)
    a=[k1[i] for i in felles]; b=[d[i] for i in felles]
    kap=cohen_kappa(a,b); lo,hi=kappa_bootstrap(a,b,n_rep=10_000,seed=734248)
    t={(True,True):0,(True,False):0,(False,True):0,(False,False):0}
    for x,y in zip(a,b): t[(x,y)]+=1
    inn=sum(r['usage'].get('input_tokens',0) for r in rader); utt=sum(r['usage'].get('output_tokens',0) for r in rader)
    cr=sum(r['usage'].get('cache_read_input_tokens',0) or 0 for r in rader)
    cc=sum(r['usage'].get('cache_creation_input_tokens',0) or 0 for r in rader)
    print(f"{navn:16}{len(rader):<7}{up:<7}{len(felles):<6}{100*ra_enighet(a,b):<7.1f}{kap:<8.3f}{f'[{lo:.3f}–{hi:.3f}]':<18}"
          f"{'LEVER' if kap>=0.70 else 'UNDER 0,70'}")
    print(f"{'':16}2×2: k1+kand+ {t[(True,True)]} · k1+kand− {t[(True,False)]} · k1−kand+ {t[(False,True)]} · begge− {t[(False,False)]}"
          f"  ·  flagget {sum(b)} treff")
    print(f"{'':16}tokens: inn {inn:,} · ut {utt:,} · buffer skrevet {cc:,} lest {cr:,}")
    ut[navn]=dict(d=d, kappa=round(kap,4), bootstrap=[round(lo,4),round(hi,4)], n=len(felles),
      domt=len(rader), uparsede=up, raa=round(ra_enighet(a,b),4), flagget=sum(b),
      tabell={"k1+kand+":t[(True,True)],"k1+kand-":t[(True,False)],"k1-kand+":t[(False,True)],"k1-kand-":t[(False,False)]},
      tokens=dict(inn=inn, ut=utt, buffer_skrevet=cc, buffer_lest=cr))
print("\n=== ADDENDUM-19s KRITERIUM: hvor faller Opus? ===")
o=ut.get("Opus 5")
if o:
    k=o['kappa']
    if 0.712<=k<=0.917: dom="INNENFOR koder 2s intervall 0,712–0,917 → MODELLEN er forklaringen"
    elif k>=0.70: dom="≥ 0,70 men utenfor intervallet → modellen bærer det meste, øktformen noe"
    elif k>=0.30: dom="0,30–0,70 → begge bidrar, ingen enkel forklaring står"
    else: dom="UNDER 0,30, i Haikus og Sonnets klasse → ØKTFORMEN er forklaringen"
    print(f"  κ = {k:.3f} → {dom}")
    print(f"  koder 2 (Opus, samme regelfil, ÉN SAMMENHENGENDE ØKT): κ = 0,812 [0,712–0,917]")
print("\n=== Sonnet: tynt utdrag mot full regelfil, paret ===")
d18,_,_=les(U/'addendum-18/sonnet5-pass1-dommer.jsonl')
d20=ut.get("Sonnet 5",{}).get('d')
if d18 and d20:
    par=sorted(set(d18)&set(d20)&set(k1))
    R=[k1[i] for i in par]; A=[d18[i] for i in par]; B=[d20[i] for i in par]
    kA=cohen_kappa(R,A); kB=cohen_kappa(R,B)
    random.seed(734248); dd=[]
    for _ in range(10000):
        idx=[random.randrange(len(par)) for _ in par]
        dd.append(cohen_kappa([R[i] for i in idx],[B[i] for i in idx])-cohen_kappa([R[i] for i in idx],[A[i] for i in idx]))
    dd.sort()
    print(f"  {len(par)} felles · to kilder κ = {kA:.3f} (flagget {sum(A)}) · seks kilder κ = {kB:.3f} (flagget {sum(B)})")
    print(f"  differanse {kB-kA:+.3f} · paret bootstrap [{dd[250]:+.3f}–{dd[9750]:+.3f}] "
          f"{'INNEHOLDER 0' if dd[250]<0<dd[9750] else 'UTELUKKER 0'}")
for v in ut.values(): v.pop('d',None)
(U/'a19-a20-full-regelfil.json').write_text(json.dumps(ut, ensure_ascii=False, indent=1), encoding='utf-8')
print(f"\nskrevet {U/'a19-a20-full-regelfil.json'}")
