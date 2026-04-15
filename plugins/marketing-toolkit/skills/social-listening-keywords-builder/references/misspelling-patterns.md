# Misspelling Patterns

Common patterns for generating plausible misspellings manually (or validating the script's output).

## Type 1: Keyboard-adjacent swaps (QWERTY)

Replace a letter with one next to it on the keyboard. Example with "Brand":
- B → V, G, H, N → "Vrand", "Grand", "Hrand", "Nrand"
- r → e, t, d, f → "Beand", "Btand", "Bdand", "Bfand"
- a → q, w, s, z → "Brqnd", "Brwnd", "Brsnd", "Brznd"
- n → b, h, j, m → "Brabd", "Brahd", "Brajd", "Bramd"
- d → s, f, e, r → "Brans", "Branf", "Brane", "Branr"

## Type 2: Transposition (swap adjacent letters)

Classic typo. Example with "Google":
- Goolge (swap g + l)
- Gooole (drop variant)
- Googel (swap l + e)

## Type 3: Dropped letters

Single letter missing:
- Google → Gogle, Gogle, Goole, Gooogle
- Brand → Band, Brnd, Bran

## Type 4: Doubled letters

Typed twice:
- Apple → Aapple, Apple, Appple, Applle, Applee
- Amazon → Aamazon, Amazonn

## Type 5: Phonetic substitutions

Common pairs that sound similar but spell differently:
- c ↔ k ("Cat" / "Kat", "IKEA" / "ICEA")
- s ↔ z ("Analyze" / "Analyse")
- f ↔ ph ("Fone" / "Phone")
- y ↔ i ("Yogurt" / "Iogurt")
- ck ↔ k ("Rack" / "Rak")

## Type 6: Spacing variants

- "Facebook" / "Face book"
- "ChatGPT" / "Chat GPT"
- "Dropbox" / "Drop box"
- "YouTube" / "You Tube" / "Utube" (also phonetic!)

## Type 7: Homoglyphs (visually similar chars)

Especially on Twitter/Instagram — users substitute:
- 0 ↔ O
- 1 ↔ l ↔ I
- 5 ↔ S
- @ ↔ a
- € ↔ e

## Type 8: Casual abbreviations

- "Instagram" → "IG", "insta", "ig", "Insta"
- "Facebook" → "FB", "fb", "facebk"
- "YouTube" → "YT", "yt"
- "Google" → "google'd" (verb usage)

## Type 9: Plural / verb forms

Users often mention brands as verbs:
- "googling"
- "uber'd"
- "slacked"
- "zoomed"

## Type 10: Foreign language spellings

For global brands, locals adapt spelling:
- English "Google" → Vietnamese "Gúc gờ" (phonetic transliteration)
- English "YouTube" → Russian "Ютуб"
- English "Facebook" → sometimes "Feysbuk" (Turkish/Russian)

## Vietnamese-specific

- Remove diacritics: "Tiki" stays, but for Vietnamese brand names with diacritics
- English brand adopted phonetically: "Highlands Coffee" → "Hai lẻn"
- Abbreviations: users write brand in Vietnamese alphabet
- Typing without Telex/VNI converts chars oddly

## Generator rules of thumb

For a 5-letter brand, expect:
- 15-25 plausible misspellings via type 1 alone
- 5-10 via type 2-4 each
- 2-5 via type 5
- Total: 40-60 unique variants

**Don't track all 60.** Track the top 5-10 most likely ones. More = noise.

## Validation check

Before committing a misspelling to your tracking list, ask:
1. Would a native speaker typing fast actually make this error? If no → skip.
2. Does it collide with a common word? ("Apple" → "Aple" also means "maple" abbreviation) → skip or add context filter.
3. Is it a known competitor's variation? → track separately.
