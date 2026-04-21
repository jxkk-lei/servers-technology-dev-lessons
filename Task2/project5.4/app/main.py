from fastapi import FastAPI, Request, HTTPException

app = FastAPI()


@app.get("/headers")
async def get_headers(request: Request):
    user_agent = request.headers.get("User-Agent")
    accept_language = request.headers.get("Accept-Language")

    if not user_agent or not accept_language:
        raise HTTPException(
            status_code=400,
            detail="Missing required headers"
        )

    if "," not in accept_language:
        raise HTTPException(
            status_code=400,
            detail="Invalid Accept-Language format"
        )

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }