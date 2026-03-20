import folium
import gpxpy
import os

# vytvoření mapy
mapa = folium.Map(location=[49.14, 16.88], zoom_start=12)

# složka s GPX
slozka = "D:/PYTHON/GIT/Repositories/Projekt_turistika/gpx_hiking"

# projdi všechny soubory ve složce
for soubor in os.listdir(slozka):

    if soubor.endswith(".gpx"):

        cesta = os.path.join(slozka, soubor)

        with open(cesta, "r", encoding="utf-8") as gpx_file:
            gpx = gpxpy.parse(gpx_file)

        body = []

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    body.append([point.latitude, point.longitude])

        # vykreslení trasy
        folium.PolyLine(body, color="blue", weight=4).add_to(mapa)

# uložení mapy
mapa.save("mapa.html")