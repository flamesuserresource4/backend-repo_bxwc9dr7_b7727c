"""
Database Schemas for Pickleball E‑commerce

Each Pydantic model maps to a MongoDB collection named after the
lowercased class name (e.g., PaddleProduct -> "paddleproduct").
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List


class PaddleProduct(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Short description")
    price: float = Field(..., ge=0, description="Price in USD")
    rating: float = Field(4.8, ge=0, le=5, description="Average rating out of 5")
    image: Optional[HttpUrl] = Field(None, description="Primary product image URL")
    colorway: Optional[str] = Field(None, description="Colorway or finish")
    weight: Optional[float] = Field(None, description="Weight in ounces")
    core: Optional[str] = Field(None, description="Core material")
    face: Optional[str] = Field(None, description="Face material")
    in_stock: bool = Field(True, description="Availability flag")


class SocialStats(BaseModel):
    instagram: Optional[int] = 0
    tiktok: Optional[int] = 0
    youtube: Optional[int] = 0


class PlayerAchievement(BaseModel):
    year: int
    title: str
    event: Optional[str] = None


class Player(BaseModel):
    name: str
    slug: str = Field(..., description="URL-friendly identifier")
    country: str
    flag: str = Field(..., description="Emoji or URL for flag icon")
    ranking: int
    dupr: float = Field(..., ge=0, le=8)
    portrait: Optional[HttpUrl] = None
    bio: Optional[str] = None
    achievements: List[PlayerAchievement] = []
    socials: SocialStats = SocialStats()
    highlights: List[HttpUrl] = []
