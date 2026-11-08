# Aplikacja do sprawdzania pogody

Prosta aplikacja GUI w Pythonie do sprawdzania pogody po wpisaniu miejscowości.

## Funkcje
- wpisanie nazwy miejscowości,
- pobieranie danych z darmowego API Open-Meteo,
- bez konta i bez klucza API,
- wyświetlanie temperatury, wilgotności, wiatru oraz prognozy na kilka dni.

## Wymagania
- Python 3.10+
- biblioteka `requests`

## Uruchomienie
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Źródło danych
- Open-Meteo: https://open-meteo.com/
