from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_BASE_URL = "https://api.themoviedb.org/3"

class SearchRequest(BaseModel):
    query: str
    api_key: str
    language: str = "ru-RU"

class MovieRequest(BaseModel):
    movie_id: int
    api_key: str
    language: str = "ru-RU"

@app.post("/api/search/movie")
async def search_movie(request: SearchRequest):
    try:
        response = requests.get(
            f"{TMDB_BASE_URL}/search/movie",
            params={
                "api_key": request.api_key,
                "query": request.query,
                "language": request.language
            }
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/movie/{movie_id}")
async def get_movie(movie_id: int, request: MovieRequest):
    try:
        response = requests.get(
            f"{TMDB_BASE_URL}/movie/{movie_id}",
            params={
                "api_key": request.api_key,
                "language": request.language
            }
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 