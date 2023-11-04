from fastapi import FastAPI, Request
import requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/launches", response_class=HTMLResponse)
async def get_launches(request: Request):
    response = requests.get("https://api.spacexdata.com/v4/launches")
    launches = response.json()
    extracted_data = [{"name": launch["name"], "date_utc": launch["date_utc"], "success": launch["success"]} for launch
                      in launches]
    return templates.TemplateResponse("launches.html", {"request": request, "launches": extracted_data})
