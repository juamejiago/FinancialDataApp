import requests

url = "https://juamejiago.pythonanywhere.com/update_tag"

# Realizar la solicitud y obtener la respuesta
response = requests.get(url)

print(response)