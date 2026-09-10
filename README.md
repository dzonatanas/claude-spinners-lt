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
**Bet kuri OS:**
```
python install/install.py
```

Paklaus dviejų klausimų (kur diegti — globaliai ar konkrečiam projektui; ir `replace` ar
`append`), tada pats saugiai sujungs `spinnerVerbs` su tavo esamu `settings.json` (jei
toks jau yra — jo TURINYS nepradingsta, tik prisideda naujas raktas), padarydamas
`.bak` atsarginę kopiją prieš rašydamas. Reikalingas tik Python 3, jokių papildomų
bibliotekų — `install.bat` pats patikrina ar `python`/`py` įdiegtas ir praneša, jei ne.

Neinteraktyviam naudojimui (pvz. automatizacijai):
```
python install/install.py --scope global --mode replace
python install/install.py --scope project --project-dir /kelias/iki/projekto --mode append
```

### Windows be Python

Jei Python neįdiegtas, `install/install_nopython.bat` atlieka tą patį grynu batch tekstu
(be jokių priklausomybių):
```
install\install_nopython.bat
install\install_nopython.bat project
install\install_nopython.bat project "C:\mano\projektas" append
install\install_nopython.bat global append
```
Be argumentų — numatytieji: globaliai, `replace`. Paklaus tik VIENO patvirtinimo
(Y/n) prieš rašydamas — sąmoningai vengiama kelių `set /p` klausimų iš eilės, nes tai
žinomai nepatikima `cmd.exe` (antras klausimas gali tiesiog negauti atsakymo, jei
skriptas paleidžiamas ne iš tikros konsolės). Taip pat daro `.bak` atsarginę kopiją ir
įspėja, jei faile jau yra `spinnerVerbs` raktas (nepašalins seno, tik pridės naują —
išsivalyk ranka, jei nori švaraus failo).

### Rankinis būdas

1. Atsidaryk `data/spinnerVerbs.settings.json` šiame repo — jame yra paruoštas
   `{"spinnerVerbs": {"mode": "replace", "verbs": [...]}}` blokas su visais 402 žodžiais.
2. Nuspręsk, kur jį dėti:
   - **Globaliai, visiems savo projektams šiame kompiuteryje** → `~/.claude/settings.json`
   - **Tik konkrečiam projektui** → `<projekto katalogas>/.claude/settings.json`
3. Jei tame faile jau yra kitų nustatymų (pvz. `theme`, `enabledPlugins`) — **NEPERRAŠYK**
   viso failo, o įklijuok tik `"spinnerVerbs": { ... }` raktą į jau esantį JSON objektą,
   kaip papildomą lauką šalia kitų.
4. Pasirink `mode`:
   - `"replace"` — rodys TIK lietuviškus žodžius (angliški numatytieji dingsta)
   - `"append"` — sujungs su 187 angliškais numatytaisiais, spinneris rodys mišinį
5. Išsaugok failą. **Pakeitimas pritaikomas iš karto**, be perkrovimo — patikrinta
   realiai veikiančioje sesijoje 2026-09-10 (Claude Code turi `settings_sync` mechanizmą,
   sekantį nustatymų failo pokyčius gyvai).

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
├── scripts/                — pagalbiniai (vienkartiniai) skriptai
│   └── scrape_claudionary.py
└── install/                — diegimo skriptai
    ├── install.py
    ├── install.bat
    └── install_nopython.bat
```

| Failas | Paskirtis |
|---|---|
| `scripts/scrape_claudionary.py` | Scraperis, ištraukiantis visą claudionary.com žodyną |
| `data/claudionary_source.json` | Scraping rezultatas — **187 originalūs anglų kalbos įrašai** (word, ipa, pos, category, etymology, definition, diagram_caption, example) |
| `data/spinner_verbs_lt_progress.json` | **Darbo būklė** — visi iki šiol išversti/sukurti lietuviški žodžiai, sugrupuoti pagal semantines kategorijas |
| `data/spinnerVerbs.settings.json` | Paruoštas `{"spinnerVerbs": {"mode": "replace", "verbs": [...]}}` blokas (visi 402 žodžiai) — naudojamas diegimo skriptų arba rankiniam kopijavimui |
| `install/install.py` | Diegimo skriptas — automatiškai sujungia `spinnerVerbs` su tavo `settings.json`, klausdamas scope (global/project) ir mode (replace/append), darydamas atsarginę kopiją. Žr. „Naudojimas" žemiau |
| `install/install.bat` | Windows apvalkalas `install.py` — dukart paspaudus paleidžia skriptą (patikrina ar Python įdiegtas) |
| `install/install_nopython.bat` | Diegimas be Python — grynas batch tekstas, jokių priklausomybių. Žr. „Naudojimas" žemiau |
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

**Rodymo mechanika** (patikrinta tiesiogiai `claude.exe` binare 2026-09-10): kiekvieną
kartą spinneris tiesiog atsitiktinai išrenka VIENĄ žodį iš viso masyvo — jokio ryšio su
tuo, ką Claude tuo metu realiai daro. `mode: "append"` sujungia numatytuosius (187 EN) su
`verbs` sąrašu ir renkasi iš viso ~589 žodžių; `mode: "replace"` rodo TIK `verbs` sąrašą.
Norint grynai lietuviško spinnerio — reikia `"replace"`.

### Stiliaus gairės (žr. taip pat atmintyje `feedback_lt_translation_style`)

- Pirmenybė tikriems, natūraliai skambantiems lietuviškiems veiksmažodžiams; kai tikslaus
  atitikmens nėra — kuriamos naujadarai/asociacijos (pvz. Fotosintetinu, Lizdinu).
- `-inėju` galūnė (kartotinis/tęstinis veiksmas) — produktyvus modelis, ypač judėjimo
  žodžiams (Puolinėju, Tupinėju, Pasiramstinėju).
- Kai siūlomas alternatyvus variantas jau išverstam žodžiui — dažniausiai paliekami ABU
  (pool'e nėra griežto 1:1 apribojimo), nebent naudotojas aiškiai prašo pakeisti.
- Žaismingi/absurdiški naujadarai (pvz. Čiulptukauju) laikomi taip pat vertingi kaip
  "rimtas" pasirinkimas — atitinka originalo toną.

## Būklė (2026-09-09)

**Visos 9 semantinės kategorijos + 6 bonus temos užrakintos, 402 žodžiai (pool įrašai, patikrinta — nė vieno pasikartojimo) — visi 187 šaltinio žodžiai jau turi lietuvišką atitikmenį:**

- ✅ Cooking/Food — 23
- ✅ Thinking/Cognition — 21
- ✅ Movement/Wandering — 38
- ✅ Nature/Organic Growth — 19 *(peržiūrėta ir galutinai užrakinta 2026-09-09, pritaikius `-inėju` galūnės variantus: Rūginėju, Išperinėju, Apdulkinėju, Sklaidausi; Germinating pakeista į Mikrobinu; Metamorphosing papildyta Vartausi; Sublimating papildyta Susigerinėju)*
- ✅ Technical/Processing — 43 *(užrakinta 2026-09-09 — čia pagaliau atsidūrė Malinėju ir Trupinu iš pradinių pavyzdžių; taip pat žaismingi meta-juokeliai Gitinu, Klaudinuosi/Debesuojuosi)*
- ✅ Physics/Sci-fi — 59 *(užrakinta 2026-09-09 — 10 EN žodžių + 41 grynai lietuviškas papildymas be angliško atitikmens, fizikos/sci-fi žargono naujadarai: Kvarkinu, Bozoninu, Teraforminu, Kibernetizuoju ir pan.)*
- ✅ Bureaucratic/Corporate — 16 *(užrakinta 2026-09-09 — Channeling/Channelling sujungti į vieną Kanalizuoju įrašą, nes JAV/britų rašybos juokelis lietuviškai neišsiverčia)*
- ✅ Whimsical Nonsense Words — 32 *(užrakinta 2026-09-10 — grynas garso žaismas/naujadarai: Kombobuliuoju/Diskombobuliuoju/Rekombobuliuoju šeima, Bandeliuoju/Bandelinuosi kalambūras su „bandele")*
- ✅ Weather & Misc (final batch) — 53 *(užrakinta 2026-09-10 — paskutinė partija, uždaranti visus 187 originalius žodžius; įskaitant Cultivating ūkininkavimo klasterį Tręšiu/Akėju/Ariu/Sodinu ir Flowing→Tekinu/Ištekinu su netyčiniu kalambūru apie ištekinimą)*

**Bonus temos (grynai lietuviškos, be angliško šaltinio, kaip Physics/Sci-fi papildymai):**

- ✅ Statistika — 15
- ✅ Matematika — 16 *(įskaitant Traukšakniuoju — kalambūras kvadratinei šaknai)*
- ✅ Kompiuteriniai tinklai — 15
- ✅ Sportas — 21
- ✅ Filosofija — 13
- ✅ Medicina — 18

- ✅ `~/.claude/settings.json` su `spinnerVerbs` konfigūracija — **užrašyta 2026-09-10**,
  `mode: "replace"` (globaliai visam kompiuteriui, ne tik šiam projektui — sąmoningas
  pasirinkimas), esami nustatymai (`tui`, `theme`, `enabledPlugins`) išsaugoti nepaliesti.
  Ta pati konfigūracija taip pat saugoma `data/spinnerVerbs.settings.json` faile šiame repo.

- ✅ Lietuviškas „claudionary" stiliaus dokumentacijos failas — `claudionary_lt.md`,
  žaismingas priedas su 17 rinktinių žodžių istorijų (ne pilnas žodynas — pagrindinis
  turinys visada lieka `data/spinner_verbs_lt_progress.json`).

Visi 3 pradiniai deliverable'ai užbaigti.

## Pastaba dėl istorijos

Šis projektas kartą jau prarado darbą, kai sesija netikėtai nutrūko — visas vertimas buvo
tik pokalbyje, niekur neišsaugotas. Atkurta iš žalios `.jsonl` sesijos transkripcijos.
**Nuo šiol progresas fiksuojamas `data/spinner_verbs_lt_progress.json` po kiekvienos
baigtos kategorijos**, kad taip nepasikartotų.

## Prisidėjimas

PR'ai ir Issues laukiami — ypač pasiūlymai likusioms kategorijoms (žr. "Liko nepradėta"
aukščiau) arba geresni variantai jau užrakintiems žodžiams. Žr. stiliaus gaires aukščiau
prieš siūlant naujus žodžius.

## Licencija

[MIT](LICENSE)
