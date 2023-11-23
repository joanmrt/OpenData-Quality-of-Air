import requests

from fastapi import FastAPI
from fastapi.responses import HTMLResponse  # Necesario para enviar html

from fastapi import HTTPException

app = FastAPI()
urlJson = "https://services1.arcgis.com/nCKYwcSONQTkPA4K/arcgis/rest/services/CalidadAire/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"


@app.get("/")
async def root():
    html = open("index.html", "r", encoding="utf-8").read()
    return HTMLResponse(content=html, status_code=200)

# Pide la peticion del Json y lo devuelve
def get_json():
    try:
        response = requests.get(urlJson)
        response.raise_for_status()
        json = response.json()

        return json
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error en la petición de datos del Json "+e)

# Muestra una tabla de todos los datos del Json
@app.get("/tabla")
async def get_table():
    json = get_json()

    html = """
    <!DOCTYPE html>
    <html>
        <style>
            table, th, td {border:1px solid black;
            border-collapse: collapse}
        </style>
        <head>
            <title>Tabla Calidad de aire</title>
        </head>
        <body>
            <table style="width: 100%">
                <tr>
                    <th>ID</th>
                    <th>EoI Code</th>
                    <th>Station Name</th>
                    <th>Longitude</th>
                    <th>Latitude</th>
                    <th>Altitude</th>
                    <th>Station Type</th>
                    <th>Station Area</th>
                    <th>Quality of Air</th>
                </tr>
        
    """
    for i in range(len(json["features"])):

        first_feature = json["features"][i]
        properties = first_feature.get("properties", {})
        html += f"""
                        <tr>
                            <td>{properties.get("OBJECTID", "N/A")}</td>
                            <td>{properties.get("EoICode", "N/A")}</td>
                            <td>{properties.get("StationNam", "N/A")}</td>
                            <td>{properties.get("Longitude", "N/A")}</td>
                            <td>{properties.get("Latitude", "N/A")}</td>
                            <td>{properties.get("Altitude", "N/A")}</td>
                            <td>{properties.get("StationTyp", "N/A")}</td>
                            <td>{properties.get("StationAre", "N/A")}</td>
                            <td>{properties.get("avg15", "N/A")}</td>
                        </tr>
            """
    html += f"""
            </table>
        </body>
    </html>
    """
    
    
    return HTMLResponse(content=html, status_code=200)

# Devuelve la media de la calidad del aire del pais pasado por parametro
@app.get("/porcentaje/{pais}")
async def getMedia(pais):
    json = get_json()
    counter = 0
    sum_air_quality = 0
    

    for i in range(len(json["features"])):
        first_feature = json["features"][i]
        properties = first_feature.get("properties", {})

        if pais in properties.get("EoICode", "N/A"):
            counter += 1
            sum_air_quality += properties.get("avg15", "N/A")

    print(counter)
    print(sum_air_quality)
    avg_quality = sum_air_quality/counter

    return avg_quality

# Devuelve la media de la calidad del aire del areaa pasada por parametro
@app.get("/areas/{area_type}")
async def getMediaAreas(area_type):
    json = get_json()
    counter = 0
    sum_air_quality = 0
    

    for i in range(len(json["features"])):
        first_feature = json["features"][i]
        properties = first_feature.get("properties", {})

        if area_type in properties.get("StationAre", "N/A"):
            counter += 1
            sum_air_quality += properties.get("avg15", "N/A")

    print(counter)
    print(sum_air_quality)
    avg_quality = sum_air_quality/counter

    return avg_quality