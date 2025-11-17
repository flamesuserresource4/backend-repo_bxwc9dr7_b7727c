import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import PaddleProduct, Player

app = FastAPI(title="Pickleball Future API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Utilities
class ObjectIdEncoder(BaseModel):
    id: Optional[str] = None


def serialize_doc(doc: dict):
    d = {**doc}
    if d.get("_id"):
        d["id"] = str(d.pop("_id"))
    return d


def ensure_seed_data():
    # Seed products
    if db is None:
        return
    if db["paddleproduct"].count_documents({}) == 0:
        samples = [
            {
                "title": "Axiom Neo Carbon X1",
                "description": "Pro-grade thermoformed paddle with carbon face and honeycomb core.",
                "price": 199.0,
                "rating": 4.9,
                "image": "https://images.unsplash.com/photo-1617957743190-efa9bade9bd1?q=80&w=1600&auto=format&fit=crop",
                "colorway": "Obsidian/Neon",
                "weight": 8.1,
                "core": "Polypropylene Honeycomb",
                "face": "T700 Raw Carbon",
                "in_stock": True,
            },
            {
                "title": "Flux Aero Pro",
                "description": "Ultra-responsive control with vibration dampening edge.",
                "price": 229.0,
                "rating": 4.8,
                "image": "https://images.unsplash.com/photo-1584291527935-456e8e2dd734?q=80&w=1600&auto=format&fit=crop",
                "colorway": "Graphite/Volt",
                "weight": 7.9,
                "core": "PP + Foam Walls",
                "face": "Toray Carbon",
                "in_stock": True,
            },
            {
                "title": "Ion Vortex S",
                "description": "Lightweight speed paddle for rapid hand battles.",
                "price": 179.0,
                "rating": 4.7,
                "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=1600&auto=format&fit=crop",
                "colorway": "Silver/Cyan",
                "weight": 7.7,
                "core": "Aramid + PP",
                "face": "Raw Carbon",
                "in_stock": True,
            },
        ]
        for s in samples:
            create_document("paddleproduct", s)

    # Seed players
    if db["player"].count_documents({}) == 0:
        players = [
            {
                "name": "Nova Reyes",
                "slug": "nova-reyes",
                "country": "USA",
                "flag": "🇺🇸",
                "ranking": 1,
                "dupr": 7.4,
                "portrait": "https://images.unsplash.com/photo-1546527868-ccb7ee7dfa6a?q=80&w=1200&auto=format&fit=crop",
                "bio": "Aggressive right-side player known for surgical thirds and fearless speed-ups.",
                "achievements": [
                    {"year": 2024, "title": "Pro Tour Finals Champion", "event": "PPA"},
                    {"year": 2023, "title": "US Open Gold", "event": "Mixed"},
                ],
                "socials": {"instagram": 320000, "tiktok": 210000, "youtube": 90000},
                "highlights": [
                    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    "https://www.youtube.com/watch?v=oHg5SJYRHA0",
                ],
            },
            {
                "name": "Kai Nakamura",
                "slug": "kai-nakamura",
                "country": "JPN",
                "flag": "🇯🇵",
                "ranking": 2,
                "dupr": 7.2,
                "portrait": "https://images.unsplash.com/photo-1527980965255-d3b416303d12?q=80&w=1200&auto=format&fit=crop",
                "bio": "Control-first lefty with elite resets and deceptive roll volleys.",
                "achievements": [
                    {"year": 2024, "title": "Masters Silver"},
                    {"year": 2023, "title": "Asia Open Champion"},
                ],
                "socials": {"instagram": 150000, "tiktok": 120000, "youtube": 60000},
                "highlights": [
                    "https://www.youtube.com/watch?v=ysz5S6PUM-U",
                ],
            },
            {
                "name": "Lena Kovac",
                "slug": "lena-kovac",
                "country": "SLO",
                "flag": "🇸🇮",
                "ranking": 3,
                "dupr": 7.0,
                "portrait": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=1200&auto=format&fit=crop",
                "bio": "Relentless tempo with feather-light hands and pinpoint dinks.",
                "achievements": [
                    {"year": 2024, "title": "European Champs Gold"},
                    {"year": 2022, "title": "Rookie of the Year"},
                ],
                "socials": {"instagram": 180000, "tiktok": 80000, "youtube": 40000},
                "highlights": [
                    "https://www.youtube.com/watch?v=jNQXAC9IVRw",
                ],
            },
        ]
        for p in players:
            create_document("player", p)


@app.on_event("startup")
async def startup_event():
    try:
        ensure_seed_data()
    except Exception:
        pass


@app.get("/")
def read_root():
    return {"message": "Pickleball Future API is running"}


@app.get("/api/products")
def list_products():
    try:
        docs = get_documents("paddleproduct")
        return [serialize_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/players")
def list_players():
    try:
        docs = get_documents("player")
        # Sort by ranking ascending
        docs = sorted(docs, key=lambda d: d.get("ranking", 999))
        return [serialize_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/players/{slug}")
def get_player(slug: str):
    try:
        docs = db["player"].find_one({"slug": slug})
        if not docs:
            raise HTTPException(status_code=404, detail="Player not found")
        return serialize_doc(docs)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
