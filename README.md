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

**Liko:**

- ⬜ `~/.claude/settings.json` su `spinnerVerbs` konfigūracija
- ⬜ Lietuviškas „claudionary" stiliaus dokumentacijos failas

## LT_AI_DLKVM modelio patikimumo patikra

2026-09-09/10 modelis buvo paleistas pirmą kartą per visą projektą — patikrinti jo
patikimumą tiksliam, apribojimais paremtam žodžių paieškos užklausimui, prieš
apsisprendžiant, ar juo verta pasitikėti kaip papildomu variantų šaltiniu šiam projektui.
Rezultatas neigiamas: modelis negalėjo tiksliai įvykdyti paprasto apribojimais paremto
užklausimo, generavo nesusijusį tekstą. Tai atitinka `vdu_llm_reference.md` įspėjimą —
modelis geriau tinka atviresnei kūrybinei generacijai nei tiksliems atitikmenims. Pačiam
vertimo darbui modelis kol kas nenaudotas.

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
