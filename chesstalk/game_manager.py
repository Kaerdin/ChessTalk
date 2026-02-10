'''
game_manager.py

Ce module définit la classe GameManager, qui gère les interactions avec l'API de Lichess 
pour récupérer les parties en cours d'un utilisateur.
'''

import json
import requests
from chess_board import ChessBoard


class GameManager:
    def __init__(self, token_file="token.json"):
        # Chargement du token API Lichess depuis le fichier JSON
        with open(token_file, "r") as f:
            data = json.load(f)

        self.token = data["lichess_token"]

        # En-têtes d'authentification pour les requêtes API
        self.headers = {"Authorization": f"Bearer {self.token}"}

        # Liste des parties actuellement en cours (objets ChessBoard)
        self.games = []

    # Récupère les parties en cours de l'utilisateur connecté
    def fetch_current_games(self):
        response = requests.get(
            "https://lichess.org/api/account/playing",
            headers=self.headers
        )

        # Vérifie que la requête a réussi (code HTTP 200 = OK)  
        if response.status_code == 200:
            data = response.json()

            # Création d'un ChessBoard par partie en cours
            self.games = [
                ChessBoard(
                    game['fen'],
                    game['color'],
                    game['opponent']['username']
                )
                for game in data['nowPlaying']
            ]
        else:
            # Affiche l'erreur retournée par l'API
            print("Erreur API :", response.status_code, response.text)

    # Affichage console des plateaux (debug / test)
    def print_boards(self):
        for game in self.games:
            print(f"Partie contre {game.opponent}, couleur: {game.color}")
            game.print_board()
            print()