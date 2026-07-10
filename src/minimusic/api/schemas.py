from pydantic import BaseModel, Field

class AlbumSchema(BaseModel):
    albumschema: str = Field(
        description="The description of the album",
        name="The name of the album"
    )

class ArtistSchema(BaseModel):
    artistsschema: str = Field(
        hash="The hash of the artist",
        name="Name to hash"
    )
