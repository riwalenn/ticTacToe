import math

def print_board(board):
    # Affiche le plateau de jeu
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < 2:
            print("---------")

def check_winner(board, player):
    # Vérifie si un joueur a gagné
    for row in board:
        if all([spot == player for spot in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def check_full(board):
    # Vérifie si le plateau est plein (match nul)
    return all([spot != ' ' for row in board for spot in row])

def player_move(board):
    # Demande à l'utilisateur d'entrer son mouvement
    move = -1
    while move not in range(1, 10) or not is_valid_move(board, move):
        move = int(input("Entrez votre mouvement (1-9): "))
    return move

def is_valid_move(board, move):
    # Vérifie si un mouvement est valide (case vide)
    row, col = divmod(move - 1, 3)
    return board[row][col] == ' '

def make_move(board, move, player):
    # Effectue un mouvement sur le plateau
    row, col = divmod(move - 1, 3)
    board[row][col] = player

def undo_move(board, move):
    # Annule un mouvement (utile pour l'algorithme Minimax)
    row, col = divmod(move - 1, 3)
    board[row][col] = ' '

def minimax(board, depth, is_maximizing):
    # Algorithme Minimax pour évaluer les meilleurs mouvements
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if check_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(board):
            make_move(board, move, 'O')
            score = minimax(board, depth + 1, False)
            undo_move(board, move)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves(board):
            make_move(board, move, 'X')
            score = minimax(board, depth + 1, True)
            undo_move(board, move)
            best_score = min(score, best_score)
        return best_score

def ai_move(board):
    # IA choisit le meilleur mouvement en utilisant Minimax
    best_score = -math.inf
    best_move = None
    for move in get_available_moves(board):
        make_move(board, move, 'O')
        score = minimax(board, 0, False)
        undo_move(board, move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def get_available_moves(board):
    # Retourne la liste des mouvements disponibles
    return [i + 1 for i in range(9) if is_valid_move(board, i + 1)]

def main():
    # Fonction principale pour gérer le jeu
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'

    while True:
        print_board(board)

        if current_player == 'X':
            move = player_move(board)
        else:
            move = ai_move(board)
            print(f"L'IA choisit: {move}")

        make_move(board, move, current_player)

        if check_winner(board, current_player):
            print_board(board)
            print(f"Le joueur {current_player} a gagné!")
            break

        if check_full(board):
            print_board(board)
            print("Match nul!")
            break

        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    main()