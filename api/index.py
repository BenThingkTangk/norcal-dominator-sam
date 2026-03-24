"""NorCal Insurance Dominator — Vercel Serverless FastAPI Backend."""

import json, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from api.data import NORCAL_COUNTIES, CARRIER_INTEL, SYSTEM_PROMPT_BASE

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    messages: list
    system_context: Optional[str] = None

class PitchRequest(BaseModel):
    prospect_name: str
    carrier: Optional[str] = None
    county: Optional[str] = None
    lines: Optional[str] = None
    experience_years: Optional[int] = None
    book_size: Optional[int] = None
    pain_points: Optional[str] = None
    stage: Optional[str] = None

class ObjectionRequest(BaseModel):
    objection: str
    prospect_context: Optional[str] = None

class IntelRequest(BaseModel):
    county: Optional[str] = None
    carrier: Optional[str] = None
    query: Optional[str] = None

def call_claude(system: str, messages: list, max_tokens: int = 2048):
    from anthropic import Anthropic
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return JSONResponse(content={"error": "ANTHROPIC_API_KEY not set"}, status_code=500)
    client = Anthropic(api_key=api_key)
    # Try models in order of preference
    models = ["claude-sonnet-4-20250514", "claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"]
    last_error = None
    for model in models:
        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=messages,
            )
            return JSONResponse(content={"text": response.content[0].text})
        except Exception as e:
            last_error = str(e)
            if "credit balance" not in last_error and "model" not in last_error.lower():
                break  # Non-model/billing error, don't retry
            continue
    return JSONResponse(content={"error": last_error}, status_code=500)

@app.post("/api/chat")
async def chat(req: ChatRequest):
    system = SYSTEM_PROMPT_BASE
    if req.system_context:
        system += "\n\nADDITIONAL CONTEXT:\n" + req.system_context
    return call_claude(system, req.messages)

@app.post("/api/pitch")
async def pitch(req: PitchRequest):
    county_data = NORCAL_COUNTIES.get(req.county, {}) if req.county else {}
    carrier_data = None
    if req.carrier:
        for k, v in CARRIER_INTEL.items():
            if k.lower() in req.carrier.lower() or req.carrier.lower() in k.lower():
                carrier_data = v
                break
    prompt = f"""Generate a tailored recruiting pitch.

PROSPECT: {req.prospect_name} | Carrier: {req.carrier or 'Unknown'} | County: {req.county or 'Unknown'} | Lines: {req.lines or 'Unknown'} | Experience: {req.experience_years or 'Unknown'} yrs | Book: {'$'+f'{req.book_size:,}' if req.book_size else 'Unknown'} | Pain: {req.pain_points or 'None'} | Stage: {req.stage or 'Unknown'}
{"COUNTY: " + json.dumps(county_data) if county_data else ""}
{"CARRIER: " + json.dumps(carrier_data) if carrier_data else ""}

Sections: 1. OPENING HOOK 2. PAIN AMPLIFICATION 3. THE BRIDGE 4. SOCIAL PROOF 5. CALL TO ACTION 6. EQ NOTES. Use real data."""
    return call_claude(SYSTEM_PROMPT_BASE, [{"role": "user", "content": prompt}])

@app.post("/api/objection")
async def objection(req: ObjectionRequest):
    prompt = f"""Objection: "{req.objection}"
{"Context: " + req.prospect_context if req.prospect_context else ""}

Respond with: 1. ACKNOWLEDGE 2. REFRAME (with data) 3. WORD-FOR-WORD REBUTTAL 4. FOLLOW-UP QUESTION 5. EMOTIONAL READ 6. IF THEY PUSH BACK AGAIN. Be tactical."""
    return call_claude(SYSTEM_PROMPT_BASE, [{"role": "user", "content": prompt}], 1500)

@app.get("/api/intel/counties")
async def counties():
    return JSONResponse(content=NORCAL_COUNTIES)

@app.get("/api/intel/carriers")
async def carriers():
    return JSONResponse(content=CARRIER_INTEL)

@app.post("/api/intel/analyze")
async def analyze(req: IntelRequest):
    ctx = []
    if req.county and req.county in NORCAL_COUNTIES:
        ctx.append(f"County: {req.county}\n{json.dumps(NORCAL_COUNTIES[req.county], indent=2)}")
    if req.carrier:
        for k, v in CARRIER_INTEL.items():
            if k.lower() in req.carrier.lower():
                ctx.append(f"Carrier: {k}\n{json.dumps(v, indent=2)}")
                break
    query = req.query or f"Brief on {req.county or req.carrier or 'NorCal market'}"
    system = SYSTEM_PROMPT_BASE + ("\n\nDATA:\n" + "\n".join(ctx) if ctx else "")
    return call_claude(system, [{"role": "user", "content": query}])

@app.get("/api/health")
async def health():
    return JSONResponse(content={"status": "dominating", "counties": len(NORCAL_COUNTIES), "carriers": len(CARRIER_INTEL), "api_key_set": bool(os.environ.get("ANTHROPIC_API_KEY"))})
