# Claude Spinners LT

Lietuviškas Claude Code spinner-veiksmažodžių (tų juokingų "Accomplishing", "Actioning"
tipo žodžių, rodomų kol Claude dirba) lokalizavimo projektas. Šaltinis —
[claudionary.com](https://claudionary.com/), pseudo-akademinis šių žodžių "žodynas".

## Tikslas

1. Sukurti `~/.claude/settings.json` su `spinnerVerbs` konfigūracija (lietuviškais žodžiais).
2. Sudaryti kūrybišką lietuvišką veiksmažodžių/gerundijų sąrašą, atitinkantį originalo
   žaismingą, absurdišką, pseudo-akademinį toną.
3. Parašyti lietuvišką "claudionary" stiliaus dokumentaciją (žaismingas žodynėlis su
   kiekvieno žodžio "etimologija"/apibrėžimu, ta pačia humoro linija kaip originale).

## Parsisiuntimas

Pirmiausia gauk repo turinį į savo kompiuterį — vienu iš dviejų būdų:

**A) Su git** (rekomenduojama, jei turi git įdiegtą):
```
git clone https://github.com/dzonatanas/claude-spinners-lt.git
cd claude-spinners-lt
```

**B) Be git** — atsisiųsk ZIP:
1. Eik į https://github.com/dzonatanas/claude-spinners-lt
2. Spausk žalią mygtuką **„Code"** → **„Download ZIP"**
3. Išarchyvuok ZIP failą bet kur savo kompiuteryje
4. Atsidaryk terminalą/Explorer tame išarchyvuotame kataloge

Toliau visos komandos žemiau paleidžiamos **iš to katalogo** (kur yra `README.md`,
`data/`, `install/` ir t.t.).

**Admin teisių nereikia.** `~/.claude/settings.json` yra tavo paties vartotojo profilio
kataloge (`%USERPROFILE%\.claude\settings.json`), ne sistemos lygmens vietoje — kiekvienas
standartinis Windows vartotojas ten turi pilnas rašymo teises be jokio administravimo.
„Globaliai" šiame projekte reiškia „globaliai tavo vartotojui šiame kompiuteryje", ne
visiems kompiuterio vartotojams. (Vienintelė išimtis — griežtai IT valdomi kompiuteriai su
užrakintais profiliais, bet tai nestandartinis atvejis.)

## Naudojimas

### Paprastas būdas — skriptas

**Windows:** tiesiog dukart paspausk `install/install.bat` (arba paleisk iš terminalo).
**macOS/Linux:**
```
install/install.sh
```
**Bet kuri OS (tiesiogiai):**
```
python install/install.py
```

Paklaus dviejų klausimų (kur diegti — globaliai ar konkrečiam projektui; ir `replace` ar
`append`), tada pats saugiai sujungs `spinnerVerbs` su tavo esamu `settings.json` (jei
toks jau yra — jo TURINYS nepradingsta, tik prisideda naujas raktas), padarydamas
`.bak` atsarginę kopiją prieš rašydamas. Reikalingas tik Python 3, jokių papildomų
bibliotekų — `install.bat`/`install.sh` patys patikrina ar `python`/`python3`/`py`
įdiegtas ir praneša, jei ne.

Neinteraktyviam naudojimui (pvz. automatizacijai):
```
python install/install.py --scope global --mode replace
python install/install.py --scope project --project-dir /kelias/iki/projekto --mode append
```

### Be Python (Windows arba macOS/Linux)

Jei Python neįdiegtas, `install/install_nopython.bat` (Windows) arba
`install/install_nopython.sh` (macOS/Linux) atlieka tą patį grynu batch/shell tekstu
(be jokių priklausomybių — shell versijai reikia tik standartinių `sh`, `sed`, `grep`
įrankių, kurie yra kiekviename macOS/Linux):
```
install\install_nopython.bat
install\install_nopython.bat project
install\install_nopython.bat project "C:\mano\projektas" append
install\install_nopython.bat global append
```
```
install/install_nopython.sh
install/install_nopython.sh project
install/install_nopython.sh project /mano/projektas append
install/install_nopython.sh global append
```
Be argumentų — numatytieji: globaliai, `replace`. Paklaus tik VIENO patvirtinimo
(Y/n) prieš rašydamas — sąmoningai vengiama kelių eilučių klausimų iš eilės (batch
versijoje `cmd.exe` `set /p` yra žinomai nepatikimas antram klausimui, jei skriptas
paleidžiamas ne iš tikros konsolės), tad scope/mode imami iš argumentų arba
numatytųjų reikšmių. Kiekvienas paleidimas daro **naują, numeruotą** atsarginę
kopiją (`.bak.1`, `.bak.2`, ...) — ankstesnės niekada neperrašomos. Po įrašymo
patikrina, ar rezultatas nėra trumpesnis už originalą (jei kažkas nutiktų
klaidingai — originalas paliekamas nepaliestas, praneša apie klaidą). Taip pat
įspėja, jei faile jau yra `spinnerVerbs` raktas (nepašalins seno, tik pridės naują —
išsivalyk ranka, jei nori švaraus failo).

**Batch versija gali užtrukti iki minutės** (kiekvieną žodį apdoroja atskirai) — tai
normalu, palauk; shell versija (`install_nopython.sh`) yra greita, nes `sed` dirba su
visu failu iš karto. `install.py`/`install.sh` (jei turi Python) yra dar saugesni —
jie tikrai perskaito/patikrina JSON turinį po įrašymo (ne tik eilučių skaičių), tad
naudok juos, jei nori stipriausios garantijos, kad niekas iš esamų nustatymų
(pvz. `statusLine`, `hooks`, teisės) neprapuls.

### Rankinis būdas

1. Atsidaryk `data/spinnerVerbs.settings.json` šiame repo — jame yra paruoštas
   `{"spinnerVerbs": {"mode": "replace", "verbs": [...]}}` blokas su visais 467 žodžiais.
2. Nuspręsk, kur jį dėti:
   - **Globaliai, visiems savo projektams šiame kompiuteryje** → `~/.claude/settings.json`
   - **Tik konkrečiam projektui** → `<projekto katalogas>/.claude/settings.json`
3. Jei tame faile jau yra kitų nustatymų (pvz. `theme`, `enabledPlugins`) — **NEPERRAŠYK**
   viso failo, o įklijuok tik `"spinnerVerbs": { ... }` raktą į jau esantį JSON objektą,
   kaip papildomą lauką šalia kitų.
4. Pasirink `mode`:
   - `"replace"` — rodys TIK lietuviškus žodžius (angliški numatytieji dingsta)
   - `"append"` — sujungs su 187 angliškais numatytaisiais, spinneris rodys mišinį
5. Išsaugok failą. **Pakeitimas pritaikomas iš karto**, be perkrovimo — Claude Code turi
   vidinį `settings_sync` mechanizmą, sekantį nustatymų failo pokyčius gyvai.

## Struktūra

```
claude-spinners-lt/
├── README.md              — šis failas
├── claudionary_lt.md       — žaismingas priedas (žr. žemiau)
├── LICENSE                 — MIT
├── data/                   — JSON duomenys
│   ├── claudionary_source.json
│   ├── spinner_verbs_lt_progress.json
│   └── spinnerVerbs.settings.json
├── scripts/                — pagalbiniai skriptai
│   ├── scrape_claudionary.py
│   └── scrape_dlkz.py
└── install/                — diegimo skriptai
    ├── install.py
    ├── install.bat
    ├── install.sh
    ├── install_nopython.bat
    └── install_nopython.sh
```

| Failas | Paskirtis |
|---|---|
| `scripts/scrape_claudionary.py` | Scraperis, ištraukiantis visą claudionary.com žodyną |
| `scripts/scrape_dlkz.py` | Scraperis, tikrinantis realius lietuviškus veiksmažodžius iš gyvo [DLKŽ](https://ekalba.lt/dabartines-lietuviu-kalbos-zodynas/) (naujų kandidatų paieškai) — reikalauja Playwright + Chromium (žr. skripto docstring dėl naudojimo/venv) |
| `data/claudionary_source.json` | Scraping rezultatas — **187 originalūs anglų kalbos įrašai** (word, ipa, pos, category, etymology, definition, diagram_caption, example) |
| `data/spinner_verbs_lt_progress.json` | **Darbo būklė** — visi iki šiol išversti/sukurti lietuviški žodžiai, sugrupuoti pagal semantines kategorijas |
| `data/spinnerVerbs.settings.json` | Paruoštas `{"spinnerVerbs": {"mode": "replace", "verbs": [...]}}` blokas (visi 467 žodžiai) — naudojamas diegimo skriptų arba rankiniam kopijavimui |
| `install/install.py` | Diegimo skriptas — automatiškai sujungia `spinnerVerbs` su tavo `settings.json`, klausdamas scope (global/project) ir mode (replace/append), darydamas atsarginę kopiją. Žr. „Naudojimas" žemiau |
| `install/install.bat` | Windows apvalkalas `install.py` — dukart paspaudus paleidžia skriptą (patikrina ar Python įdiegtas) |
| `install/install.sh` | macOS/Linux apvalkalas `install.py` — paleidžia skriptą iš terminalo (patikrina ar `python3`/`python` įdiegtas) |
| `install/install_nopython.bat` | Windows diegimas be Python — grynas batch tekstas, jokių priklausomybių. Žr. „Naudojimas" žemiau |
| `install/install_nopython.sh` | macOS/Linux diegimas be Python — grynas shell (`sh`/`sed`) tekstas, jokių priklausomybių. Žr. „Naudojimas" žemiau |
| `claudionary_lt.md` | **Žaismingas priedas** — 17 rinktinių žodžių pseudo-akademiniu claudionary.com stiliumi (etimologija, apibrėžimas, citata). Ne pilnas žodynas — tik geriausios istorijos; pagrindinis turinys visada yra `data/spinner_verbs_lt_progress.json` |
| `README.md` | Šis failas |

## Metodas

Žodžiai verčiami/kuriami **tiesiogiai Claude**, kategorija po kategorijos (ne masiškai visi
187 iš karto) — kartu su naudotoju peržiūrint ir koreguojant kiekvieną grupę prieš pereinant
prie kitos.

Galutinis sąrašas nėra griežtas 1:1 atitikmuo anglų kalbos žodžiams — tai laisvas žodžių
"baseinas" (`spinnerVerbs: { mode, verbs }` priima paprastą masyvą per `verbs`), tad kai
kuriems angliškiems žodžiams paliekami keli lietuviški variantai (pvz. Gusting →
Gūsiuoju/Vėjinu/Vėduoju/Vėsinu), o kai kurie lietuviški žodžiai neturi tiesioginio
angliško atitikmens (naudotojo pridėti papildymai).

**Rodymo mechanika**: kiekvieną kartą spinneris tiesiog atsitiktinai išrenka VIENĄ žodį
iš viso masyvo — jokio ryšio su
tuo, ką Claude tuo metu realiai daro. `mode: "append"` sujungia numatytuosius (187 EN) su
`verbs` sąrašu ir renkasi iš viso 654 žodžius (187+467); `mode: "replace"` rodo TIK `verbs` sąrašą.
Norint grynai lietuviško spinnerio — reikia `"replace"`.

### Papildomi žodžių šaltiniai

Nuo 2026-09-14, šalia tiesioginio Claude vertimo/kūrimo, dalis naujų žodžių atrenkama
iš realių lietuviškų žodynų/žodžių sąrašų (ne tik laisvai sugalvojama) — kiekvienas
tokio šaltinio žodis vis tiek eina per tą patį peržiūros procesą (Claude atrenka ir
išverčia, naudotojas patikrina/pataiso), tiesiog kandidatų sąrašas platesnis:

- **[ispell-lt](https://github.com/ispell-lt/ispell-lt)** (BSD-3-Clause licencija,
  © Albertas Agejevas ir bendraautoriai) — projekto `lietuviu.veiksmazodziai` failas
  yra specialiai sudarytas lietuviškų veiksmažodžių sąrašas (naudojamas ispell rašybos
  tikrinimo taisyklėms), iš jo atrinkti kandidatai žymimi `note` lauke
  `spinner_verbs_lt_progress.json` faile su nuoroda „ispell-lt verb list". Naudojami
  tik pavieniai žodžiai kaip vertimo kandidatai — patį failą ar jo struktūrą
  (afiksų taisykles) neperskelbiame/neplatiname.
- **[DLKŽ](https://ekalba.lt/dabartines-lietuviu-kalbos-zodynas/)** (Dabartinės
  lietuvių kalbos žodynas, Lietuvių kalbos institutas) — naudojamas kandidatų
  patikrai (ar žodis tikrai egzistuoja žodyne) per `scripts/scrape_dlkz.py`. Taip pat
  tik pavieniai antraštiniai žodžiai naudojami kaip nuoroda, jokio žodyno turinio
  (apibrėžimų, pavyzdžių) neperskelbiame.

### Stiliaus gairės

- Pirmenybė tikriems, natūraliai skambantiems lietuviškiems veiksmažodžiams; kai tikslaus
  atitikmens nėra — kuriamos naujadarai/asociacijos (pvz. Fotosintetinu, Lizdinu).
- `-inėju` galūnė (kartotinis/tęstinis veiksmas) — produktyvus modelis, ypač judėjimo
  žodžiams (Puolinėju, Tupinėju, Pasiramstinėju).
- Kai siūlomas alternatyvus variantas jau išverstam žodžiui — dažniausiai paliekami ABU
  (pool'e nėra griežto 1:1 apribojimo), nebent naudotojas aiškiai prašo pakeisti.
- Žaismingi/absurdiški naujadarai (pvz. Čiulptukauju) laikomi taip pat vertingi kaip
  "rimtas" pasirinkimas — atitinka originalo toną.

## Būklė

Visi 187 originalūs claudionary.com žodžiai turi lietuvišką atitikmenį, papildyta bonus
temomis be angliško šaltinio — iš viso **467 žodžiai, 16 kategorijų**, patikrinta be
pasikartojimų:

- Cooking/Food — 24
- Thinking/Cognition — 27
- Movement/Wandering — 44
- Nature/Organic Growth — 19
- Technical/Processing — 50
- Physics/Sci-fi — 59 *(10 iš originalaus žodyno + 41 grynai lietuviškas fizikos/sci-fi žargonas)*
- Bureaucratic/Corporate — 21
- Whimsical Nonsense Words — 40
- Weather & Misc — 54
- Statistika — 16
- Matematika — 16
- Kompiuteriniai tinklai — 15
- Sportas — 23
- Filosofija — 13
- Medicina — 18
- Garsai — 28

Visi trys pradiniai tikslai (žr. „Tikslas" viršuje) įgyvendinti: `settings.json`
konfigūracija paruošta, žodžių sąrašas pilnas, `claudionary_lt.md` dokumentacija parašyta.

## Prisidėjimas

PR'ai ir Issues laukiami — ypač naujos temos/kategorijos arba geresni variantai jau
esantiems žodžiams. Žr. stiliaus gaires aukščiau prieš siūlant naujus žodžius.

## Licencija

[MIT](LICENSE)
