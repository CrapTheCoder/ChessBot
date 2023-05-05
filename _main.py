"""
Write your code in this file to participate in the Chess Bot challenge!
Username: <enter your username here>
"""

from enum import Enum
from _ContestUtils import PlayerColour, BoardState, BoardPiece
from _ContestUtils import files, ranks, all_squares

WhitePieces = [BoardPiece.WhitePawn, BoardPiece.WhiteKnight,
               BoardPiece.WhiteBishop, BoardPiece.WhiteRook,
               BoardPiece.WhiteQueen, BoardPiece.WhiteKing]

BlackPieces = [BoardPiece.BlackPawn, BoardPiece.BlackKnight,
               BoardPiece.BlackBishop, BoardPiece.BlackRook,
               BoardPiece.BlackQueen, BoardPiece.BlackKing]

BoardPiece = Enum('BoardPiece', [
    'WhitePawn',
    'WhiteKnight',
    'WhiteBishop',
    'WhiteRook',
    'WhiteQueen',
    'WhiteKing',
    'BlackPawn',
    'BlackKnight',
    'BlackBishop',
    'BlackRook',
    'BlackQueen',
    'BlackKing',
    'EmptySquare',
    'Resignation',
    'Invalid'
])

class Engine:
    """
    This function will be called at the start of each game. You should use this to
    set up any key data structures you will need for the game. You can also use
    this function to precompute any data you will use during the game.
    Parameters:
      - colour:             PlayerColour.White or PlayerColour.Black, representing the
                            colour your bot will be playing for this game.
      - time_per_move:      Float representing the number of seconds you have per move
                            for each move during this game.
    Return:
      - Nothing. You can choose to return something if you wish, but nothing will be
        done with this information.
    Constraints:
      - This function must complete running in at most 10 seconds, or the game will
        automatically be considered forfeited.
    """
    def __init__(self, colour, time_per_move):
        self.colour = colour
        self.self_pieces = WhitePieces if colour == PlayerColour.White else BlackPieces
        self.other_pieces = BlackPieces if colour == PlayerColour.White else WhitePieces
        self.queenside_castle = self.kingside_castle = True

    @staticmethod
    def from_fen(fen):
        board = fen.split(" ")[0]
        board_ranks = board.split("/")
        result = {}

        for rank_index, rank in enumerate(board_ranks):
            file_index = 0
            for char in rank:
                if char.isdigit():
                    file_index += int(char)
                else:
                    result[files[file_index] + ranks[7 - rank_index]] = PieceCharName[char]
                    file_index += 1

        return BoardState(result)

    """
    This function will be called every time your opponent makes a move (or, if you're
    playing white, also at the start). In other words, this function will be called
    whenever it's your turn to make a move. You can use this function to calculate 
    your next move and then send it.
    Parameters:
      - board_state:        BoardState object representing the current state of the
                            board. 
    Return:
      - A new board state after your move is made, represented using the BoardState 
        object. 
    Constraints:
      - If the new board state you return is not a valid board state resulting from
        a valid move you can make, then you will immediately lose the game.
      - If this function takes more than time_per_move seconds to run, you will
        immediately lose the game.
      - You can return BoardState.resign() if you'd like to resign.
    """

    def get_legal_moves(self, board):
        def is_valid(rank_index, file_index):
            return 0 <= rank_index <= 7 and 0 <= file_index <= 7

        all_legal_moves = []
        for rank_index, rank in enumerate(board):
            for file_index, piece in enumerate(rank):
                if piece not in self.our_pieces:
                    continue

                all_legal_moves.extend(get_knight_moves(file_index, rank_index))

    def get_move(self, board_state: BoardState):
        board = [[board_state.piece_at(file, rank) for file in files] for rank in ranks]
        print(*board, sep='\n')


if __name__ == '__main__':
    e = Engine(PlayerColour.White, 5)
    b = BoardState.from_fen('rnbqk1nr/pppp1ppp/8/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R')
    print(e.get_move(b))
