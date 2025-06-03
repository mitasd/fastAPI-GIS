# 🌍 FastAPI GIS — Geotechnical Project Manager

A full-stack GIS application for managing and visualizing geotechnical project locations using a FastAPI backend, GeoJSON data, and an HTML + ArcGIS JavaScript frontend.

---

## 🚀 Features

- Add, update, delete, and filter project locations via REST API
- Store spatial data as a GeoJSON file (`LOKACIJE.geojson`)
- View and manage data in a responsive HTML table interface
- Visualize project points on an interactive ArcGIS map with dynamic basemaps
- Simple frontend served independently (via `index.html` and `mapa.html`)
- Token-protected endpoints

---

## 🛠️ Tech Stack

- ⚙️ **FastAPI** – backend API server
- 🗺️ **ArcGIS JS API** – map rendering
- 📄 **GeoJSON** – spatial data storage
- 🧪 **HTML + Bootstrap + JavaScript** – user interface
- 🐳 **Docker** – containerization (optional)

---

## 📦 Project Structure
fastAPI-GIS/
├── app.py # FastAPI backend with all endpoints
├── index.html # Project table interface
├── mapa.html # ArcGIS-based map visualization
├── LOKACIJE.geojson # Stored project locations
├── Dockerfile # Docker configuration (optional)


| Method | Endpoint                   | Description                          |
|--------|----------------------------|--------------------------------------|
| `GET`  | `/lokacije`                | Returns all project locations (GeoJSON) |
| `POST` | `/lokacije`                | Adds a new location (via form data) |
| `PUT`  | `/lokacije/{broj_foldera}` | Updates a location by folder number |
| `DELETE` | `/lokacije/{broj_foldera}` | Deletes a location by folder number |
| `GET`  | `/lokacije/filter`         | Filters locations by year, project planner, investor, etc. |

> 🔐 All endpoints require a valid `Bearer` token in the `Authorization` header (unless `API_TOKEN` is empty in `app.py`).

---

## 🧭 Running Locally

### Option 1: Manual (recommended for development)

1. Clone the repo:
```bash
git clone https://github.com/mitasd/fastAPI-GIS.git
cd fastAPI-GIS

    Install dependencies:

pip install fastapi uvicorn

    Start the server:

uvicorn app:app --reload

    Open index.html or mapa.html in your browser to interact with the API.

Option 2: Docker (optional)

Build and run with Docker:

docker build -t fastapi-gis .
docker run -p 8000:8000 fastapi-gis

🌐 Frontend Access

    index.html – View, add, edit, and delete projects in a table UI

    mapa.html – Interactive map with ArcGIS basemaps and feature labels

✅ To Do

User authentication (login/register)

Host map and table frontend via FastAPI static routes

    Switch from file-based GeoJSON to PostGIS or MongoDB

👨‍💻 Author

Dimitrije Gajin
📍 Belgrade, Serbia
🔗 GitHub Profile
