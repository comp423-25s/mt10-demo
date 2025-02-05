"""An API for Thingies!"""

__author__ = "Kris Jordan <kris@cs.unc.edu>"

from typing import Annotated
from fastapi import FastAPI, Body, Response, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()


class Thingy(BaseModel):
    """A Thingy!"""

    id: Annotated[str, Field(description="Resource ID", examples=["1234"])]

    redirect_url: Annotated[
        str, Field(description="URL redirected to", examples=["https://csxl.unc.edu"])
    ] = ""

    snippet_text: Annotated[
        str, Field(description="Snippet text", examples=["Hello, world"])
    ] = "... no snippet text ..."


"""A 'Database' of Thingies (... this is *not* a database! :)"""
thingies_db: dict[str, Thingy] = {}


@app.post("/", summary="Create a Thingy")
def thingy_new(
    thingy: Annotated[Thingy, Body(description="Thingy to Create")]
) -> Thingy:
    thingies_db[thingy.id] = thingy
    return thingies_db[thingy.id]


@app.get("/{thingy_id}", summary="Load a Thingy")
def thingy_too(
    thingy_id: Annotated[str, Path(description="Thingy Identifier")]
) -> Response:
    thingy: Thingy | None = thingies_db.get(thingy_id)
    if thingy:
        if thingy.snippet_text:
            return Response(content=thingy.snippet_text, media_type="text/plain")
        else:
            return Response(status_code=302, headers={"Location": thingy.redirect_url})
    else:
        return JSONResponse(status_code=404, content={"error": "Resource not found"})
