"""ADDENDUM-19b: identisk ADDENDUM-19, men max_tokens 2 000. Første kjøring var ugyldig på avkutting."""
import re, json, subprocess, time, hashlib, sys
from pathlib import Path
REPO=Path.home()/"dev/gjenopptak"
UT=Path('/Volumes/Vault/gjenopptak-kilder/ekstraksjon/2026-09-26/addendum-19'); UT.mkdir(parents=True, exist_ok=True)
ASHA="fb0410e3b1225b60613cb430376f927f22d3bbb896d4f5e718c6a7d369890223"
def nokkel():
    for l in (Path.home()/'.zshenv').read_text(encoding='utf-8').splitlines():
        m=re.match(r'\s*(?:export\s+)?ANTHROPIC_API_KEY_NORDVAULT\s*=\s*(.*)$', l)
        if m: return m.group(1).strip().strip('"').strip("'")
    raise SystemExit("ingen nøkkel")
REGLER=Path('/Volumes/Vault/gjenopptak-kilder/koder2/koderegler-gjenvunnet.md').read_text(encoding='utf-8')
RSHA=hashlib.sha256(REGLER.encode()).hexdigest()
assert RSHA=="234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449", RSHA
SYSTEM=[{"type":"text",
  "text": REGLER + "\n\n---\n\nDu får én tekstbit om gangen. Avgjør om den er et TREFF etter reglene over. "
          "Svar bare med JSON på én linje: {\"treff\": true|false, \"begrunnelse\": \"<én setning>\"}. "
          "Ingen annen tekst.",
  "cache_control":{"type":"ephemeral"}}]
def _post(k, payload):
    body=json.dumps(payload).encode()
    r=subprocess.run(["curl","-sS","-o","-","-w","\n%{http_code}","-X","POST",
        "https://api.anthropic.com/v1/messages","-H","content-type: application/json",
        "-H","anthropic-version: 2023-06-01","-H",f"x-api-key: {k}","--data-binary","@-"],
        input=body, capture_output=True, timeout=180)
    ut=r.stdout.decode(); i=ut.rfind("\n")
    return ut[i+1:].strip(), ut[:i]
def kall(k, modell, tekst):
    base={"model":modell,"max_tokens":2000,"system":SYSTEM,"messages":[{"role":"user","content":tekst}]}
    kode,svar=_post(k, dict(base, temperature=0))
    if kode=="400" and "temperature" in svar:
        kode,svar=_post(k, base); return kode, svar, True
    return kode, svar, False
if __name__=="__main__":
    modell=sys.argv[1]; kort=sys.argv[2]
    k=nokkel()
    rader=[json.loads(x) for x in (REPO/'data/port-presisjonssett-ADDENDUM10.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    logg=UT/f'{kort}-dommer.jsonl'; gjort=set()
    if logg.is_file():
        for l in logg.read_text(encoding='utf-8').splitlines():
            if l.strip(): gjort.add(json.loads(l)['id'])
    print(f"{modell}: {len(rader)} tekstbiter · ferdig fra før {len(gjort)} · regel-sha {RSHA[:16]} "
          f"({len(REGLER.encode()):,} B)", flush=True)
    t0=time.time(); inn=ut_=cc=cr=0; feil=0
    with logg.open('a', encoding='utf-8') as f:
        for i,r in enumerate(rader,1):
            if r['id'] in gjort: continue
            kode,svar,utelatt=kall(k, modell, r['tekst'])
            if not kode.startswith("2"):
                feil+=1; print(f"  HTTP {kode} på {r['id']}", flush=True)
                if kode in ("401","403"): print("STOPP: 401/403", flush=True); break
                time.sleep(5); continue
            d=json.loads(svar)
            txt=" ".join(b.get('text','') for b in d.get('content',[]))
            u=d.get('usage',{})
            inn+=u.get('input_tokens',0); ut_+=u.get('output_tokens',0)
            cc+=u.get('cache_creation_input_tokens',0) or 0; cr+=u.get('cache_read_input_tokens',0) or 0
            f.write(json.dumps(dict(id=r['id'], utvalgstype=r['utvalgstype'], modell=d.get('model'),
                signatur=dict(model_id=d.get('model'),
                              temperature=("utelatt — deprecated for denne modellen" if utelatt else 0),
                              temperature_utelatt=utelatt, max_tokens=2000,
                              regel_sha256=RSHA, regelfil="koder2/koderegler-gjenvunnet.md",
                              hurtigbuffer="cache_control ephemeral på systemblokken",
                              addendum="ADDENDUM-19b", addendum_sha256=ASHA),
                usage=u, raasvar=txt.strip()), ensure_ascii=False)+"\n"); f.flush()
            if i%50==0: print(f"  {i}/{len(rader)}  {(time.time()-t0)/60:.1f} min  inn {inn:,} ut {ut_:,} "
                              f"buffer skrevet {cc:,} lest {cr:,}", flush=True)
    print(f"FERDIG {modell}: {(time.time()-t0)/60:.1f} min · inn {inn:,} ut {ut_:,} · "
          f"buffer skrevet {cc:,} lest {cr:,} · HTTP-feil {feil}", flush=True)
