'''
chess_board.py

Ce module définit la classe ChessBoard, qui encapsule l'état d'une partie d'échecs à partir d'une chaîne FEN. 
Il fournit des méthodes pour afficher le plateau et récupérer les pièces par type.
'''

import chess

class ChessBoard:
    def __init__(self, fen, color, opponent):
        # Initialise le plateau à partir de la FEN
        self.board = chess.Board(fen)

        # Couleur du joueur (white / black)
        self.color = color

        # Nom de l'adversaire
        self.opponent = opponent

    # Affiche le plateau dans la console (debug / test)
    def print_board(self):
        print(self.board)

    # Retourne les cases contenant un type de pièce donné
    def get_pieces_by_type(self, piece_type):
        return [
            sq for sq in chess.SQUARES
            if self.board.piece_at(sq)
            and self.board.piece_at(sq).piece_type == piece_type
        ]