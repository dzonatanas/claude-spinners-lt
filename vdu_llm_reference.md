# Vietiniai VDU lietuviškų LLM modeliai — aprašas ir naudojimo instrukcija

Šie modeliai buvo atsisiųsti ir išbandyti 2026-09-05 kito projekto (Facebook komiksų
duomenų analizės) metu. Aplinka jau paruošta ir veikianti — nereikia iš naujo diegti,
tik paleisti.

## Aplinka

- **Katalogas**: `D:\VDU_LLM\`
- **Venv**: `D:\VDU_LLM\venv` (CPU-only PyTorch 2.14.0+cpu + transformers 5.16.1, jau įdiegta, patikrinta veikianti 2026-09-08)
- **HF cache**: `D:\VDU_LLM\hf_cache` (modeliai jau atsisiųsti, veikia offline)
- **Aparatūra, kuria testuota**: i7-8700 (6c/12t), 32GB RAM, be atskiro GPU (Intel UHD 630) — CPU-only inference patvirtinta pakankama abiem modeliams.
- Paleidimas: `D:\VDU_LLM\venv\Scripts\python.exe skriptas.py` (arba aktyvuok venv įprastai).
- **Būtina** kiekvieno skripto pradžioje: `os.environ["HF_HOME"] = r"D:\VDU_LLM\hf_cache"` PRIEŠ importuojant `transformers` — kitaip bandys atsisiųsti iš naujo į numatytąjį kelią.

## Modelis 1: `VSSA-SDSA/LT-MLKM-modernBERT` (encoder, 159.5M parametrų)

```python
from transformers import AutoTokenizer, AutoModel
tok = AutoTokenizer.from_pretrained("VSSA-SDSA/LT-MLKM-modernBERT")
model = AutoModel.from_pretrained("VSSA-SDSA/LT-MLKM-modernBERT")
inputs = tok(["frazė vienas", "frazė du"], return_tensors="pt", padding=True)
out = model(**inputs)
emb = out.last_hidden_state.mean(dim=1)  # paprastas mean-pooling
```

**Paskirtis**: teksto embeddingai/panašumo matavimas.
**Statusas — NEPATIKIMAS panašumui/semantikai be papildomo apmokymo.** Testuota: žalia
(be fine-tuning) `mean_pooling` embeddingai neteisingai reitingavo NESUSIJUSIŲ frazių porą
(„nerti nerimą" vs „sūrus reikalas", cosine 0.832) kaip PANAŠESNĘ už tikrai susijusią
porą („nerti nerimą" vs „nerimastingas nėrimas", cosine 0.738). T.y. žalias encoderis be
kontrastinio apmokymo NETINKA panašumo/klasterizavimo užduotims.
**Kam GALĖTŲ tikti**: žaliavinis teksto tokenizavimas/embeddingas kaip featurų šaltinis
kitam apmokytam sluoksniui, arba paprasčiausiai kaip lietuviškas tokenizeris, jei
prireiktų — bet NE tiesioginiam semantinio panašumo sprendimui.

## Modelis 2: `VSSA-SDSA/LT_AI_DLKVM` (generative/causal LM, 1.04B parametrų)

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
tok = AutoTokenizer.from_pretrained("VSSA-SDSA/LT_AI_DLKVM")
model = AutoModelForCausalLM.from_pretrained("VSSA-SDSA/LT_AI_DLKVM", dtype=torch.bfloat16)
model.eval()

inputs = tok("Tavo prompt'as:", return_tensors="pt")
with torch.no_grad():
    out = model.generate(
        **inputs, max_new_tokens=60,
        do_sample=False,               # arba do_sample=True, temperature=0.7, top_p=0.9
        repetition_penalty=1.3,        # BŪTINA - be šito modelis kartoja tą patį fragmentą į begalybę
        no_repeat_ngram_size=3,        # BŪTINA - papildoma apsauga nuo kartojimosi
    )
text = tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
```

**Greitis (CPU)**: ~5 tok/s — tinka trumpiems, ne realaus laiko poreikiams (batch/offline).

**KRITIŠKAI SVARBU — dekodavimo parametrai**: be `repetition_penalty` (rekomenduoju 1.2–1.3)
IR `no_repeat_ngram_size=3`, modelis patenka į begalinę to paties fragmento kartojimosi
kilpą. Su šiais parametrais problema pilnai išsprendžiama.

**Statusas — geras generavimui/kūrybai, NEPATIKIMAS faktams.** Su ištaisytu dekodavimu
modelis generuoja SKLANDŲ, gramatiškai teisingą lietuvišką tekstą, BET kai klausta
faktinės informacijos (žodžių etimologijos ir pan.), fabrikuoja įtikinamai skambančius,
BET NETEISINGUS faktus (išgalvojo lotynišką „nerti" kilmę, klaidingai teigė „sūris" kilus
iš graikų k.). **Tai NĖRA problema kūrybinėms/generatyvinėms užduotims** (pvz. žodžių
sąrašo generavimas, sinonimų/variantų siūlymas, stiliaus imitacija) — ten fabrikacija
tiesiog reiškia „modelis sugalvojo įdomų variantą", ne klaidą. Problema iškyla TIK jei
prašai patikimų FAKTŲ (istorija, kilmė, apibrėžimai) be žmogaus peržiūros.

## Rekomendacija konkrečiai užduočiai („Lithuanian localization for spinner verbs")

Tai generatyvi/kūrybinė užduotis (reikia sąrašo lietuviškų veiksmažodžių/gerundijų,
stilistiškai tinkamų spinner'io tekstams, ne faktinio patikrinimo) — **`LT_AI_DLKVM`
generatyvus modelis tam tinka gerai**, būtent dėl to, kad fabrikacijos rizika čia
nereiškia klaidos. Naudok jį kaip papildomą variantų/idėjų šaltinį (pvz. prompt'ink
"Sugalvok N lietuviškų veiksmažodžių/gerundijų, tinkančių trumpam 'įkeliama...' tipo
pranešimui" arba pateik anglų kalbos veiksmažodžių sąrašą ir prašyk vertimo/lokalizacijos
variantų), BET **kiekvieną pasiūlymą peržiūrėk pats/su Jonu** prieš naudojant — modelio
lietuvių kalbos GRAMATIKA patikima, bet STILISTINIS tinkamumas/natūralumas gali svyruoti
(vis dėlto tai 1B modelis, ne didelis komercinis LLM), o esamas Claude (tu pats) tikriausiai
duos geresnius/natūralesnius vertimus be papildomo modelio apskritai — VDU modelis geriausiai
tinka kaip DIVERSIFIKACIJOS/įkvėpimo šaltinis papildomiems variantams, ne pirminis vertėjas.

## Žinomi apribojimai (neišspręsti, nereikėjo šiai užduočiai)

- Koderio (modelis 1) panašumo funkcija nepatikima be fine-tuning — nenaudok klasterizavimui/
  panašumo paieškai be papildomo apmokymo.
- Generatyvus (modelis 2) fabrikuoja faktus — nenaudok kaip vienintelio šaltinio faktinei
  informacijai be žmogaus peržiūros.
- Abu modeliai CPU-only testuoti šiame kompiuteryje — jei kita sesija veikia kitame
  kompiuteryje/aplinkoje, `D:\VDU_LLM\` kelias ir jau atsisiųsti modeliai ten NEPASIEKIAMI,
  reikėtų iš naujo `pip install torch transformers` + `from_pretrained(...)` (atsisius iš HF).
