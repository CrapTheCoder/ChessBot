"""
This file will be available to you via import. The starter code file imports
everything accessible already.
"""
from enum import Enum, auto


class PlayerColour(Enum):
    White = auto()
    Black = auto()


class BoardPiece(Enum):
    WhitePawn = auto()
    WhiteKnight = auto()
    WhiteBishop = auto()
    WhiteRook = auto()
    WhiteQueen = auto()
    WhiteKing = auto()
    BlackPawn = auto()
    BlackKnight = auto()
    BlackBishop = auto()
    BlackRook = auto()
    BlackQueen = auto()
    BlackKing = auto()
    EmptySquare = auto()
    Resignation = auto()
    Invalid = auto()


files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

all_squares = [file + rank for file in files for rank in ranks]

PieceCharName = {
    'P': BoardPiece.WhitePawn,
    'N': BoardPiece.WhiteKnight,
    'B': BoardPiece.WhiteBishop,
    'R': BoardPiece.WhiteRook,
    'Q': BoardPiece.WhiteQueen,
    'K': BoardPiece.WhiteKing,
    'p': BoardPiece.BlackPawn,
    'n': BoardPiece.BlackKnight,
    'b': BoardPiece.BlackBishop,
    'r': BoardPiece.BlackRook,
    'q': BoardPiece.BlackQueen,
    'k': BoardPiece.BlackKing,
}

PieceNameChar = {
    BoardPiece.WhitePawn: '♙',
    BoardPiece.WhiteKnight: '♘',
    BoardPiece.WhiteBishop: '♗',
    BoardPiece.WhiteRook: '♖',
    BoardPiece.WhiteQueen: '♕',
    BoardPiece.WhiteKing: '♔',
    BoardPiece.BlackPawn: '♟︎',
    BoardPiece.BlackKnight: '♞',
    BoardPiece.BlackBishop: '♝',
    BoardPiece.BlackRook: '♜',
    BoardPiece.BlackQueen: '♛',
    BoardPiece.BlackKing: '♚',
    BoardPiece.EmptySquare: '－',
}

# This class represents the board state
class BoardState:

    @staticmethod
    def resign():
        states = {}
        for file in files:
            for rank in ranks:
                states[file + rank] = BoardPiece.Resignation
        return BoardState(states)

    @staticmethod
    def invalid():
        states = {}
        for file in files:
            for rank in ranks:
                states[file + rank] = BoardPiece.Invalid
        return BoardState(states)

    @classmethod
    def from_fen(cls, fen):
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

        return cls(result)

    def __str__(self):
        return '\n'.join(''.join(PieceNameChar[self._state[file + rank]] for file in files) for rank in ranks[::-1])

    # Create a new board state with a dictionary mapping positions (like
    # e4, a8, ...) to BoardPiece members. Empty squares can either be
    # specified to be empty, or ommitted entirely.
    def __init__(self, position_states):
        invalidate = False
        resign = False
        if type(position_states) is not dict:
            invalidate = True
        for (position, piece) in position_states.items():
            if type(piece) is not BoardPiece:
                invalidate = True
            if type(position) is not str:
                invalidate = True
            if position not in all_squares:
                invalidate = True
            if piece == BoardPiece.Invalid:
                invalidate = True
            if piece == BoardPiece.Resignation:
                resign = True

        if invalidate:
            for position in all_squares:
                position_states[position] = BoardPiece.Invalid
            self._state = position_states
            return
        if resign:
            for position in all_squares:
                position_states[position] = BoardPiece.Resignation
            self._state = position_states
            return

        for position in all_squares:
            if position not in position_states.keys():
                position_states[position] = BoardPiece.EmptySquare
        self._state = position_states

    # Get a piece at a file and rank
    # Note that files are lowercase alphabet a-h
    # Note that ranks are strings of 1-8
    def piece_at(self, file, rank):
        if file not in files or rank not in ranks:
            return BoardPiece.Invalid
        return self._state[file + rank]


# board_state should be a valid BoardState object
# colour should be PlayerColour.White or PlayerColour.Black
# note that this function has a significant time penalty!
# also note that using 'import chess' in your code is disallowed!
def get_next_states(board_state, colour):
    import chess
    import time

    def get_inbuilt_state(board):
        pos_dict = {}
        for file in files:
            for rank in ranks:
                square = chess.parse_square(file + rank)
                piece = board.piece_at(square)
                if piece == None:
                    pos_dict[file + rank] = BoardPiece.EmptySquare
                else:
                    answer = None
                    if piece.piece_type == chess.PAWN:
                        if piece.color == chess.WHITE:
                            answer = BoardPiece.WhitePawn
                        else:
                            answer = BoardPiece.BlackPawn
                    if piece.piece_type == chess.KNIGHT:
                        if piece.color == chess.WHITE:
                            answer = BoardPiece.WhiteKnight
                        else:
                            answer = BoardPiece.BlackKnight
                    if piece.piece_type == chess.BISHOP:
                        if piece.color == chess.WHITE:
                            answer = BoardPiece.WhiteBishop
                        else:
                            answer = BoardPiece.BlackBishop
                    if piece.piece_type == chess.ROOK:
                        if piece.color == chess.WHITE:
                            answer = BoardPiece.WhiteRook
                        else:
                            answer = BoardPiece.BlackRook
                    if piece.piece_type == chess.QUEEN:
                        if piece.color == chess.WHITE:
                            answer = BoardPiece.WhiteQueen
                        else:
                            answer = BoardPiece.BlackQueen
                    if piece.piece_type == chess.KING:
                        if piece.color == chess.WHITE:
                            answer = BoardPiece.WhiteKing
                        else:
                            answer = BoardPiece.BlackKing
                    pos_dict[file + rank] = answer
        return BoardState(pos_dict)

    def to_fen_piece(piece):
        if piece == BoardPiece.WhitePawn:
            return 'P'
        if piece == BoardPiece.WhiteKnight:
            return 'N'
        if piece == BoardPiece.WhiteBishop:
            return 'B'
        if piece == BoardPiece.WhiteRook:
            return 'R'
        if piece == BoardPiece.WhiteQueen:
            return 'Q'
        if piece == BoardPiece.WhiteKing:
            return 'K'
        if piece == BoardPiece.BlackPawn:
            return 'p'
        if piece == BoardPiece.BlackKnight:
            return 'n'
        if piece == BoardPiece.BlackBishop:
            return 'b'
        if piece == BoardPiece.BlackRook:
            return 'r'
        if piece == BoardPiece.BlackQueen:
            return 'q'
        if piece == BoardPiece.BlackKing:
            return 'k'
        return 1

    def to_fen(board_pos):
        tr = []
        for rank in '87654321':
            here = []
            for file in 'abcdefgh':
                pieceAt = to_fen_piece(board_pos.piece_at(file, rank))
                if pieceAt == 1 and len(here) > 0 and (type(here[-1]) == type(5)):
                    here[-1] += 1
                else:
                    here.append(pieceAt)
            here = "".join([str(x) for x in here])
            tr.append(here)
        return "/".join(tr)

    state_fen = to_fen(board_state)
    move_fen = "w"
    if colour == PlayerColour.Black:
        move_fen = "b"
    castling_fen = "-"
    passant_fen = "-"
    halfmove_fen = "0"
    fullmove_fen = "1"
    fen_string = " ".join([state_fen, move_fen, castling_fen, passant_fen, halfmove_fen, fullmove_fen])
    b = chess.Board(fen_string)
    x = list(b.legal_moves)
    if len(x) == 0:
        raise RuntimeError()
    res = []
    for move in x:
        c = b.copy()
        c.push(move)
        res.append(get_inbuilt_state(c))
    return res
