'''
game_ui.py

Ce module définit la classe GameUI, qui utilise Pygame pour afficher graphiquement un plateau d'échecs à partir d'un objet ChessBoard.
'''

import pygame
import chess
import os

class GameUI:
    def __init__(self, games, start_index=0):
        """
        games: liste d'objets ChessBoard (manager.games)
        start_index: index initial de la partie à afficher
        """
        if not games:
            raise ValueError("La liste games est vide.")

        pygame.init()
        pygame.font.init()

        self.games = games
        self.current = max(0, min(start_index, len(games)-1))

        # dimensions
        self.square_size = 100 # 800 * 800 pour le plateau
        self.board_px = 8 * self.square_size
        self.menu_width = 600 # Taille du panneau d'information à droite
        self.screen = pygame.display.set_mode((self.board_px + self.menu_width, self.board_px))
        pygame.display.set_caption(f"ChessTalk")

        # tailles des polices
        self.font_title = pygame.font.SysFont(None, 28)
        self.font_text = pygame.font.SysFont(None, 20)
        self.font_coord = pygame.font.SysFont(None, 40)

        # taille des pièces par rapport à la case
        self.piece_size = int(self.square_size * 0.80)

        self.load_pieces()

        # rectangles pour boutons (dans le menu)
        self.btn_prev_rect = pygame.Rect(self.board_px + self.menu_width-240, self.board_px - 50, 100, 36)
        self.btn_next_rect = pygame.Rect(self.board_px + self.menu_width-120, self.board_px - 50, 100, 36)

        # couleurs
        self.menu_bg = pygame.Color(40, 40, 40)
        self.menu_fg = pygame.Color(230, 230, 230)
        self.board_light = pygame.Color(235, 209, 166)
        self.board_dark = pygame.Color(165, 117, 81)
        self.border_color = pygame.Color(10, 10, 10)

        # couleurs pour labels de coordonnées (contraste)
        # clair sur cases foncées, marron foncé sur cases claires
        self.coord_light = pygame.Color(245, 245, 220)  # très clair (pour square dark)
        self.coord_dark_brown = pygame.Color(92, 54, 17)  # marron foncé (pour square light)

        

    # Charge les images des pièces depuis assets et les prépare pour l'affichage
    def load_pieces(self):
        # Dictionnaire { 'p': image pion noir, 'K': image roi blanc, ... }
        self.piece_images = {}

        # Chemin vers le dossier assets/
        base_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(base_dir, "assets")

        # Symboles python-chess des pièces (noir = minuscule, blanc = majuscule)
        pieces = ['p', 'r', 'n', 'b', 'q', 'k', 'P', 'R', 'N', 'B', 'Q', 'K']

        for p in pieces:
            # Détermine le sous-dossier selon la couleur
            color_dir = "white" if p.isupper() else "black"
            filename = f"{p}.png"
            path = os.path.join(assets_dir, color_dir, filename)

            # Si l'image n'existe pas, on stocke None pour éviter les erreurs plus tard en cas de problème
            if not os.path.isfile(path):
                self.piece_images[p] = None
                continue

            # Chargement et redimensionnement de l'image
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(
                img,
                (self.piece_size, self.piece_size)
            )

            # Stocke l'image prête à être affichée
            self.piece_images[p] = img

    # Détermine l'orientation du plateau par rapport à la couleur du joueur (si on joue blanc ou noir)
    def _compute_orientation(self, board_obj):
        """
        True => blancs en bas (vue depuis les blancs)
        False => noirs en bas (vue depuis les noirs)
        """
        player_color = getattr(board_obj, "color", None)
        if isinstance(player_color, str):
            return player_color.lower() == "white"
        return True

    # Affiche le plateau d'échecs avec les pièces, les cases, et les coordonnées
    def draw_board_area(self, board_obj):
        board = board_obj.board
        white_bottom = self._compute_orientation(board_obj)

        files = ['a','b','c','d','e','f','g','h']
        ranks = ['1','2','3','4','5','6','7','8']

        # dessiner cases et coordonées
        for rank_index in range(8):  # affichage de haut (0) à bas (7)
            for file_index in range(8):
                # mapping selon orientation pour déterminer quel carré on affiche
                if white_bottom:
                    file = file_index
                    rank = 7 - rank_index
                else:
                    file = 7 - file_index
                    rank = rank_index

                rect = pygame.Rect(file_index*self.square_size, rank_index*self.square_size, self.square_size, self.square_size)
                is_dark_square = ((file + rank) % 2) != 0
                color = self.board_dark if is_dark_square else self.board_light
                pygame.draw.rect(self.screen, color, rect)

                # --- LABELS ---
                # Lettres (a-h) : toujours sur la 8 cases du bas, en bas-gauche, miroir si flip
                show_file_label = (rank_index == 7)
                if show_file_label:
                    if white_bottom:
                        file_label = files[file]           # left->right a..h
                    else:
                        file_label = files[7 - file_index] # mirrored when black bottom
                    # couleur contrastée
                    coord_color = self.coord_light if is_dark_square else self.coord_dark_brown
                    surf = self.font_coord.render(file_label, True, coord_color)
                    x = rect.x + 4
                    y = rect.y + self.square_size - surf.get_height() - 4
                    self.screen.blit(surf, (x, y))

                # Chiffres (1-8) : toujours sur la colonne de droite, en haut-droit, s'inversent quand on flip
                show_rank_label = (file_index == 7)
                if show_rank_label:
                    if white_bottom:
                        # top->bottom on affiche 8..1 => ranks[7 - rank_index]
                        rank_label = ranks[7 - rank_index]
                    else:
                        # when flipped we invert the numbers: top->bottom 1..8 => ranks[rank_index]
                        rank_label = ranks[rank_index]
                    coord_color = self.coord_light if is_dark_square else self.coord_dark_brown
                    surf = self.font_coord.render(rank_label, True, coord_color)
                    x = rect.x + self.square_size - surf.get_width() - 4
                    y = rect.y + 4  # en haut
                    self.screen.blit(surf, (x, y))


        # Dessinner les pièces
        # On parcourt toutes les cases de l'échiquier (0 à 63 en notation python-chess)
        for sq in range(64):

            # Récupère la pièce présente sur la case `sq` (None si la case est vide)
            piece = board.piece_at(sq)
            if not piece:
                continue  # si pas de pièce, on passe directement à la case suivante

            # file = colonne (a=0 ... h=7)
            # rank = rangée (1=0 ... 8=7)
            sq_file = chess.square_file(sq)
            sq_rank = chess.square_rank(sq)

            # Conversion des coordonnées logiques en coordonnées d'affichage écran
            # selon l'orientation du plateau (blancs ou noirs en bas)
            if white_bottom:
                file_disp = sq_file
                rank_disp = 7 - sq_rank  # inversion verticale (pygame y=0 en haut)
            else:
                file_disp = 7 - sq_file  # inversion horizontale
                rank_disp = sq_rank

            # Récupère l'image correspondant à la pièce (ex: 'P', 'k', etc.)
            img = self.piece_images.get(piece.symbol())

            if img:
                # Décalage pour centrer la pièce dans la case
                offset = (self.square_size - self.piece_size) // 2

                # Calcul de la position pixel exacte de la pièce
                x = file_disp * self.square_size + offset
                y = rank_disp * self.square_size + offset

                # Dessine la pièce
                self.screen.blit(img, (x, y))

            else:
                # Fallback visuel si l'image n'existe pas
                # (évite un crash et permet de voir qu'une pièce est là)
                cx = file_disp * self.square_size + self.square_size // 2
                cy = rank_disp * self.square_size + self.square_size // 2
                pygame.draw.circle(
                    self.screen,
                    pygame.Color(0, 0, 0),
                    (cx, cy),
                    self.square_size // 4
                )

    def draw_menu(self, board_obj, idx):
        # --- Fond du menu ---
        menu_rect = pygame.Rect(self.board_px, 0, self.menu_width, self.board_px)
        pygame.draw.rect(self.screen, self.menu_bg, menu_rect)

        # --- Titre du panneau ---
        title_surf = self.font_title.render("Informations partie", True, self.menu_fg)
        self.screen.blit(title_surf, (self.board_px + 16, 16))

        # --- Numéro de la partie ---
        idx_text = f"Numéro partie en cours {idx+1} / {len(self.games)}"
        idx_surf = self.font_text.render(idx_text, True, self.menu_fg)
        self.screen.blit(idx_surf, (self.board_px + 16, 52))

        # --- Nom de l’adversaire ---
        opp_text = f"Adversaire: {board_obj.opponent}"
        opp_surf = self.font_text.render(opp_text, True, self.menu_fg)
        self.screen.blit(opp_surf, (self.board_px + 16, 80))

        # --- Trait (qui doit jouer) ---
        turn = board_obj.board.turn
        turn_text = "Trait: Blanc" if turn else "Trait: Noir"
        turn_surf = self.font_text.render(turn_text, True, self.menu_fg)
        self.screen.blit(turn_surf, (self.board_px + 16, 110))

        # --- Affichage du FEN  ---
        fen = board_obj.board.fen()
        fen_surf = self.font_text.render("FEN: " + fen, True, self.menu_fg)
        self.screen.blit(fen_surf, (self.board_px + 16, 140))

        # --- Boutons Précédent / Suivant ---
        pygame.draw.rect(self.screen, pygame.Color(80,80,80), self.btn_prev_rect, border_radius=6)
        pygame.draw.rect(self.screen, pygame.Color(80,80,80), self.btn_next_rect, border_radius=6)

        prev_label = self.font_text.render("<- Précédent", True, self.menu_fg)
        next_label = self.font_text.render("Suivant ->", True, self.menu_fg)
        prev_x = self.btn_prev_rect.x + (self.btn_prev_rect.w - prev_label.get_width())//2
        prev_y = self.btn_prev_rect.y + (self.btn_prev_rect.h - prev_label.get_height())//2
        next_x = self.btn_next_rect.x + (self.btn_next_rect.w - next_label.get_width())//2
        next_y = self.btn_next_rect.y + (self.btn_next_rect.h - next_label.get_height())//2
        self.screen.blit(prev_label, (prev_x, prev_y))
        self.screen.blit(next_label, (next_x, next_y))

    # Titre fenêtre
    def set_window_title(self, board_obj):
        pygame.display.set_caption(f"ChessTalk - vs {board_obj.opponent} — {'Blanc' if board_obj.board.turn else 'Noir'} trait")

    # Boucle graphique principale : gestion des événements et rendu
    def run(self):
        # Horloge pour limiter le nombre d'images par seconde
        clock = pygame.time.Clock()
        running = True

        # --- Boucle principale de l'application ---
        while running:
            # Limite la boucle à 30 FPS
            clock.tick(30)

            # --- Gestion des événements (clavier, souris, fermeture) ---
            for event in pygame.event.get():
                # Fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    running = False

                # Navigation clavier entre les parties
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.current = (self.current + 1) % len(self.games)
                    elif event.key == pygame.K_LEFT:
                        self.current = (self.current - 1) % len(self.games)

                # Navigation souris via les boutons du menu
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if self.btn_prev_rect.collidepoint(mx, my):
                        self.current = (self.current - 1) % len(self.games)
                    elif self.btn_next_rect.collidepoint(mx, my):
                        self.current = (self.current + 1) % len(self.games)

            # --- Rendu graphique ---
            self.screen.fill((120, 120, 120))  # fond global
            board_obj = self.games[self.current]
            self.draw_board_area(board_obj)    # plateau d'échecs
            self.draw_menu(board_obj, self.current)  # panneau d'information
            self.set_window_title(board_obj)   # titre de la fenêtre

            # Mise à jour de l'affichage
            pygame.display.flip()

        pygame.quit()
