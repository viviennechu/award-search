#!/usr/bin/env python3
"""
哩程機票查詢系統
用法：python award_search.py
然後開啟 http://localhost:8888
"""

import json
import urllib.request
import urllib.parse
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler

SSL_CTX = ssl._create_unverified_context()

API_KEY = "pro_3BAOy4p8Z4TJXnXZBR9njSBu5Vd"
API_BASE = "https://seats.aero/partnerapi"

SOURCE_NAMES = {
    "aeroplan":       "Air Canada Aeroplan",
    "alaska":         "Alaska Mileage Plan",
    "american":       "AAdvantage",
    "aeromexico":     "Aeromexico Club Premier",
    "lifemiles":      "Avianca LifeMiles",
    "azul":           "Azul Fidelidade",
    "copa":           "Copa ConnectMiles",
    "delta":          "Delta SkyMiles",
    "emirates":       "Emirates Skywards",
    "ethiopian":      "Ethiopian ShebaMiles",
    "etihad":         "Etihad Guest",
    "finnair":        "Finnair Plus",
    "flyingblue":     "Flying Blue（法航/荷航）",
    "smiles":         "GOL Smiles",
    "jetblue":        "JetBlue TrueBlue",
    "lufthansa":      "Miles & More（漢莎）",
    "qantas":         "Qantas Frequent Flyer",
    "qatar":          "Qatar Privilege Club",
    "eurobonus":      "SAS EuroBonus",
    "saudia":         "Saudia AlFursan",
    "singapore":      "KrisFlyer（新航）",
    "turkish":        "Miles&Smiles（土航）",
    "united":         "United MileagePlus",
    "virginatlantic": "Virgin Atlantic",
    "velocity":       "Virgin Australia Velocity",
}

AIRPORT_ALIASES = {
    # 台灣
    "台北": ["TPE"], "桃園": ["TPE"], "桃園機場": ["TPE"],
    "松山": ["TSA"], "台北松山": ["TSA"],
    "高雄": ["KHH"], "小港": ["KHH"],
    "台中": ["RMQ"],
    "花蓮": ["HUN"],
    "台南": ["TNN"],
    # 日本
    "東京": ["NRT", "HND"], "成田": ["NRT"], "東京成田": ["NRT"],
    "羽田": ["HND"], "東京羽田": ["HND"],
    "大阪": ["KIX"], "關西": ["KIX"], "大阪關西": ["KIX"],
    "伊丹": ["ITM"], "大阪伊丹": ["ITM"],
    "名古屋": ["NGO"],
    "福岡": ["FUK"],
    "札幌": ["CTS"], "新千歲": ["CTS"],
    "沖繩": ["OKA"], "那霸": ["OKA"],
    "廣島": ["HIJ"],
    "仙台": ["SDJ"],
    # 韓國
    "首爾": ["ICN"], "仁川": ["ICN"], "首爾仁川": ["ICN"],
    "金浦": ["GMP"], "首爾金浦": ["GMP"],
    "釜山": ["PUS"],
    "濟州": ["CJU"],
    # 中國
    "北京": ["PEK"], "北京首都": ["PEK"],
    "上海": ["PVG", "SHA"], "浦東": ["PVG"], "上海浦東": ["PVG"],
    "虹橋": ["SHA"], "上海虹橋": ["SHA"],
    "廣州": ["CAN"],
    "深圳": ["SZX"],
    "成都": ["CTU"],
    "重慶": ["CKG"],
    "廈門": ["XMN"],
    "杭州": ["HGH"],
    # 東南亞
    "香港": ["HKG"],
    "澳門": ["MFM"],
    "新加坡": ["SIN"],
    "曼谷": ["BKK"], "素旺那普": ["BKK"], "廊曼": ["DMK"],
    "吉隆坡": ["KUL"],
    "馬尼拉": ["MNL"],
    "雅加達": ["CGK"],
    "峇里島": ["DPS"], "巴里島": ["DPS"], "峇厘島": ["DPS"],
    "胡志明市": ["SGN"],
    "河內": ["HAN"],
    "普吉": ["HKT"],
    "清邁": ["CNX"],
    # 南亞
    "孟買": ["BOM"],
    "新德里": ["DEL"], "德里": ["DEL"],
    # 中東
    "杜拜": ["DXB"],
    "阿布達比": ["AUH"],
    "多哈": ["DOH"],
    "伊斯坦堡": ["IST"],
    "特拉維夫": ["TLV"],
    # 歐洲
    "倫敦": ["LHR"], "希斯洛": ["LHR"], "倫敦希斯洛": ["LHR"],
    "蓋威克": ["LGW"], "倫敦蓋威克": ["LGW"],
    "巴黎": ["CDG"], "戴高樂": ["CDG"], "巴黎戴高樂": ["CDG"],
    "阿姆斯特丹": ["AMS"],
    "法蘭克福": ["FRA"],
    "慕尼黑": ["MUC"],
    "蘇黎世": ["ZRH"],
    "維也納": ["VIE"],
    "羅馬": ["FCO"],
    "米蘭": ["MXP"],
    "馬德里": ["MAD"],
    "巴塞隆納": ["BCN"],
    "里斯本": ["LIS"],
    "布魯塞爾": ["BRU"],
    "哥本哈根": ["CPH"],
    "斯德哥爾摩": ["ARN"],
    "赫爾辛基": ["HEL"],
    "奧斯陸": ["OSL"],
    "華沙": ["WAW"],
    "布拉格": ["PRG"],
    "布達佩斯": ["BUD"],
    "雅典": ["ATH"],
    "都柏林": ["DUB"],
    "愛丁堡": ["EDI"],
    # 北美洲
    "紐約": ["JFK", "EWR"], "甘迺迪": ["JFK"], "紐約甘迺迪": ["JFK"],
    "紐瓦克": ["EWR"], "紐約紐瓦克": ["EWR"],
    "洛杉磯": ["LAX"],
    "舊金山": ["SFO"],
    "西雅圖": ["SEA"],
    "拉斯維加斯": ["LAS"],
    "芝加哥": ["ORD"], "奧海爾": ["ORD"],
    "波士頓": ["BOS"],
    "邁阿密": ["MIA"],
    "達拉斯": ["DFW"],
    "休士頓": ["IAH"],
    "鳳凰城": ["PHX"],
    "丹佛": ["DEN"],
    "亞特蘭大": ["ATL"],
    "溫哥華": ["YVR"],
    "多倫多": ["YYZ"],
    "蒙特婁": ["YUL"],
    "墨西哥城": ["MEX"],
    "夏威夷": ["HNL"], "檀香山": ["HNL"],
    # 大洋洲
    "雪梨": ["SYD"],
    "墨爾本": ["MEL"],
    "布里斯本": ["BNE"],
    "奧克蘭": ["AKL"],
    # 非洲
    "開羅": ["CAI"],
    "奈洛比": ["NBO"],
    "約翰尼斯堡": ["JNB"],
}

IATA_TO_CHINESE = {
    "TPE": "桃園 TPE", "TSA": "松山 TSA", "KHH": "高雄 KHH", "RMQ": "台中 RMQ",
    "NRT": "成田 NRT", "HND": "羽田 HND", "KIX": "關西 KIX", "ITM": "伊丹 ITM",
    "NGO": "名古屋 NGO", "FUK": "福岡 FUK", "CTS": "新千歲 CTS", "OKA": "沖繩 OKA",
    "ICN": "仁川 ICN", "GMP": "金浦 GMP", "PUS": "釜山 PUS",
    "HKG": "香港 HKG", "MFM": "澳門 MFM", "SIN": "新加坡 SIN",
    "BKK": "曼谷 BKK", "KUL": "吉隆坡 KUL", "MNL": "馬尼拉 MNL",
    "PVG": "上海浦東 PVG", "SHA": "上海虹橋 SHA",
    "PEK": "北京 PEK", "CAN": "廣州 CAN",
    "CDG": "巴黎 CDG", "LHR": "倫敦 LHR", "FRA": "法蘭克福 FRA",
    "AMS": "阿姆斯特丹 AMS", "VIE": "維也納 VIE", "PRG": "布拉格 PRG",
    "JFK": "紐約 JFK", "LAX": "洛杉磯 LAX", "SFO": "舊金山 SFO",
    "YVR": "溫哥華 YVR", "YYZ": "多倫多 YYZ", "SYD": "雪梨 SYD",
    "DXB": "杜拜 DXB", "DOH": "多哈 DOH",
}


def resolve_airport(text):
    text = text.strip()
    upper = text.upper()
    if len(upper) == 3 and upper.isalpha():
        return [upper]
    for alias, codes in AIRPORT_ALIASES.items():
        if text in alias or alias in text:
            return codes
    return []


def search_awards(origin_codes, dest_codes, cabin, start_date, end_date):
    all_results = []
    seen_ids = set()
    for origin in origin_codes:
        for dest in dest_codes:
            params = {"origin_airport": origin, "destination_airport": dest}
            if cabin:
                params["cabin"] = cabin
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date
            url = f"{API_BASE}/search?" + urllib.parse.urlencode(params)
            req = urllib.request.Request(url, headers={
                "Partner-Authorization": API_KEY,
                "User-Agent": "AwardSearch/1.0"
            })
            try:
                with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
                    data = json.loads(resp.read().decode())
                    for item in (data.get("data") or []):
                        if item["ID"] not in seen_ids:
                            seen_ids.add(item["ID"])
                            all_results.append(item)
            except Exception as e:
                print(f"API error ({origin}-{dest}): {e}")
    return all_results


def get_trips(availability_id):
    url = f"{API_BASE}/trips/{availability_id}"
    req = urllib.request.Request(url, headers={
        "Partner-Authorization": API_KEY,
        "User-Agent": "AwardSearch/1.0"
    })
    try:
        with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}


HTML = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>哩程機票查詢</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, "Noto Sans TC", sans-serif;
    background: #0f1117;
    color: #e2e8f0;
    min-height: 100vh;
  }
  .header {
    background: linear-gradient(135deg, #1a1f2e 0%, #0f1117 100%);
    border-bottom: 1px solid #2d3748;
    padding: 20px 32px;
  }
  .header h1 { font-size: 22px; font-weight: 700; color: #fff; }
  .header span { font-size: 13px; color: #718096; }
  .search-panel { max-width: 960px; margin: 24px auto; padding: 0 16px; }
  .search-box {
    background: #1a1f2e;
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 20px;
    overflow: visible;
  }
  .row { display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }
  .field { flex: 1; min-width: 140px; position: relative; }
  .field.narrow { flex: 0 0 100px; min-width: 80px; }
  @media (max-width: 480px) {
    .search-panel { margin: 12px auto; padding: 0 12px; }
    .search-box { padding: 16px; }
    .row { flex-direction: column; gap: 10px; }
    .field, .field.narrow { flex: 1 1 100%; min-width: 0; width: 100%; }
    .swap-btn { display: none; }
    .field input { font-size: 16px; padding: 12px 14px; }
    .cabin-btn { padding: 10px 18px; font-size: 14px; }
    .search-btn { padding: 14px; font-size: 17px; }
  }
  .field label {
    display: block; font-size: 11px; color: #718096;
    margin-bottom: 6px; font-weight: 600; letter-spacing: .6px; text-transform: uppercase;
  }
  .field input {
    width: 100%; padding: 10px 14px;
    background: #0f1117; border: 1px solid #2d3748;
    border-radius: 8px; color: #e2e8f0; font-size: 15px; outline: none;
    transition: border-color .2s;
  }
  .field input[type="number"] { font-size: 15px; }
  .field input:focus { border-color: #4a9eff; }
  .swap-btn {
    flex: 0; display: flex; align-items: flex-end; padding-bottom: 9px;
    font-size: 22px; cursor: pointer; color: #718096;
    transition: color .2s;
  }
  .swap-btn:hover { color: #4a9eff; }
  .suggestions {
    position: absolute; top: 100%; left: 0; right: 0; z-index: 100;
    background: #1e2535; border: 1px solid #3a4a6a;
    border-radius: 8px; margin-top: 4px;
    max-height: 200px; overflow-y: auto; display: none;
  }
  .suggestions.show { display: block; }
  .sug-item {
    padding: 8px 14px; cursor: pointer; font-size: 13px;
    display: flex; justify-content: space-between; align-items: center;
  }
  .sug-item:hover { background: #2d3a5a; }
  .sug-iata { color: #4a9eff; font-weight: 600; font-size: 12px; }
  .cabin-section { margin-bottom: 16px; }
  .cabin-section label {
    display: block; font-size: 11px; color: #718096;
    margin-bottom: 8px; font-weight: 600; letter-spacing: .6px; text-transform: uppercase;
  }
  .cabin-options { display: flex; gap: 8px; flex-wrap: wrap; }
  .cabin-btn {
    padding: 7px 16px; border-radius: 20px;
    border: 1px solid #2d3748; background: #0f1117;
    color: #a0aec0; cursor: pointer; font-size: 13px; transition: all .2s;
  }
  .cabin-btn.active { background: #2b4a8a; border-color: #4a9eff; color: #fff; }
  .search-btn {
    width: 100%; padding: 12px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border: none; border-radius: 8px; color: #fff;
    font-size: 16px; font-weight: 600; cursor: pointer; transition: opacity .2s;
  }
  .search-btn:hover { opacity: .9; }
  .search-btn:disabled { opacity: .5; cursor: default; }

  .results-area { max-width: 1280px; margin: 0 auto 60px; padding: 0 20px; }
  .results-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 14px; flex-wrap: wrap; gap: 10px;
  }
  .results-title { font-size: 16px; font-weight: 600; margin-bottom: 3px; }
  .results-count { color: #718096; font-size: 13px; }

  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; }
  th {
    background: #1a1f2e; padding: 10px 14px; text-align: left;
    font-size: 11px; font-weight: 600; color: #718096; letter-spacing: .5px;
    border-bottom: 1px solid #2d3748; white-space: nowrap;
    cursor: pointer; user-select: none;
  }
  th:hover { color: #a0aec0; }
  tbody tr.data-row {
    cursor: pointer; transition: background .15s;
    border-bottom: 1px solid #1a2030;
  }
  tbody tr.data-row:hover td { background: #1a2535; }
  td { padding: 10px 14px; font-size: 13px; vertical-align: middle; }

  .detail-row td {
    padding: 0;
    background: #111620;
    border-bottom: 2px solid #2d3748;
  }
  .detail-inner {
    padding: 16px 20px;
    display: none;
  }
  .detail-inner.open { display: block; }

  /* Badges */
  .cabin-tag {
    display: inline-block; padding: 2px 8px;
    border-radius: 4px; font-size: 11px; font-weight: 600;
  }
  .cabin-Y { background:#1a3a1a; color:#68d391; }
  .cabin-W { background:#1a2a3a; color:#63b3ed; }
  .cabin-J { background:#2a1a3a; color:#b794f4; }
  .cabin-F { background:#3a2a1a; color:#f6ad55; }
  .direct-badge {
    display:inline-block; padding:2px 6px;
    background:#1a3a2a; color:#68d391; border-radius:4px; font-size:11px;
  }
  .indirect-badge {
    display:inline-block; padding:2px 6px;
    background:#2a2a1a; color:#f6ad55; border-radius:4px; font-size:11px;
  }
  .lieflat-badge {
    display:inline-block; padding:3px 8px;
    background:#1a3a1a; color:#68d391; border-radius:4px; font-size:12px; font-weight:600;
  }
  .mixed-badge {
    display:inline-block; padding:3px 8px;
    background:#2a2a1a; color:#ecc94b; border-radius:4px; font-size:12px; font-weight:600;
  }
  .recliner-badge {
    display:inline-block; padding:3px 8px;
    background:#2a1a1a; color:#fc8181; border-radius:4px; font-size:12px; font-weight:600;
  }
  .airport-tag {
    font-size:11px; color:#4a9eff;
    background:#1a2a3a; padding:1px 6px; border-radius:3px; margin:0 2px;
  }
  .miles { font-weight:700; color:#e2e8f0; }
  .miles-unit { font-size:11px; color:#718096; }
  .seats-num { font-weight:600; }
  .seats-ok { color:#68d391; }
  .seats-warn { color:#ecc94b; }
  .seats-low { color:#fc8181; }
  .expand-icon { color:#4a9eff; font-size:12px; margin-left:4px; }

  /* Trip detail */
  .trip-cards { display:flex; flex-direction:column; gap:10px; }
  .trip-card {
    background:#1a2030; border:1px solid #2d3748; border-radius:8px; padding:14px 16px;
  }
  .trip-card-header {
    display:flex; justify-content:space-between; align-items:center;
    margin-bottom:10px; flex-wrap:wrap; gap:8px;
  }
  .flight-info { font-size:13px; color:#a0aec0; }
  .flight-num { font-weight:600; color:#e2e8f0; margin-right:8px; }
  .time-info { font-size:14px; font-weight:600; }
  .time-arrow { color:#718096; margin:0 8px; }
  .duration { font-size:12px; color:#718096; margin-left:8px; }
  .aircraft-info { display:flex; align-items:center; gap:8px; margin-top:4px; }
  .aircraft-name { font-size:13px; color:#a0aec0; }
  .book-links { display:flex; gap:8px; flex-wrap:wrap; margin-top:12px; }
  .book-btn {
    padding:6px 14px; border-radius:6px; font-size:12px; font-weight:600;
    text-decoration:none; border:1px solid #2d3748; color:#a0aec0;
    transition:all .2s; cursor:pointer; background:#0f1117;
  }
  .book-btn.primary {
    background:#2b4a8a; border-color:#4a9eff; color:#fff;
  }
  .book-btn:hover { opacity:.85; }
  .loading-detail {
    padding:20px; text-align:center; color:#718096; font-size:13px;
  }
  .spinner {
    display:inline-block; width:16px; height:16px;
    border:2px solid #2d3748; border-top-color:#4a9eff;
    border-radius:50%; animation:spin .8s linear infinite;
    margin-right:6px; vertical-align:middle;
  }
  @keyframes spin { to { transform:rotate(360deg); } }
  .loading-full { text-align:center; padding:60px; color:#718096; font-size:16px; }
  .spinner-lg {
    display:inline-block; width:24px; height:24px;
    border:3px solid #2d3748; border-top-color:#4a9eff;
    border-radius:50%; animation:spin .8s linear infinite;
    margin-right:10px; vertical-align:middle;
  }
  .error-msg { color:#fc8181; padding:20px; text-align:center; }
  .no-results { color:#718096; padding:40px; text-align:center; font-size:15px; }
  .seg-row { display:flex; align-items:center; gap:12px; padding:6px 0; flex-wrap:wrap; }
  .seg-airports { font-size:14px; font-weight:600; }
  .stops-label { font-size:11px; color:#fc8181; background:#2a1a1a; padding:2px 6px; border-radius:4px; }
</style>
</head>
<body>

<div class="header">
  <h1>✈ 哩程機票查詢</h1>
  <span>搜尋全部哩程計畫 · 支援中文輸入 · 點擊航班查看機型與訂票連結</span>
</div>

<div class="search-panel">
  <div class="search-box">
    <div class="row">
      <div class="field">
        <label>出發地</label>
        <input type="text" id="origin" placeholder="台北 / 桃園 / TPE" autocomplete="off">
        <div class="suggestions" id="origin-sug"></div>
      </div>
      <div class="swap-btn" onclick="swapAirports()" title="互換">⇄</div>
      <div class="field">
        <label>目的地</label>
        <input type="text" id="dest" placeholder="東京 / 成田 / NRT" autocomplete="off">
        <div class="suggestions" id="dest-sug"></div>
      </div>
      <div class="field">
        <label>出發日期（起）</label>
        <input type="date" id="start-date">
      </div>
      <div class="field">
        <label>出發日期（迄）</label>
        <input type="date" id="end-date">
      </div>
      <div class="field narrow">
        <label>人數</label>
        <input type="number" id="passengers" value="1" min="1" max="9">
      </div>
    </div>

    <div class="cabin-section">
      <label>艙等</label>
      <div class="cabin-options">
        <button class="cabin-btn" data-cabin="economy" onclick="toggleCabin(this)">經濟艙 Y</button>
        <button class="cabin-btn" data-cabin="premium_economy" onclick="toggleCabin(this)">豪華經濟 W</button>
        <button class="cabin-btn active" data-cabin="business" onclick="toggleCabin(this)">商務艙 J</button>
        <button class="cabin-btn" data-cabin="first" onclick="toggleCabin(this)">頭等艙 F</button>
      </div>
    </div>

    <button class="search-btn" id="search-btn" onclick="doSearch()">搜尋</button>
  </div>
</div>

<div class="results-area" id="results-area"></div>

<script>
const AIRPORT_ALIASES = """ + json.dumps(AIRPORT_ALIASES, ensure_ascii=False) + """;
const IATA_TO_CHINESE = """ + json.dumps(IATA_TO_CHINESE, ensure_ascii=False) + """;
const SOURCE_NAMES = """ + json.dumps(SOURCE_NAMES, ensure_ascii=False) + """;

// 搜尋索引
const SEARCH_INDEX = [];
const _seen = new Set();
for (const [alias, codes] of Object.entries(AIRPORT_ALIASES)) {
  for (const code of codes) {
    const key = alias + '|' + code;
    if (!_seen.has(key)) {
      _seen.add(key);
      SEARCH_INDEX.push({ alias, code, display: IATA_TO_CHINESE[code] || code });
    }
  }
}

function setupAutocomplete(inputId, sugId) {
  const input = document.getElementById(inputId);
  const sug = document.getElementById(sugId);
  input.addEventListener('input', () => {
    const val = input.value.trim();
    if (!val) { sug.classList.remove('show'); return; }
    const upper = val.toUpperCase();
    const results = SEARCH_INDEX.filter(item =>
      item.alias.includes(val) || item.code.startsWith(upper) || (item.display && item.display.includes(val))
    );
    const shown = new Map();
    for (const r of results) {
      if (!shown.has(r.code)) shown.set(r.code, r);
      if (shown.size >= 8) break;
    }
    if (!shown.size) { sug.classList.remove('show'); return; }
    sug.innerHTML = [...shown.values()].map(r =>
      `<div class="sug-item" onclick="selectAirport('${inputId}','${sugId}','${r.alias}')">
        <span>${r.display || r.alias}</span>
        <span class="sug-iata">${r.code}</span>
      </div>`
    ).join('');
    sug.classList.add('show');
  });
  document.addEventListener('click', e => {
    if (!input.contains(e.target) && !sug.contains(e.target)) sug.classList.remove('show');
  });
}

function selectAirport(inputId, sugId, alias) {
  document.getElementById(inputId).value = alias;
  document.getElementById(sugId).classList.remove('show');
}

function swapAirports() {
  const o = document.getElementById('origin');
  const d = document.getElementById('dest');
  [o.value, d.value] = [d.value, o.value];
}

function toggleCabin(btn) { btn.classList.toggle('active'); }

function resolveInput(val) {
  val = val.trim();
  if (val.length === 3 && /^[A-Za-z]{3}$/.test(val)) return [val.toUpperCase()];
  if (AIRPORT_ALIASES[val]) return AIRPORT_ALIASES[val];
  for (const [alias, codes] of Object.entries(AIRPORT_ALIASES)) {
    if (val.includes(alias) || alias.includes(val)) return codes;
  }
  return null;
}

setupAutocomplete('origin', 'origin-sug');
setupAutocomplete('dest', 'dest-sug');

// 預設日期
const today = new Date();
const later = new Date(today);
later.setMonth(later.getMonth() + 3);
document.getElementById('start-date').value = today.toISOString().slice(0,10);
document.getElementById('end-date').value = later.toISOString().slice(0,10);

let sortCol = 'date';
let sortDir = 1;
let currentData = [];

const CABIN_CODES = { economy:'Y', premium_economy:'W', business:'J', first:'F' };
const CABIN_LABELS = { Y:'經濟', W:'豪華經濟', J:'商務', F:'頭等' };

// 機型分類
function classifyAircraft(name, code) {
  const c = (code || '').toUpperCase();
  const n = (name || '').toLowerCase();
  // 真平躺商務
  const lieFlat = ['77W','77L','772','773','777','789','788','787','359','35K','350','388','380','345','343','342','A380','A350','A340'];
  // 大多數長程 A330 也是平躺
  const lieFlatNames = ['777','787','dreamliner','a350','a380','a340'];
  for (const p of lieFlat) if (c === p || c.startsWith(p)) return 'lieflat';
  for (const p of lieFlatNames) if (n.includes(p)) return 'lieflat';
  // A330 大多是平躺，但有例外
  if (c.startsWith('332') || c.startsWith('333') || n.includes('a330')) return 'lieflat';
  // 767：長程通常平躺，短程可能不是
  if (c.startsWith('76') || n.includes('767')) return 'mixed';
  // 757、737、A320 家族：商務艙通常只是隔一個座位
  const recliner = ['752','753','757','738','739','737','73','32','31','319','320','321','E17','E19','E7','CRJ','AT7','AT4'];
  for (const p of recliner) if (c.startsWith(p)) return 'recliner';
  if (n.includes('737') || n.includes('a320') || n.includes('a319') || n.includes('a321') || n.includes('757') || n.includes('embraer') || n.includes('crj')) return 'recliner';
  return 'unknown';
}

function aircraftBadge(name, code) {
  const cls = classifyAircraft(name, code);
  if (cls === 'lieflat') return '<span class="lieflat-badge">✅ 平躺商務</span>';
  if (cls === 'mixed') return '<span class="mixed-badge">⚠️ 看航空公司</span>';
  if (cls === 'recliner') return '<span class="recliner-badge">❌ 非平躺</span>';
  return '';
}

function fmtTime(iso) {
  if (!iso) return '-';
  const d = new Date(iso);
  // 顯示 UTC 時間（seats.aero 給的是 local time stored as UTC）
  return d.toLocaleString('zh-TW', {month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit',hour12:false,timeZone:'UTC'});
}

function fmtDuration(mins) {
  if (!mins) return '';
  const h = Math.floor(mins/60), m = mins%60;
  return `${h}h${m > 0 ? m+'m' : ''}`;
}

// Trip 詳情快取
const tripCache = new Map();

async function toggleDetail(availId, cabinCode, rowIdx) {
  const detailRow = document.getElementById('detail-' + rowIdx);
  const inner = detailRow.querySelector('.detail-inner');
  if (inner.classList.contains('open')) {
    inner.classList.remove('open');
    return;
  }
  inner.classList.add('open');
  if (inner.dataset.loaded) return;

  inner.innerHTML = '<div class="loading-detail"><span class="spinner"></span>載入班機資訊...</div>';

  const cacheKey = availId + '-' + cabinCode;
  let data = tripCache.get(cacheKey);
  if (!data) {
    try {
      const resp = await fetch('/api/trips/' + availId + '?cabin=' + cabinCode);
      data = await resp.json();
      tripCache.set(cacheKey, data);
    } catch (e) {
      inner.innerHTML = `<div class="error-msg">無法載入班機資訊：${e.message}</div>`;
      return;
    }
  }

  if (data.error || !data.data || !data.data.length) {
    inner.innerHTML = '<div class="loading-detail">無詳細班機資訊</div>';
    inner.dataset.loaded = '1';
    return;
  }

  // 只顯示符合艙等的 trips
  const trips = data.data.filter(t => !cabinCode || t.Cabin === cabinCode);
  const bookingLinks = data.booking_links || [];

  const cards = trips.map(trip => {
    const segs = trip.AvailabilitySegments || [];
    const aircraft = (trip.Aircraft || []).join(', ');
    const firstCode = segs.length ? (segs[0].AircraftCode || '') : '';
    const badge = (cabinCode === 'J' || cabinCode === 'F') ? aircraftBadge(aircraft, firstCode) : '';

    const segHtml = segs.map((seg, i) => `
      <div class="seg-row">
        <span class="seg-airports">
          <span class="airport-tag">${seg.OriginAirport}</span>
          → <span class="airport-tag">${seg.DestinationAirport}</span>
        </span>
        <span class="flight-num">${seg.FlightNumber || ''}</span>
        <span class="time-info">${fmtTime(seg.DepartsAt)}<span class="time-arrow">→</span>${fmtTime(seg.ArrivesAt)}</span>
        <span class="duration">${fmtDuration(seg.Duration)}</span>
        <span class="aircraft-name">${seg.AircraftName || seg.AircraftCode || ''}</span>
      </div>
    `).join('');

    const stopsLabel = trip.Stops > 0 ? `<span class="stops-label">${trip.Stops}次轉機</span>` : '';

    return `
      <div class="trip-card">
        <div class="trip-card-header">
          <div>
            <div class="flight-info">${stopsLabel} ${trip.FlightNumbers || ''}</div>
            <div class="aircraft-info">
              <span class="aircraft-name">✈ ${aircraft || '未知機型'}</span>
              ${badge}
            </div>
          </div>
          <div style="text-align:right">
            <div style="font-size:12px;color:#718096">剩餘 ${trip.RemainingSeats || '-'} 席</div>
            <div style="font-size:13px;font-weight:600;color:#b794f4">${trip.MileageCost ? trip.MileageCost.toLocaleString() + ' 哩' : ''}</div>
          </div>
        </div>
        ${segHtml}
      </div>
    `;
  }).join('');

  const linksHtml = bookingLinks.length ? `
    <div class="book-links">
      ${bookingLinks.slice(0,5).map(l =>
        `<a class="book-btn ${l.primary?'primary':''}" href="${l.link}" target="_blank" rel="noopener">${l.label}</a>`
      ).join('')}
    </div>
  ` : '';

  inner.innerHTML = `<div class="trip-cards">${cards}</div>${linksHtml}`;
  inner.dataset.loaded = '1';
}

function doSearch() {
  const originVal = document.getElementById('origin').value.trim();
  const destVal = document.getElementById('dest').value.trim();
  const startDate = document.getElementById('start-date').value;
  const endDate = document.getElementById('end-date').value;
  const passengers = parseInt(document.getElementById('passengers').value) || 1;

  const originCodes = resolveInput(originVal);
  const destCodes = resolveInput(destVal);

  if (!originCodes?.length) { alert('找不到出發地機場'); return; }
  if (!destCodes?.length) { alert('找不到目的地機場'); return; }

  const activeCabins = [...document.querySelectorAll('.cabin-btn.active')].map(b => b.dataset.cabin);
  if (!activeCabins.length) { alert('請選擇至少一個艙等'); return; }

  const area = document.getElementById('results-area');
  area.innerHTML = '<div class="loading-full"><span class="spinner-lg"></span>搜尋中...</div>';
  document.getElementById('search-btn').disabled = true;

  const params = new URLSearchParams({
    origin: originCodes.join(','),
    dest: destCodes.join(','),
    cabin: activeCabins.join(','),
    start: startDate,
    end: endDate,
  });

  fetch('/api/search?' + params)
    .then(r => r.json())
    .then(data => {
      document.getElementById('search-btn').disabled = false;
      if (data.error) { area.innerHTML = `<div class="error-msg">錯誤：${data.error}</div>`; return; }
      currentData = data.results || [];
      renderResults(currentData, originCodes, destCodes, passengers, activeCabins);
    })
    .catch(e => {
      document.getElementById('search-btn').disabled = false;
      area.innerHTML = `<div class="error-msg">搜尋失敗：${e.message}</div>`;
    });
}

function renderResults(rows, originCodes, destCodes, passengers, activeCabins) {
  const area = document.getElementById('results-area');

  // 展開成每艙等一筆
  const flat = [];
  for (const r of rows) {
    for (const [cabinKey, code] of Object.entries(CABIN_CODES)) {
      if (!activeCabins || !activeCabins.includes(cabinKey)) continue;
      if (!r[code + 'Available']) continue;
      const seats = r[code + 'RemainingSeatsRaw'] || 0;
      if (seats < passengers) continue; // 人數過濾
      flat.push({
        id: r.ID,
        date: r.Date,
        source: r.Source,
        origin: r.Route?.OriginAirport || '',
        dest: r.Route?.DestinationAirport || '',
        cabinKey,
        cabin: code,
        miles: r[code + 'MileageCostRaw'] || 0,
        taxes: r[code + 'TotalTaxesRaw'] || 0,
        seats,
        direct: r[code + 'Direct'],
        airlines: r[code + 'Airlines'] || '',
        currency: r.TaxesCurrency || 'USD',
      });
    }
  }

  const originLabel = originCodes.map(c => IATA_TO_CHINESE[c] || c).join(' / ');
  const destLabel = destCodes.map(c => IATA_TO_CHINESE[c] || c).join(' / ');

  if (!flat.length) {
    area.innerHTML = `
      <div class="no-results">
        😔 查無符合 ${passengers} 人的可用票位<br>
        <span style="font-size:13px;margin-top:8px;display:block">試試放寬日期、減少人數，或換個目的地</span>
      </div>`;
    return;
  }

  // 排序
  flat.sort((a, b) => {
    let av, bv;
    if (sortCol === 'date') { av = a.date; bv = b.date; }
    else if (sortCol === 'miles') { av = a.miles; bv = b.miles; }
    else if (sortCol === 'seats') { av = a.seats; bv = b.seats; }
    else { av = a.date; bv = b.date; }
    if (av < bv) return -sortDir;
    if (av > bv) return sortDir;
    return 0;
  });

  function sortIcon(col) {
    if (sortCol !== col) return '<span style="opacity:.3">↕</span>';
    return sortDir > 0 ? '↑' : '↓';
  }

  function seatsClass(n) {
    if (n >= 4) return 'seats-ok';
    if (n >= 2) return 'seats-warn';
    return 'seats-low';
  }

  const rows2 = flat.map((r, i) => `
    <tr class="data-row" onclick="toggleDetail('${r.id}','${r.cabin}',${i})">
      <td>${r.date} <span class="expand-icon">▸</span></td>
      <td><span class="airport-tag">${r.origin}</span> → <span class="airport-tag">${r.dest}</span></td>
      <td>${SOURCE_NAMES[r.source] || r.source}</td>
      <td><span class="cabin-tag cabin-${r.cabin}">${CABIN_LABELS[r.cabin]}</span></td>
      <td><span class="miles">${r.miles > 0 ? r.miles.toLocaleString() : '-'}</span> <span class="miles-unit">哩</span></td>
      <td>${r.taxes > 0 ? (r.taxes/100).toFixed(0) + ' ' + r.currency : '-'}</td>
      <td><span class="seats-num ${seatsClass(r.seats)}">${r.seats}</span></td>
      <td>${r.direct ? '<span class="direct-badge">直飛</span>' : '<span class="indirect-badge">轉機</span>'}</td>
      <td style="font-size:12px;color:#a0aec0">${r.airlines}</td>
    </tr>
    <tr class="detail-row" id="detail-${i}">
      <td colspan="9"><div class="detail-inner"></div></td>
    </tr>
  `).join('');

  area.innerHTML = `
    <div class="results-header">
      <div>
        <div class="results-title">${originLabel} → ${destLabel}</div>
        <div class="results-count">共 ${flat.length} 筆 · 需求 ${passengers} 席 · 點擊行查看機型與訂票連結</div>
      </div>
    </div>
    <div class="table-wrap">
    <table>
      <thead><tr>
        <th onclick="resort('date')">日期 ${sortIcon('date')}</th>
        <th>航線</th>
        <th>哩程計畫</th>
        <th>艙等</th>
        <th onclick="resort('miles')">哩程數 ${sortIcon('miles')}</th>
        <th>稅費</th>
        <th onclick="resort('seats')">剩餘座位 ${sortIcon('seats')}</th>
        <th>直飛</th>
        <th>航空公司</th>
      </tr></thead>
      <tbody>${rows2}</tbody>
    </table>
    </div>
  `;
}

function resort(col) {
  if (sortCol === col) sortDir = -sortDir;
  else { sortCol = col; sortDir = 1; }
  const passengers = parseInt(document.getElementById('passengers').value) || 1;
  const activeCabins = [...document.querySelectorAll('.cabin-btn.active')].map(b => b.dataset.cabin);
  const originCodes = resolveInput(document.getElementById('origin').value) || [];
  const destCodes = resolveInput(document.getElementById('dest').value) || [];
  renderResults(currentData, originCodes, destCodes, passengers, activeCabins);
}

document.addEventListener('keydown', e => {
  if (e.key === 'Enter' && e.target.tagName !== 'BUTTON') doSearch();
});
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"  {args[0]} {args[1]}")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))

        elif parsed.path == "/api/search":
            qs = urllib.parse.parse_qs(parsed.query)
            origin_codes = qs.get("origin", [""])[0].split(",")
            dest_codes   = qs.get("dest",   [""])[0].split(",")
            cabins       = qs.get("cabin",  ["business"])[0].split(",")
            start_date   = qs.get("start",  [""])[0]
            end_date     = qs.get("end",    [""])[0]

            all_results = []
            for cabin in cabins:
                results = search_awards(origin_codes, dest_codes, cabin, start_date, end_date)
                all_results.extend(results)

            seen = set()
            deduped = []
            for r in all_results:
                if r["ID"] not in seen:
                    seen.add(r["ID"])
                    deduped.append(r)

            resp = json.dumps({"results": deduped}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(resp)

        elif parsed.path.startswith("/api/trips/"):
            avail_id = parsed.path[len("/api/trips/"):]
            data = get_trips(avail_id)
            resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(resp)

        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8888))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print("✈  哩程機票查詢系統啟動中")
    print(f"   開啟瀏覽器：http://localhost:{port}")
    print("   Ctrl+C 停止")
    server.serve_forever()
