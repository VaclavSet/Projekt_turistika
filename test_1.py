import folium # knihovna pro tvorbu interaktivních map (Leaflet mapy v HTML)
import gpxpy # knihovna pro načítání a parsování GPX souborů (GPS trasy)
import os # práce se souborovým systémem (složky, soubory)

# Vytvoření základní mapy
# location = [zeměpisná šířka, zeměpisná délka]
# zoom_start = počáteční přiblížení mapy
mapa = folium.Map(location=[49.14, 16.88], zoom_start=12)

# Slovník, který mapuje typ aktivity na styl vykreslení čáry
STYLE_MAP = {
    "hiking": {"color": "red", "weight": 5}, # pěší trasy budou červené
    "biking": {"color": "green", "weight": 5}, # cyklotrasy zelené
    "plan": {"color": "black", "weight": 5}, # plánované trasy černé
}

# Funkce, která získá typ aktivity z názvu složky
# Např. "vylet_hiking" → "hiking"
def get_activity_type(folder_name):
    return folder_name.split("_")[-1].lower()

# Cesta ke složce, kde jsou podsložky s GPX soubory
slozka = "D:/PYTHON/GIT/Repositories/Projekt_turistika"

# Procházení všech položek ve složce
for folder in os.listdir(slozka):
    folder_path = os.path.join(slozka, folder)

    # Pokud to není složka (např. soubor), přeskočíme
    if not os.path.isdir(folder_path):
        continue

    # Získání typu aktivity podle názvu složky
    activity_type = get_activity_type(folder)

    # Získání stylu podle typu aktivity
    # Pokud typ není ve STYLE_MAP, použije se default (šedá čára)
    style = STYLE_MAP.get(activity_type, {"color": "gray", "weight": 3})

    # Procházení souborů v dané složce
    for file in os.listdir(folder_path):
        if file.endswith(".gpx"): # Zajímá nás pouze soubory s příponou .gpx
            file_path = os.path.join(folder_path, file)

            print(activity_type, file, style) # Výpis do konzole pro kontrolu

            # Otevření a načtení GPX souboru
            with open(file_path, "r", encoding="utf-8") as gpx_file:
                gpx = gpxpy.parse(gpx_file)

            points = [] # seznam bodů (souřadnic), které se vykreslí

            # ✅ TRACKS (nejběžnější forma záznamu trasy)
            # GPX může obsahovat více tracků → segmentů → bodů
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        points.append((point.latitude, point.longitude))

            # ✅ Routes (fallback)
            for route in gpx.routes:
                for point in route.points:
                    points.append((point.latitude, point.longitude)) # ukládáme dvojici (lat, lon)

            # Pokud máme nějaké body, vykreslíme čáru do mapy
            if points:
                folium.PolyLine(
                    points,
                    color=style["color"],
                    weight=style["weight"],
                    tooltip=file  # název trasy při najetí myší
                ).add_to(mapa)

# Uložení výsledné mapy do HTML souboru
mapa.save("D:/PYTHON/GIT/Repositories/Projekt_turistika/mapa.html")

