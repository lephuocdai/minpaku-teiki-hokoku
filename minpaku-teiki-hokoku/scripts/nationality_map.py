# -*- coding: utf-8 -*-
"""
nationality_map.py — normalize free-text nationality strings to the 22
categories used by the 民泊制度運営システム 定期報告 (住宅宿泊事業法 14条).

The 22 categories are a FIXED list of numeric boxes on the government form
(操作手順書 図2-43; also 電子宿泊者名簿 操作説明書 表1-2). There is no
free-text country entry on the form; anything outside the 21 named
countries/regions goes into the single その他 (other) box.

DESIGN NOTES
------------
* This module is deterministic string normalization ONLY. Judgment calls
  (residence rules such as "foreigner with a Japan address counts as 日本",
  name-based inference, per-guest evidence weighing) happen UPSTREAM in the
  skill dialogue, which writes final per-guest values into
  normalized_reservations.csv. This module is the safety net that maps
  raw spellings ("Taiwanese", "U.S.A.", "français", "HK", ...) onto the
  official categories, and returns None for anything it cannot recognize
  so the engine can surface it for review instead of guessing.
* Matching strategy (in order):
    1. exact lookup of the cleaned string
    2. compound self-reported nationalities ("X / Y", "X & Y", "X and Y",
       "X、Y") -> the first component that resolves (first/primary wins)
    3. whole-token match for SHORT keys (<= 3 chars, e.g. "us", "in", "ca").
       Short keys must match a whole word — a plain substring match on a
       short key like "ca" would wrongly hit inside "Moroccan" -> カナダ,
       or "it" inside "U.S. Citizen" -> イタリア.
    4. substring match for LONGER keys, longest key first, so
       "people's republic of china" wins over "republic of china" wins
       over "china".
  Anything else -> None (unresolved; the engine flags it, never drops it).
"""

import re

# The 22 categories in the EXACT order they appear on the government form.
# (香港 is included — its omission in one manual table is a documented typo;
# the actual upload format and the on-screen grid both contain it.)
NATIONALITY_CATEGORIES = [
    "日本", "韓国", "台湾", "香港", "中国", "タイ", "シンガポール",
    "マレーシア", "インドネシア", "フィリピン", "ベトナム", "インド",
    "英国", "ドイツ", "フランス", "イタリア", "スペイン", "ロシア",
    "米国", "カナダ", "オーストラリア", "その他",
]

# Fast membership test for values that are already final categories.
CATEGORY_SET = frozenset(NATIONALITY_CATEGORIES)

# Mapping: cleaned lowercase input -> category.
# Generic entries only. If your own data contains new spellings, add them
# here (or resolve them upstream in the skill dialogue).
_RAW_MAP = {
    # ── 日本 ──
    "japan": "日本", "japanese": "日本", "日本": "日本", "jp": "日本",
    "nippon": "日本", "nihon": "日本",

    # ── 韓国 ── (North Korea maps to その他; see explicit entries below —
    # the longest-first substring pass checks them before plain "korea".)
    "korea": "韓国", "korean": "韓国", "south korea": "韓国",
    "republic of korea": "韓国", "韓国": "韓国", "kr": "韓国",
    "대한민국": "韓国", "한국": "韓国",

    # ── 台湾 ──
    "taiwan": "台湾", "taiwanese": "台湾", "台湾": "台湾", "tw": "台湾",
    "taiwan, province of china": "台湾", "chinese taipei": "台湾",
    # "Republic of China" formally refers to Taiwan. Exact lookup runs first,
    # and the substring pass is longest-first, so "people's republic of
    # china" still resolves to 中国.
    "republic of china": "台湾",

    # ── 香港 ──
    "hong kong": "香港", "hongkong": "香港", "hk": "香港", "香港": "香港",
    "hong kong sar": "香港", "hongkongchina": "香港",
    "hong kong china": "香港", "hong kong, china": "香港",

    # ── 中国 ──
    "china": "中国", "chinese": "中国", "中国": "中国", "cn": "中国",
    "people's republic of china": "中国", "peoples republic of china": "中国",
    "prc": "中国", "mainland china": "中国",

    # ── タイ ──
    "thailand": "タイ", "thai": "タイ", "タイ": "タイ", "th": "タイ",

    # ── シンガポール ──
    "singapore": "シンガポール", "singaporean": "シンガポール",
    "シンガポール": "シンガポール", "sg": "シンガポール",

    # ── マレーシア ──
    "malaysia": "マレーシア", "malaysian": "マレーシア",
    "マレーシア": "マレーシア", "my": "マレーシア",

    # ── インドネシア ──
    "indonesia": "インドネシア", "indonesian": "インドネシア",
    "インドネシア": "インドネシア", "id": "インドネシア",

    # ── フィリピン ──
    "philippines": "フィリピン", "philippine": "フィリピン",
    "filipino": "フィリピン", "filipina": "フィリピン",
    "フィリピン": "フィリピン", "ph": "フィリピン",

    # ── ベトナム ──
    "vietnam": "ベトナム", "vietnamese": "ベトナム", "viet nam": "ベトナム",
    "ベトナム": "ベトナム", "vn": "ベトナム",

    # ── インド ──
    "india": "インド", "indian": "インド", "インド": "インド", "in": "インド",

    # ── 英国 ──
    "uk": "英国", "united kingdom": "英国", "britain": "英国",
    "great britain": "英国", "british": "英国", "england": "英国",
    "english": "英国", "scotland": "英国", "scottish": "英国",
    "wales": "英国", "welsh": "英国", "northern ireland": "英国",
    "英国": "英国", "イギリス": "英国", "gb": "英国",

    # ── ドイツ ──
    "germany": "ドイツ", "german": "ドイツ", "ドイツ": "ドイツ",
    "de": "ドイツ", "deutschland": "ドイツ", "deutsch": "ドイツ",

    # ── フランス ──
    "france": "フランス", "french": "フランス", "フランス": "フランス",
    "fr": "フランス",
    "francais": "フランス", "francaise": "フランス",   # endonyms
    "français": "フランス", "française": "フランス",

    # ── イタリア ──
    "italy": "イタリア", "italian": "イタリア", "イタリア": "イタリア",
    "it": "イタリア", "italia": "イタリア", "italiano": "イタリア",

    # ── スペイン ──
    "spain": "スペイン", "spanish": "スペイン", "スペイン": "スペイン",
    "es": "スペイン", "españa": "スペイン", "espana": "スペイン",
    "español": "スペイン", "espanol": "スペイン",

    # ── ロシア ──
    "russia": "ロシア", "russian": "ロシア", "ロシア": "ロシア",
    "ru": "ロシア", "russian federation": "ロシア",

    # ── 米国 ──
    "usa": "米国", "us": "米国", "united states": "米国",
    "united states of america": "米国", "american": "米国",
    "米国": "米国", "アメリカ": "米国", "america": "米国",
    "us citizen": "米国", "u.s.": "米国", "u.s.a.": "米国",
    "u.s. citizen": "米国",

    # ── カナダ ──
    "canada": "カナダ", "canadian": "カナダ", "カナダ": "カナダ", "ca": "カナダ",

    # ── オーストラリア ──
    "australia": "オーストラリア", "australian": "オーストラリア",
    "オーストラリア": "オーストラリア", "au": "オーストラリア",
    "aussie": "オーストラリア",

    # ── その他 (map common cases explicitly so they don't get flagged) ──
    "その他": "その他", "other": "その他", "others": "その他",
    # North Korea — must NOT fall into 韓国 via the "korea" substring.
    "north korea": "その他", "dprk": "その他",
    "democratic people's republic of korea": "その他",
    # Europe
    "netherlands": "その他", "dutch": "その他", "holland": "その他",
    "belgium": "その他", "belgian": "その他",
    "switzerland": "その他", "swiss": "その他",
    "austria": "その他", "austrian": "その他",
    "portugal": "その他", "portuguese": "その他",
    "sweden": "その他", "swedish": "その他",
    "norway": "その他", "norwegian": "その他",
    "denmark": "その他", "danish": "その他",
    "finland": "その他", "finnish": "その他",
    "ireland": "その他", "irish": "その他",
    "poland": "その他", "polish": "その他",
    "czech republic": "その他", "czech": "その他", "czechia": "その他",
    "hungary": "その他", "hungarian": "その他",
    "romania": "その他", "romanian": "その他",
    "greece": "その他", "greek": "その他",
    "bulgaria": "その他", "bulgarian": "その他",
    "slovakia": "その他", "slovak": "その他",
    "slovenia": "その他", "slovenian": "その他",
    "croatia": "その他", "croatian": "その他",
    "serbia": "その他", "serbian": "その他",
    "estonia": "その他", "estonian": "その他",
    "latvia": "その他", "latvian": "その他",
    "lithuania": "その他", "lithuanian": "その他",
    "ukraine": "その他", "ukrainian": "その他",
    "belarus": "その他", "iceland": "その他", "icelandic": "その他",
    "luxembourg": "その他", "malta": "その他", "maltese": "その他",
    "cyprus": "その他", "georgia": "その他", "armenia": "その他",
    # Americas
    "mexico": "その他", "mexican": "その他",
    "brazil": "その他", "brazilian": "その他",
    "argentina": "その他", "argentinian": "その他", "argentine": "その他",
    "colombia": "その他", "colombian": "その他",
    "chile": "その他", "chilean": "その他",
    "peru": "その他", "perú": "その他", "peruvian": "その他",
    "ecuador": "その他", "ecuadorian": "その他",
    "bolivia": "その他", "bolivian": "その他",
    "uruguay": "その他", "paraguay": "その他",
    "venezuela": "その他", "venezuelan": "その他",
    "guatemala": "その他", "guatemalan": "その他",
    "honduras": "その他", "el salvador": "その他", "nicaragua": "その他",
    "costa rica": "その他", "costa rican": "その他",
    "panama": "その他", "panamanian": "その他",
    "cuba": "その他", "cuban": "その他",
    "jamaica": "その他", "jamaican": "その他",
    "trinidad and tobago": "その他", "trinidadian": "その他",
    "dominican republic": "その他", "dominican": "その他",
    "puerto rico": "その他", "puerto rican": "その他",
    # Middle East / Africa
    "turkey": "その他", "turkish": "その他", "türkiye": "その他",
    "israel": "その他", "israeli": "その他",
    "iran": "その他", "iranian": "その他",
    "iraq": "その他", "iraqi": "その他",
    "saudi arabia": "その他", "saudi": "その他",
    "uae": "その他", "united arab emirates": "その他", "emirati": "その他",
    "qatar": "その他", "kuwait": "その他", "jordan": "その他",
    "lebanon": "その他", "lebanese": "その他",
    "egypt": "その他", "egyptian": "その他",
    "morocco": "その他", "moroccan": "その他",
    "algeria": "その他", "algerian": "その他",
    "tunisia": "その他", "south africa": "その他", "south african": "その他",
    "nigeria": "その他", "nigerian": "その他",
    "kenya": "その他", "kenyan": "その他", "ghana": "その他",
    "ethiopia": "その他",
    # Rest of Asia / Oceania
    "pakistan": "その他", "pakistani": "その他",
    "bangladesh": "その他", "bangladeshi": "その他",
    "sri lanka": "その他", "sri lankan": "その他",
    "nepal": "その他", "nepali": "その他", "nepalese": "その他",
    "myanmar": "その他", "burmese": "その他",
    "cambodia": "その他", "cambodian": "その他",
    "laos": "その他", "laotian": "その他", "lao": "その他",
    "brunei": "その他", "bhutan": "その他", "maldives": "その他",
    "mongolia": "その他", "mongolian": "その他",
    "kazakhstan": "その他", "uzbekistan": "その他",
    "new zealand": "その他", "new zealander": "その他", "nz": "その他",
    "kiwi": "その他",
    "fiji": "その他", "fijian": "その他", "papua new guinea": "その他",
}

# Keys sorted longest-first, precomputed once, so the substring pass always
# prefers the most specific key ("people's republic of china" > "china").
_LONG_KEYS = sorted((k for k in _RAW_MAP if len(k) > 3), key=len, reverse=True)
_SHORT_KEYS = [k for k in _RAW_MAP if len(k) <= 3]


def _clean(raw):
    """Lowercase and strip punctuation noise from a raw nationality string.

    Dots are REMOVED (not replaced by spaces) so "U.S.A." -> "usa" and
    "U.S." -> "us" still hit their exact-map entries. Commas, parens and
    leading "the " become/eat whitespace.
    """
    s = str(raw).strip().lower()
    s = s.replace(".", "")
    for noise in (",", "(", ")", "[", "]"):
        s = s.replace(noise, " ")
    s = re.sub(r"\s+", " ", s).strip()
    if s.startswith("the "):
        s = s[4:]
    return s


def normalize_nationality(raw):
    """Normalize a free-text nationality string to one of the 22 categories.

    Returns the Japanese category name (a member of NATIONALITY_CATEGORIES),
    or None when the input is empty or unrecognized. Callers must treat
    None as "unresolved — surface for human review", never as その他.
    """
    if raw is None:
        return None
    cleaned = _clean(raw)
    if not cleaned:
        return None

    # 1. Exact lookup (covers all Japanese category names, endonyms, codes).
    if cleaned in _RAW_MAP:
        return _RAW_MAP[cleaned]

    # 2. Compound self-reported nationalities ("X / Y", "X & Y", "X and Y",
    #    "X、Y"): first/primary component wins — normalize the FIRST
    #    component that resolves. Runs before the token/substring passes so
    #    the first component, not the longest matching key, decides.
    #    (Multi-word map entries like "trinidad and tobago" are unaffected:
    #    they are caught by the exact lookup above.)
    if re.search(r"/|&|、| and ", cleaned):
        for part in re.split(r"/|&|、| and ", cleaned):
            part = part.strip()
            if part and part != cleaned:
                result = normalize_nationality(part)
                if result:
                    return result

    # 3. Whole-token match for short keys ("us", "uk", "in", "ca", ...).
    #    Tokens are ASCII word chunks; CJK inputs are handled by exact match.
    tokens = set(re.split(r"[^a-z0-9]+", cleaned)) - {""}
    for key in _SHORT_KEYS:
        if key in tokens:
            return _RAW_MAP[key]

    # 4. Substring match for longer keys, longest key first.
    for key in _LONG_KEYS:
        if key in cleaned:
            return _RAW_MAP[key]

    # Unrecognized: let the engine flag it for review. Do NOT guess.
    return None
