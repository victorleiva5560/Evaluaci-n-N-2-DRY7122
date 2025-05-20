import requests

API_KEY = 'IvFeyUOiM89lR4HuI9GTugdQpT0GLBkX'

def obtener_datos(origen, destino):
    url = "https://www.mapquestapi.com/directions/v2/route"
    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}
    data = {
        "locations": [origen, destino],
        "options": {
            "unit": "k",  # kilómetros
            "routeType": "fastest",
            "vehicleFuelEfficiency": 12,
            "fuelType": "GASOLINE",
            "drivingStyle": 1,
            "vehicleType": "auto"
        }
    }

    response = requests.post(url, headers=headers, params=params, json=data)
    try:
        return response.json()
    except Exception as e:
        print("❌ Error al convertir JSON:", e)
        return None

def traducir_narrativa(texto):
    traducciones = {
        "Head toward": "Dirígete hacia",
        "Turn right": "Gira a la derecha en",
        "Turn left": "Gira a la izquierda en",
        "Continue on": "Continúa por",
        "Go for": "por",
        "Take the exit toward": "Toma la salida hacia",
        "Take the": "Toma la",
        "Keep right": "Mantente a la derecha",
        "Arrive at": "Has llegado a",
        "Exit": "Salida",
        "onto": "en",
        "from roundabout": "desde la rotonda",
        "1st exit": "primera salida",
        "toward": "en dirección a"
    }

    for en, es in traducciones.items():
        texto = texto.replace(en, es)
    return texto

def mostrar_info_viaje(datos):
    ruta = datos["route"]
    duracion = ruta.get("formattedTime", "No disponible")
    distancia = ruta.get("distance", 0)  # en km
    print(f"\n🧭 Duración estimada: {duracion}")
    print(f"📏 Distancia: {distancia} km")

    # Cálculo de combustible: usa el valor real si viene, si no, calcula manualmente
    if 'fuelUsed' in ruta and ruta['fuelUsed'] is not None:
        galones = ruta['fuelUsed']
        litros = round(galones * 3.78541, 2)
        print(f"⛽ Combustible estimado (API): {litros} litros")
    else:
        litros_estimados = round(float(distancia) / 12, 2)  # 12 km/L
        print(f"⛽ Combustible estimado (calculado): {litros_estimados} litros")

    print("\n📌 Instrucciones del viaje:")
    for paso in ruta["legs"][0]["maneuvers"]:
        texto_traducido = traducir_narrativa(paso['narrative'])
        print(f"- {texto_traducido}")

def main():
    print("🌍 Evaluación DRY7122 - API Pública MapQuest\n")
    while True:
        origen = input("Ciudad de origen (o 'q' para salir): ")
        if origen.lower() == 'q':
            print("👋 Saliendo del programa.")
            break

        destino = input("Ciudad de destino (o 'q' para salir): ")
        if destino.lower() == 'q':
            print("👋 Saliendo del programa.")
            break

        datos = obtener_datos(origen, destino)
        if datos and datos.get("info", {}).get("statuscode") == 0:
            mostrar_info_viaje(datos)
        else:
            print("❌ No se pudo obtener una ruta válida. Verifica las ciudades o la conexión.")

if __name__ == "__main__":
    main()
