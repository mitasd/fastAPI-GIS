from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Path
from fastapi import Body
import json
import os
from fastapi import Query
import re
from fastapi import Request, HTTPException, status


app = FastAPI()

API_TOKEN = ""  # ZAMENI OVDE SA SVOJIM TOKENOM

def proveri_token(request: Request):
    if not API_TOKEN:
        return  # Token nije postavljen – preskoči proveru
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token nije poslat")
    token = auth_header.split(" ")[1]
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Neispravan token")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GEOJSON_PATH = os.path.join(os.path.dirname(__file__), "LOKACIJE.geojson")

@app.post("/lokacije")
async def dodaj_lokaciju_formom(
    request: Request,
    broj_foldera: int = Form(...),
    Elaborat: str = Form(...),
    Datum: str = Form(...),
    Projektant: str = Form(...),
    broj_parcele: str = Form(...),
    Katastarska_opstina: str = Form(...),
    Investitor: str = Form(...),
    x: float = Form(...),
    y: float = Form(...)
):
    proveri_token(request)
    try:
        # Novi GeoJSON Feature
        novi_feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [x, y]
            },
            "properties": {
                "broj_foldera": broj_foldera,
                "Elaborat": Elaborat,
                "Datum": Datum,
                "Projektant": Projektant,
                "broj_parcele": broj_parcele,
                "Katastarska_opstina": Katastarska_opstina,
                "Investitor": Investitor
            }
        }

                # Učitaj postojeći geojson ili napravi novi ako ne postoji
        if os.path.exists(GEOJSON_PATH):
            with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
                geojson_data = json.load(f)
        else:
            geojson_data = {"type": "FeatureCollection", "features": []}

        # Dodaj novi feature u listu — OVO MORA BITI VAN `if`!
        geojson_data["features"].append(novi_feature)

        # Snimi nazad
        with open(GEOJSON_PATH, "w", encoding="utf-8") as f:
            json.dump(geojson_data, f, ensure_ascii=False, indent=2)


    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    print("Dodajem novi feature:", novi_feature)
    print("Broj feature-a:", len(geojson_data["features"]))
    return {"status": "Uspešno dodato"}



from fastapi.responses import Response

@app.get("/lokacije")
async def get_geojson(request: Request):
    proveri_token(request)
    if os.path.exists(GEOJSON_PATH):
        with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        return Response(
            content,
            media_type="application/json",
            headers={"Cache-Control": "no-store"}
        )
    return JSONResponse({"error": "GeoJSON fajl ne postoji"}, status_code=404)



@app.delete("/lokacije/{broj_foldera}")
async def obrisi_lokaciju(request: Request, broj_foldera: int = Path(..., description="Broj foldera koji želiš da obrišeš")):
    proveri_token(request)
    try:
        if not os.path.exists(GEOJSON_PATH):
            return JSONResponse({"error": "GeoJSON fajl ne postoji"}, status_code=404)

        with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

        original_len = len(geojson_data["features"])

        # Zadrži sve osim onih koji imaju taj broj_foldera
        geojson_data["features"] = [
            feat for feat in geojson_data["features"]
            if feat["properties"].get("broj_foldera") != broj_foldera
        ]

        # Provera da li je obrisano
        if len(geojson_data["features"]) == original_len:
            return JSONResponse({"status": "Nijedan feature nije obrisan", "broj_foldera": broj_foldera}, status_code=404)

        # Snimi nazad
        with open(GEOJSON_PATH, "w", encoding="utf-8") as f:
            json.dump(geojson_data, f, ensure_ascii=False, indent=2)

        return {"status": "Obrisano", "broj_foldera": broj_foldera}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    

from fastapi import Body

@app.put("/lokacije/{broj_foldera}")
def izmeni_lokaciju(request: Request, broj_foldera: int, nova: dict = Body(...)):
    proveri_token(request)

    if not os.path.exists(GEOJSON_PATH):
        return JSONResponse({"error": "GeoJSON fajl ne postoji"}, status_code=404)

    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    izmenjeno = False

    for feature in geojson["features"]:
        if feature["properties"].get("broj_foldera") == broj_foldera:
            # Ažuriraj poznata polja u properties
            for key in ["Elaborat", "Datum", "Projektant", "broj_parcele", "Katastarska_opstina", "Investitor"]:
                if key in nova:
                    feature["properties"][key] = nova[key]

            try:
                x = float(nova.get("x"))
                y = float(nova.get("y"))
                feature["geometry"]["coordinates"] = [x, y]
                print("▶︎ x iz zahteva:", x)
                print("▶︎ y iz zahteva:", y)
                print("▶︎ geometry pre:", feature["geometry"])

                feature["properties"].pop("x", None)
                feature["properties"].pop("y", None)
                print("✅ Geometry ažuriran na:", [x, y])
            except Exception as e:
                print("❌ Greška pri obradi koordinata:", e)
                return JSONResponse({"error": "Neispravne koordinate"}, status_code=400)

            izmenjeno = True
            break

    if not izmenjeno:
        return JSONResponse({"error": "Nema takvog foldera"}, status_code=404)

    with open(GEOJSON_PATH, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    return {"status": "Izmenjeno"}




from fastapi import Query

@app.get("/lokacije/filter")
def filtriraj_lokacije(
    projektant: str = Query(None),
    opstina: str = Query(None),
    investitor: str = Query(None),
    godina: str = Query(None)
):
    import json, os
    if not os.path.exists(GEOJSON_PATH):
        return JSONResponse({"error": "GeoJSON fajl ne postoji"}, status_code=404)

    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    filtrirane = []
    for feature in geojson_data["features"]:
        p = feature["properties"]
        datum = p.get("Datum", "")
        godina_iz_datuma = ""
        if isinstance(datum, str):
            match = re.search(r"(19|20)\d{2}", datum)
            if match:
                godina_iz_datuma = match.group(0)

        if projektant and projektant.lower() not in p.get("Projektant", "").lower():
            continue
        if opstina and opstina.lower() not in p.get("Katastarska_opstina", "").lower():
            continue
        if investitor and investitor.lower() not in p.get("Investitor", "").lower():
            continue
        if godina and godina != godina_iz_datuma:
            continue

        filtrirane.append(feature)

    return {"type": "FeatureCollection", "features": filtrirane}
