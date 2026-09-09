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

## Failai

| Failas | Paskirtis |
|---|---|
| `scrape_claudionary.py` | Scraperis, ištraukiantis visą claudionary.com žodyną |
| `claudionary_source.json` | Scraping rezultatas — **187 originalūs anglų kalbos įrašai** (word, ipa, pos, category, etymology, definition, diagram_caption, example) |
| `vdu_llm_reference.md` | Instrukcija dviem vietiniams lietuviškiems LLM (`D:\VDU_LLM\`) — encoderiui (nepatikimas panašumui) ir generatyviam 1B modeliui (geras kūrybai, fabrikuoja faktus). Skirtas kaip PAPILDOMAS variantų šaltinis, ne pirminis vertėjas |
| `spinner_verbs_lt_progress.json` | **Darbo būklė** — visi iki šiol išversti/sukurti lietuviški žodžiai, sugrupuoti pagal semantines kategorijas |
| `README.md` | Šis failas |

## Metodas

Žodžiai verčiami/kuriami **tiesiogiai Claude**, kategorija po kategorijos (ne masiškai visi
187 iš karto) — kartu su naudotoju peržiūrint ir koreguojant kiekvieną grupę prieš pereinant
prie kitos. Vietinis LT LLM (`LT_AI_DLKVM`) numatytas kaip papildomas idėjų šaltinis, bet
kol kas nebuvo paleistas — visas darbas iki šiol yra tiesioginis vertimas/asociacija.

Galutinis sąrašas nėra griežtas 1:1 atitikmuo anglų kalbos žodžiams — tai laisvas žodžių
"baseinas" (`spinnerVerbs.add` priima paprastą masyvą), tad kai kuriems angliškiems
žodžiams paliekami keli lietuviški variantai (pvz. Gusting → Gūsiuoju/Vėjinu/Vėduoju/Vėsinu),
o kai kurie lietuviški žodžiai neturi tiesioginio angliško atitikmens (naudotojo pridėti
papildymai).

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

**Užrakinta 4 iš ~7 semantinių kategorijų, ~97 žodžiai (pool įrašai):**

- ✅ Cooking/Food — 23
- ✅ Thinking/Cognition — 21
- ✅ Movement/Wandering — ~34
- ✅ Nature/Organic Growth — 19 *(peržiūrėta ir galutinai užrakinta 2026-09-09, pritaikius `-inėju` galūnės variantus: Rūginėju, Išperinėju, Apdulkinėju, Sklaidausi; Germinating pakeista į Mikrobinu; Metamorphosing papildyta Vartausi; Sublimating papildyta Susigerinėju)*

**Liko nepradėta:**

- ⬜ Whimsical Nonsense Words (Discombobulating, Flibbertigibbeting, Razzmatazzing...)
- ⬜ Technical/Processing (čia turėtų atsidurti Malinėju, Trupinu iš pradinių pavyzdžių)
- ⬜ Bureaucratic/corporate jargon (Actioning, Actualizing... — galimai praleisti arba
  ieškoti LT biurokratizmų atitikmenų)
- ⬜ Physics/sci-fi (Hyperspacing, Quantumizing, Levitating, Warping)

**Dar nepradėta (galutiniai deliverable'ai):**

- ⬜ `~/.claude/settings.json` su `spinnerVerbs` konfigūracija (schema patvirtinta:
  `{"spinnerVerbs": {"add": [...]}}`, Unicode/lietuviškos raidės palaikomos)
- ⬜ Lietuviškas "claudionary" stiliaus dokumentacijos failas

## Pastaba dėl istorijos

Šis projektas kartą jau prarado darbą, kai sesija netikėtai nutrūko — visas vertimas buvo
tik pokalbyje, niekur neišsaugotas. Atkurta iš žalios `.jsonl` sesijos transkripcijos.
**Nuo šiol progresas fiksuojamas `spinner_verbs_lt_progress.json` po kiekvienos baigtos
kategorijos**, kad taip nepasikartotų.

## Prisidėjimas

PR'ai ir Issues laukiami — ypač pasiūlymai likusioms kategorijoms (žr. "Liko nepradėta"
aukščiau) arba geresni variantai jau užrakintiems žodžiams. Žr. stiliaus gaires aukščiau
prieš siūlant naujus žodžius.

## Licencija

[MIT](LICENSE)
