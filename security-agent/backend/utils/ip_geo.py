import requests

cache = {}

def get_ip_info(ip):
    if ip in cache:
        return cache[ip]

    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        data = response.json()

        if data["status"] == "success":
            info = {
                "country": data.get("country", "Unknown"),
                "city": data.get("city", "Unknown"),
                "lat": data.get("lat"),
                "lon": data.get("lon")
            }
        else:
            info = {"country": "Unknown", "city": "Unknown", "lat": None, "lon": None}

    except:
        info = {"country": "Unknown", "city": "Unknown", "lat": None, "lon": None}

    cache[ip] = info
    return info