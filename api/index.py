"""NorCal Insurance Dominator — Vercel Serverless FastAPI Backend.
All AI endpoints for the Objection Handler, Pitch Generator, and Market Intel Agent."""

import json, os, traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional

# Import shared data
from api.data import NORCAL_COUNTIES, CARRIER_INTEL, SYSTEM_PROMPT_BASE

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def get_client():
    from anthropic import Anthropic
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    return Anthropic(api_key=api_key)

# ═══════ REQUEST MODELS ═══════
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

# ═══════ STREAMING HELPER ═══════
def stream_anthropic(system: str, messages: list, max_tokens: int = 2048):
    def generate():
        try:
            client = get_client()
            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                system=system,
                messages=messages,
            ) as stream:
                for text in stream.text_stream:
                    yield f"data: {json.dumps({'text': text})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            yield f"data: {json.dumps({'text': error_msg})}\n\n"
            yield "data: [DONE]\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")

# ═══════ NON-STREAMING FALLBACK (for debugging) ═══════
def call_anthropic(system: str, messages: list, max_tokens: int = 2048):
    try:
        client = get_client()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        text = response.content[0].text
        # Return as SSE chunks for frontend compatibility
        def generate():
            chunk_size = 100
            for i in range(0, len(text), chunk_size):
                yield f"data: {json.dumps({'text': text[i:i+chunk_size]})}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(generate(), media_type="text/event-stream")
    except Exception as e:
        def error_gen():
            yield f"data: {json.dumps({'text': f'Error: {str(e)}'})}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(error_gen(), media_type="text/event-stream")

# ═══════ STREAMING CHAT ═══════
@app.post("/api/chat")
async def chat_stream(req: ChatRequest):
    system = SYSTEM_PROMPT_BASE
    if req.system_context:
        system += "\n\nADDITIONAL CONTEXT:\n" + req.system_context
    return call_anthropic(system, req.messages)

# ═══════ PITCH GENERATOR ═══════
@app.post("/api/pitch")
async def generate_pitch(req: PitchRequest):
    county_data = NORCAL_COUNTIES.get(req.county, {}) if req.county else {}
    carrier_data = None
    if req.carrier:
        for k, v in CARRIER_INTEL.items():
            if k.lower() in req.carrier.lower() or req.carrier.lower() in k.lower():
                carrier_data = v
                break

    pitch_prompt = f"""Generate a tailored, high-impact recruiting pitch for this specific prospect. Make it personal, data-driven, and emotionally compelling.

PROSPECT PROFILE:
- Name: {req.prospect_name}
- Current Carrier/Agency: {req.carrier or 'Unknown'}
- County: {req.county or 'Unknown'}
- Lines of Business: {req.lines or 'Unknown'}
- Years of Experience: {req.experience_years or 'Unknown'}
- Book Size: {'$' + f'{req.book_size:,}' if req.book_size else 'Unknown'}
- Known Pain Points: {req.pain_points or 'None specified'}
- Pipeline Stage: {req.stage or 'Unknown'}

{"COUNTY INTEL: " + json.dumps(county_data) if county_data else ""}
{"CARRIER INTEL: " + json.dumps(carrier_data) if carrier_data else ""}

Generate a pitch with these sections:
1. **OPENING HOOK** — A bold, personalized opening line. Maximum 2 sentences.
2. **PAIN AMPLIFICATION** — 2-3 sentences with specific data.
3. **THE BRIDGE** — What you offer that solves their specific problem.
4. **SOCIAL PROOF** — Brief reference to other agents who've moved.
5. **CALL TO ACTION** — A specific, time-bounded next step.
6. **EMOTIONAL INTELLIGENCE NOTES** — Coaching notes on tone and triggers.

Be specific. Use real data. No generic fluff."""

    return call_anthropic(SYSTEM_PROMPT_BASE, [{"role": "user", "content": pitch_prompt}])

# ═══════ OBJECTION HANDLER ═══════
@app.post("/api/objection")
async def handle_objection(req: ObjectionRequest):
    objection_prompt = f"""A prospect just hit me with this objection during a recruiting conversation:

OBJECTION: "{req.objection}"

{"PROSPECT CONTEXT: " + req.prospect_context if req.prospect_context else ""}

Generate a powerful response with:

1. **ACKNOWLEDGE** — Show you heard them (1 sentence, empathetic)
2. **REFRAME** — Flip the objection using specific data (2-3 sentences)
3. **WORD-FOR-WORD REBUTTAL** — Exact words to say, in quotes
4. **FOLLOW-UP QUESTION** — Strategic question to keep the conversation going
5. **EMOTIONAL READ** — What they're really feeling underneath
6. **IF THEY PUSH BACK AGAIN** — A second-level response

Be direct and tactical. This is a live conversation."""

    return call_anthropic(SYSTEM_PROMPT_BASE, [{"role": "user", "content": objection_prompt}], max_tokens=1500)

# ═══════ INTEL ENDPOINTS ═══════
@app.get("/api/intel/counties")
async def get_counties():
    return JSONResponse(content=NORCAL_COUNTIES)

@app.get("/api/intel/carriers")
async def get_carriers():
    return JSONResponse(content=CARRIER_INTEL)

@app.post("/api/intel/analyze")
async def analyze_intel(req: IntelRequest):
    context_parts = []
    if req.county:
        data = NORCAL_COUNTIES.get(req.county, {})
        if data:
            context_parts.append(f"County: {req.county}\n{json.dumps(data, indent=2)}")
    if req.carrier:
        for k, v in CARRIER_INTEL.items():
            if k.lower() in req.carrier.lower() or req.carrier.lower() in k.lower():
                context_parts.append(f"Carrier: {k}\n{json.dumps(v, indent=2)}")
                break

    query = req.query or f"Give me a full intelligence briefing on {req.county or req.carrier or 'the NorCal market'}"
    system = SYSTEM_PROMPT_BASE + ("\n\nRELEVANT DATA:\n" + "\n".join(context_parts) if context_parts else "")
    return call_anthropic(system, [{"role": "user", "content": query}])

# ═══════ HEALTH CHECK ═══════
@app.get("/api/health")
async def health():
    has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    return JSONResponse(content={
        "status": "dominating",
        "counties": len(NORCAL_COUNTIES),
        "carriers": len(CARRIER_INTEL),
        "api_key_set": has_key
    })
