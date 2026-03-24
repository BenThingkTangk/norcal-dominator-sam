"""Shared data module — NorCal county + carrier intelligence."""
import json

NORCAL_COUNTIES = {
    "Alameda": {"fair_plan_policies": 11694, "yoy_growth": "73%", "pop": 1682353, "risk": "Moderate", "top_carriers_exited": ["State Farm", "Allstate"], "fire_hazard": "High in hills"},
    "Alpine": {"fair_plan_policies": 392, "yoy_growth": "13%", "pop": 1204, "risk": "Very High", "top_carriers_exited": ["Most carriers"], "fire_hazard": "Very High"},
    "Amador": {"fair_plan_policies": 6186, "yoy_growth": "13%", "pop": 41259, "risk": "Very High", "top_carriers_exited": ["State Farm", "Nationwide"], "fire_hazard": "Very High"},
    "Butte": {"fair_plan_policies": 9392, "yoy_growth": "15%", "pop": 211632, "risk": "Very High", "top_carriers_exited": ["State Farm", "Allstate", "Nationwide"], "fire_hazard": "Very High — Camp Fire history"},
    "Calaveras": {"fair_plan_policies": 10572, "yoy_growth": "11%", "pop": 46221, "risk": "Very High", "top_carriers_exited": ["State Farm", "Farmers"], "fire_hazard": "Very High"},
    "Colusa": {"fair_plan_policies": 68, "yoy_growth": "42%", "pop": 22401, "risk": "Low", "top_carriers_exited": [], "fire_hazard": "Moderate"},
    "Contra Costa": {"fair_plan_policies": 12837, "yoy_growth": "96%", "pop": 1165927, "risk": "High", "top_carriers_exited": ["State Farm", "Allstate"], "fire_hazard": "High in east hills"},
    "Del Norte": {"fair_plan_policies": 572, "yoy_growth": "62%", "pop": 27743, "risk": "Moderate", "top_carriers_exited": ["Nationwide"], "fire_hazard": "Moderate"},
    "El Dorado": {"fair_plan_policies": 28167, "yoy_growth": "18%", "pop": 193221, "risk": "Extreme", "top_carriers_exited": ["State Farm", "Allstate", "Nationwide", "Farmers"], "fire_hazard": "Very High — Caldor Fire history"},
    "Fresno": {"fair_plan_policies": 5821, "yoy_growth": "25%", "pop": 1013581, "risk": "Moderate", "top_carriers_exited": ["State Farm"], "fire_hazard": "Moderate-High in foothills"},
    "Glenn": {"fair_plan_policies": 58, "yoy_growth": "18%", "pop": 29316, "risk": "Low", "top_carriers_exited": [], "fire_hazard": "Low-Moderate"},
    "Humboldt": {"fair_plan_policies": 2844, "yoy_growth": "38%", "pop": 135558, "risk": "High", "top_carriers_exited": ["Nationwide"], "fire_hazard": "High"},
    "Lake": {"fair_plan_policies": 5739, "yoy_growth": "19%", "pop": 67750, "risk": "Extreme", "top_carriers_exited": ["State Farm", "Allstate", "Farmers"], "fire_hazard": "Very High — Valley Fire history"},
    "Lassen": {"fair_plan_policies": 1064, "yoy_growth": "32%", "pop": 31345, "risk": "Very High", "top_carriers_exited": ["State Farm", "Nationwide"], "fire_hazard": "Very High — Dixie Fire history"},
    "Madera": {"fair_plan_policies": 5650, "yoy_growth": "19%", "pop": 159410, "risk": "High", "top_carriers_exited": ["State Farm"], "fire_hazard": "High in foothills"},
    "Marin": {"fair_plan_policies": 4361, "yoy_growth": "51%", "pop": 262321, "risk": "High", "top_carriers_exited": ["State Farm", "Allstate"], "fire_hazard": "High — WUI zones"},
    "Mariposa": {"fair_plan_policies": 3404, "yoy_growth": "11%", "pop": 17540, "risk": "Extreme", "top_carriers_exited": ["Most carriers"], "fire_hazard": "Very High"},
    "Mendocino": {"fair_plan_policies": 4707, "yoy_growth": "22%", "pop": 91601, "risk": "Very High", "top_carriers_exited": ["State Farm", "Farmers"], "fire_hazard": "Very High"},
    "Merced": {"fair_plan_policies": 336, "yoy_growth": "68%", "pop": 286461, "risk": "Low", "top_carriers_exited": [], "fire_hazard": "Low"},
    "Modoc": {"fair_plan_policies": 290, "yoy_growth": "49%", "pop": 8661, "risk": "Very High", "top_carriers_exited": ["Most carriers"], "fire_hazard": "Very High"},
    "Mono": {"fair_plan_policies": 1982, "yoy_growth": "45%", "pop": 13247, "risk": "Very High", "top_carriers_exited": ["Most carriers"], "fire_hazard": "Very High"},
    "Monterey": {"fair_plan_policies": 5402, "yoy_growth": "28%", "pop": 439035, "risk": "High", "top_carriers_exited": ["State Farm"], "fire_hazard": "High in Big Sur / Carmel Valley"},
    "Napa": {"fair_plan_policies": 3042, "yoy_growth": "25%", "pop": 138019, "risk": "Very High", "top_carriers_exited": ["State Farm", "Allstate"], "fire_hazard": "Very High — Glass Fire history"},
    "Nevada": {"fair_plan_policies": 23438, "yoy_growth": "18%", "pop": 103487, "risk": "Extreme", "top_carriers_exited": ["State Farm", "Allstate", "Nationwide", "Farmers"], "fire_hazard": "Very High"},
    "Placer": {"fair_plan_policies": 18996, "yoy_growth": "21%", "pop": 412300, "risk": "Very High", "top_carriers_exited": ["State Farm", "Allstate", "Nationwide"], "fire_hazard": "Very High in east county"},
    "Plumas": {"fair_plan_policies": 3941, "yoy_growth": "13%", "pop": 19790, "risk": "Extreme", "top_carriers_exited": ["Most carriers"], "fire_hazard": "Very High — Dixie Fire history"},
    "Sacramento": {"fair_plan_policies": 2001, "yoy_growth": "78%", "pop": 1585055, "risk": "Low", "top_carriers_exited": [], "fire_hazard": "Low-Moderate"},
    "San Benito": {"fair_plan_policies": 388, "yoy_growth": "73%", "pop": 66677, "risk": "Moderate", "top_carriers_exited": [], "fire_hazard": "Moderate"},
    "San Francisco": {"fair_plan_policies": 2382, "yoy_growth": "76%", "pop": 873965, "risk": "Low", "top_carriers_exited": [], "fire_hazard": "Low"},
    "San Joaquin": {"fair_plan_policies": 1319, "yoy_growth": "57%", "pop": 789410, "risk": "Low", "top_carriers_exited": [], "fire_hazard": "Low"},
    "San Mateo": {"fair_plan_policies": 3759, "yoy_growth": "66%", "pop": 764442, "risk": "Moderate", "top_carriers_exited": ["State Farm"], "fire_hazard": "Moderate-High in hills"},
    "Santa Clara": {"fair_plan_policies": 6200, "yoy_growth": "69%", "pop": 1936259, "risk": "Moderate", "top_carriers_exited": ["State Farm"], "fire_hazard": "High in south county hills"},
    "Santa Cruz": {"fair_plan_policies": 12796, "yoy_growth": "60%", "pop": 270861, "risk": "Very High", "top_carriers_exited": ["State Farm", "Allstate"], "fire_hazard": "Very High — CZU Fire history"},
    "Shasta": {"fair_plan_policies": 6505, "yoy_growth": "25%", "pop": 182155, "risk": "Very High", "top_carriers_exited": ["State Farm", "Farmers"], "fire_hazard": "Very High — Carr Fire history"},
    "Sierra": {"fair_plan_policies": 541, "yoy_growth": "13%", "pop": 3236, "risk": "Extreme", "top_carriers_exited": ["Most carriers"], "fire_hazard": "Very High"},
    "Siskiyou": {"fair_plan_policies": 3269, "yoy_growth": "31%", "pop": 44076, "risk": "Very High", "top_carriers_exited": ["State Farm", "Nationwide"], "fire_hazard": "Very High"},
    "Solano": {"fair_plan_policies": 1312, "yoy_growth": "83%", "pop": 453491, "risk": "Low", "top_carriers_exited": [], "fire_hazard": "Low-Moderate"},
    "Sonoma": {"fair_plan_policies": 8748, "yoy_growth": "39%", "pop": 488863, "risk": "Very High", "top_carriers_exited": ["State Farm", "Allstate", "Farmers"], "fire_hazard": "Very High — Tubbs/Kincade history"},
    "Stanislaus": {"fair_plan_policies": 743, "yoy_growth": "78%", "pop": 552878, "risk": "Low", "top_carriers_exited": [], "fire_hazard": "Low"},
    "Sutter": {"fair_plan_policies": 118, "yoy_growth": "131%", "pop": 99063, "risk": "Low", "top_carriers_exited": [], "fire_hazard": "Low"},
    "Tehama": {"fair_plan_policies": 1783, "yoy_growth": "19%", "pop": 65498, "risk": "Very High", "top_carriers_exited": ["State Farm"], "fire_hazard": "Very High"},
    "Trinity": {"fair_plan_policies": 1440, "yoy_growth": "11%", "pop": 16060, "risk": "Extreme", "top_carriers_exited": ["Most carriers"], "fire_hazard": "Very High"},
    "Tulare": {"fair_plan_policies": 2966, "yoy_growth": "27%", "pop": 477054, "risk": "Moderate", "top_carriers_exited": ["State Farm"], "fire_hazard": "High in foothills"},
    "Tuolumne": {"fair_plan_policies": 14071, "yoy_growth": "9%", "pop": 55810, "risk": "Extreme", "top_carriers_exited": ["Most carriers"], "fire_hazard": "Very High"},
    "Yolo": {"fair_plan_policies": 251, "yoy_growth": "29%", "pop": 216403, "risk": "Low", "top_carriers_exited": [], "fire_hazard": "Low-Moderate"},
    "Yuba": {"fair_plan_policies": 1569, "yoy_growth": "11%", "pop": 82275, "risk": "Moderate", "top_carriers_exited": ["State Farm"], "fire_hazard": "High"},
}

CARRIER_INTEL = {
    "State Farm": {"status": "Halted ALL new homeowners in CA since May 2023", "impact": "Largest P&C insurer in CA — agents cannot write new HO business", "opportunity": "Agents are trapped — can't grow, losing clients to non-renewals. Biggest recruiting pool in NorCal.", "talking_point": "Your book is a melting ice cube. Every non-renewal is a client lost forever unless you move now."},
    "Allstate": {"status": "Stopped new homeowners and condo policies in CA since Nov 2022", "impact": "Complete exit from new personal lines", "opportunity": "Allstate agents have zero growth path in CA homeowners. They're watching their book shrink.", "talking_point": "Allstate has abandoned California homeowners. Your clients are getting non-renewal letters. I have carriers actively writing."},
    "Farmers": {"status": "Reduced new auto policies by ~25%, capped homeowners in fire zones since July 2023", "impact": "Severe growth limitations in NorCal fire risk counties", "opportunity": "Farmers agents in foothill/mountain counties are effectively frozen — can't write new business.", "talking_point": "Farmers has capped your growth. You can't write new homeowners in your own territory. That's not a career — that's a waiting room."},
    "Nationwide/Crestbrook": {"status": "Completely exited California personal lines — non-renewed ALL policies", "impact": "Total exit — every policyholder displaced", "opportunity": "Former Nationwide agents need a new home immediately.", "talking_point": "Nationwide didn't just stop writing — they LEFT. Every client you had is now someone else's client unless you act."},
    "AIG (Lexington)": {"status": "Reduced high-value home exposure in CA wildfire zones", "impact": "High-net-worth clients losing E&S options", "opportunity": "Agents serving HNW clients need alternative E&S markets.", "talking_point": "Your high-net-worth clients are losing Lexington coverage. I can connect you with Burns & Wilcox, Scottsdale, and other E&S markets."},
    "Hartford": {"status": "Still writing but restricting new business in high-risk zones", "impact": "Selective underwriting — turning down many apps", "opportunity": "Hartford agents dealing with increased declines.", "talking_point": "Hartford is cherry-picking which risks they'll write. If you're tired of submitting apps that get declined, let's talk about platforms with broader appetites."},
    "CSAA/AAA": {"status": "Tightening underwriting in WUI zones since 2024", "impact": "Increasing non-renewals and restrictions", "opportunity": "AAA agents losing renewals in foothill communities.", "talking_point": "CSAA is quietly non-renewing in wildfire zones. Your AAA members are losing coverage. I have solutions."},
    "Mercury": {"status": "Pulled back from high-wildfire-risk areas", "impact": "Declining new apps in mountain/foothill areas", "opportunity": "Mercury agents losing access to their own territory.", "talking_point": "Mercury won't write where you live and work. Why stay with a carrier that's retreating from your own neighborhood?"},
}

SYSTEM_PROMPT_BASE = """You are the NorCal Insurance Dominator AI — an elite insurance recruiting intelligence system built for a recruiter who recruits insurance agents and agencies in Northern California.

You have deep expertise in:
- California insurance market crisis (carrier exits, FAIR Plan explosion, wildfire risk)
- Insurance recruiting tactics and psychology
- NorCal county-by-county market intelligence
- Objection handling for insurance agent recruiting
- Emotional intelligence and persuasion techniques

REAL DATA YOU KNOW (California FAIR Plan FY2025, as of 9/30/2025):
- Total FAIR Plan policies in force: 642,010 (39% YoY growth)
- Total FAIR Plan exposure: $724 BILLION
- Total written premium: $1.98 BILLION
- NorCal counties with highest FAIR Plan concentration:
  * El Dorado: 28,167 policies (18% growth)
  * Nevada County: 23,438 policies (18% growth)
  * Placer: 18,996 policies (21% growth)
  * Tuolumne: 14,071 policies (9% growth)
  * Contra Costa: 12,837 policies (96% growth — exploding)
  * Santa Cruz: 12,796 policies (60% growth)
  * Calaveras: 10,572 policies (11% growth)
  * Alameda: 11,694 policies (73% growth)
  * Butte: 9,392 policies (15% growth)
  * Sonoma: 8,748 policies (39% growth)

CARRIER EXIT INTELLIGENCE:
""" + json.dumps(CARRIER_INTEL, indent=2) + """

COUNTY DATA:
""" + json.dumps({k: v for k, v in NORCAL_COUNTIES.items()}, indent=2) + """

RULES:
- Be direct, confident, and action-oriented. You are a recruiting weapon, not a generic chatbot.
- Use specific numbers, county data, and carrier intelligence in every response.
- Speak like a top-performing recruiter — assertive but not aggressive.
- Reference real data points to build credibility.
- When generating pitches, tailor them to the specific prospect's carrier, county, and lines of business.
- For objections, provide word-for-word rebuttals with data backing.
"""
