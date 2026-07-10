from schemas import (
    AlbumSchema,
    ArtistSchema
)

from fastapi import FastAPI
from pydantic import Field

app = FastAPI()

class ArtistQuery():
    query: bool = Field(
        description="Description of query", default=False
    )

@app.get("/api/artist")
async def get_artist(schema: ArtistSchema, query: ArtistQuery):
    artist = schema.artistsschema
    return artist