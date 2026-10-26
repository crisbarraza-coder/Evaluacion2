import requests

def geocodificar(ciudad):
    url = f"https://nominatim.openstreetmap.org/search?q={ciudad}&format=json&limit=1"
    headers = {'User-Agent': 'DevNetLab/1.0'}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        data = r.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            nombre = data[0]['display_name'].split(',')[0]
            return lat, lon, nombre
    except Exception:
        pass
    return None, None, None

def obtener_ruta():
    print("=========================================")
    print(" SISTEMA DE GEOLOCALIZACIÓN Y RUTAS ")
    print("=========================================")
    
    origen = input("Origen: ")
    if origen.lower() in ["s", "q", "quit", "salir"]:
        return False

    destino = input("Destino: ")
    if destino.lower() in ["s", "q", "quit", "salir"]:
        return False

    lat1, lon1, nom1 = geocodificar(origen)
    lat2, lon2, nom2 = geocodificar(destino)

    if not lat1 or not lat2:
        print("\n[!] No se pudieron obtener las coordenadas de origen o destino. Intenta de nuevo.\n")
        return True

    url_route = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false&steps=true"
    try:
        r = requests.get(url_route, timeout=5)
        res = r.json()
        if res.get("code") == "Ok":
            route = res["routes"][0]
            distancia_km = route["distance"] / 1000
            tiempo_min = route["duration"] / 60
            
            print("\n-----------------------------------------")
            print(f"Ruta calculada de: {nom1} a {nom2}")
            print(f"Distancia total : {distancia_km:.2f} km")
            print(f"Tiempo estimado : {tiempo_min:.2f} minutos")
            print("-----------------------------------------")
            print("Instrucciones paso a paso:")
            
            for step in route["legs"][0]["steps"]:
                text = step.get("name")
                if not text:
                    text = "Continuar por la vía principal"
                dist_step = step["distance"] / 1000
                print(f"- {text} ({dist_step:.2f} km)")
            print("-----------------------------------------\n")
        else:
            print("\n[!] No se pudo calcular la ruta.\n")
    except Exception as e:
        print(f"\n[!] Error en el servicio de rutas: {e}\n")
        
    return True

if __name__ == "__main__":
    while True:
        cont = obtener_ruta()
        if not cont:
            print("Saliendo del sistema de geolocalización...")
            break
