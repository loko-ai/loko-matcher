import requests

resp = requests.get("http://localhost:8080/ui/")

resp.raise_for_status()
