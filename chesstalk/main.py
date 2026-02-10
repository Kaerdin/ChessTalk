'''
main.py

Ce module est le point d'entrée de l'application ChessTalk. 
Il initialise le GameManager pour récupérer les parties en cours, puis utilise GameUI pour afficher graphiquement le plateau d'une partie sélectionnée.
'''

from game_manager import GameManager
from game_ui import GameUI


def main():
    # Initialise le gestionnaire et récupère les parties en cours
    manager = GameManager()
    manager.fetch_current_games()

    # Affichage console des plateaux (debug)
    manager.print_boards()

    # Si aucune partie n'est en cours, on arrête le programme
    if not manager.games:
        print("Aucune partie en cours trouvée.")
        return

    # Affichage
    ui = GameUI(manager.games, start_index=0)
    ui.run()


if __name__ == "__main__":
    main()
