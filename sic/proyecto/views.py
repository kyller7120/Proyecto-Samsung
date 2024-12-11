from django.shortcuts import render
import requests
import json
from django.http import HttpResponse

class TeamData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TeamData, cls).__new__(cls)
            cls._instance.team_id = None
            cls._instance.players_dict = {}
        return cls._instance

    @property
    def id(self):
        return self.team_id

    @id.setter
    def id(self, value):
        self.team_id = value

# Vista inicial
def index(request):
    return render(request, 'index.html')

# busqueda de equipo
def search_team(request):
    team_name = ""
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
    
    team_data = TeamData()

    url = "https://transfermarket.p.rapidapi.com/search"

    headers = {
        'x-rapidapi-key': "5b40e5fb69mshf21006f6bbefda5p100797jsn9589b7089146",
        'x-rapidapi-host': "transfermarket.p.rapidapi.com"
    }

    querystring = {"query":team_name, "domain":"de"}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        json_data = response.json()

        if 'clubs' in json_data and len(json_data['clubs']) > 0:
            team_data.team_id = json_data['clubs'][0]['id']
        else:
            print("No se encontraron equipos.")
            team_data = {}

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los equipos: {e}")
        team_data = {}
    
    return render(request, 'index.html', {'team_data': team_data, 'team_name': team_name})

# vista de formulario para la plantilla del equipo
def plantilla_team(request, nombre_equipo, id_equipo):
    return render(request, 'plantilla_team.html', {'team': nombre_equipo, 'id_team': id_equipo})

#ejecucion de la busqueda de plantilla del equipo
def jugadores(request, nombre_equipo, id_equipo):
    season_id = 0
    if request.method == 'POST':
        season_id = request.POST.get('season_year')
        
        if not season_id:
            return HttpResponse('El año de la temporada es obligatorio.', status=400)

    team_data = TeamData()

    team_data.team_id = id_equipo

    url = "https://transfermarket.p.rapidapi.com/clubs/get-squad"
    
    querystring = {
        "id": str(team_data.team_id),
        "saison_id": season_id,
        "domain": "de"
    }
    
    headers = {
        "x-rapidapi-key": "5b40e5fb69mshf21006f6bbefda5p100797jsn9589b7089146",
        "x-rapidapi-host": "transfermarket.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        
        team_data.players_dict.clear()
        
        if 'squad' in data:
            players_with_id = {} 
            for idx, player in enumerate(data['squad']):
                if 'name' in player and 'id' in player:
                    simulated_id = idx + 1
                    players_with_id[simulated_id] = {
                        'name': player['name'],
                        'player_id': player['id']
                    }
            
            return render(request, 'plantilla_team.html', {
                'nombre_equipo': nombre_equipo,
                'players': players_with_id,
                'season_year': season_id,
                'id_team': id_equipo,
                'team': nombre_equipo,
            })

        else:
            return HttpResponse('No se encontraron jugadores para este equipo y temporada.', status=404)
    
    except requests.exceptions.RequestException as e:
        return HttpResponse(f'Error al obtener los jugadores: {str(e)}', status=500)