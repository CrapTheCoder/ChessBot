"""
Write your code in this file to participate in the Chess Bot challenge!

Username: crap_the_coder
"""
import collections
from time import time
from ContestUtils import PlayerColour, BoardState, BoardPiece
from ContestUtils import files, ranks
from random import randint

STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

INF = 1000000

WhitePawn = 'wp'
WhiteRook = 'wr'
WhiteKnight = 'wn'
WhiteBishop = 'wb'
WhiteQueen = 'wq'
WhiteKing = 'wk'
BlackPawn = 'bp'
BlackRook = 'br'
BlackKnight = 'bn'
BlackBishop = 'bb'
BlackQueen = 'bq'
BlackKing = 'bk'
EmptySquare = '..'
Invalid = 'xx'

PROMOTION = 'P'
CASTLING = 'C'
PAWN_DOUBLE = 'D'
NORMAL = 'N'

PieceToString = {
    BoardPiece.WhitePawn: WhitePawn,
    BoardPiece.WhiteRook: WhiteRook,
    BoardPiece.WhiteKnight: WhiteKnight,
    BoardPiece.WhiteBishop: WhiteBishop,
    BoardPiece.WhiteQueen: WhiteQueen,
    BoardPiece.WhiteKing: WhiteKing,
    BoardPiece.BlackPawn: BlackPawn,
    BoardPiece.BlackRook: BlackRook,
    BoardPiece.BlackKnight: BlackKnight,
    BoardPiece.BlackBishop: BlackBishop,
    BoardPiece.BlackQueen: BlackQueen,
    BoardPiece.BlackKing: BlackKing,
    BoardPiece.EmptySquare: EmptySquare
}

PieceToNumber = {
    WhitePawn: 0,
    WhiteRook: 1,
    WhiteKnight: 2,
    WhiteBishop: 3,
    WhiteQueen: 4,
    WhiteKing: 5,
    BlackPawn: 6,
    BlackRook: 7,
    BlackKnight: 8,
    BlackBishop: 9,
    BlackQueen: 10,
    BlackKing: 11,
    EmptySquare: 12,
}

StringToPiece = {string: piece for piece, string in PieceToString.items()}

UP = 10
DOWN = -10
LEFT = -1
RIGHT = 1

ALL_DIRECTIONS = ((UP, 'rq'), (DOWN, 'rq'), (LEFT, 'rq'), (RIGHT, 'rq'),
                  (UP + LEFT, 'bq'), (UP + RIGHT, 'bq'), (DOWN + LEFT, 'bq'), (DOWN + RIGHT, 'bq'))

ROOK_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

KNIGHT_MOVES = (UP + UP + LEFT, UP + UP + RIGHT, UP + LEFT + LEFT, UP + RIGHT + RIGHT,
                DOWN + DOWN + LEFT, DOWN + DOWN + RIGHT, DOWN + LEFT + LEFT, DOWN + RIGHT + RIGHT)

BISHOP_DIRECTIONS = (UP + LEFT, UP + RIGHT, DOWN + LEFT, DOWN + RIGHT)

KING_MOVES = (UP, DOWN, LEFT, RIGHT, UP + LEFT, UP + RIGHT, DOWN + LEFT, DOWN + RIGHT)

TRUE_SQUARES = {
    81: 56, 82: 57, 83: 58, 84: 59, 85: 60, 86: 61, 87: 62, 88: 63,
    71: 48, 72: 49, 73: 50, 74: 51, 75: 52, 76: 53, 77: 54, 78: 55,
    61: 40, 62: 41, 63: 42, 64: 43, 65: 44, 66: 45, 67: 46, 68: 47,
    51: 32, 52: 33, 53: 34, 54: 35, 55: 36, 56: 37, 57: 38, 58: 39,
    41: 24, 42: 25, 43: 26, 44: 27, 45: 28, 46: 29, 47: 30, 48: 31,
    31: 16, 32: 17, 33: 18, 34: 19, 35: 20, 36: 21, 37: 22, 38: 23,
    21: 8, 22: 9, 23: 10, 24: 11, 25: 12, 26: 13, 27: 14, 28: 15,
    11: 0, 12: 1, 13: 2, 14: 3, 15: 4, 16: 5, 17: 6, 18: 7
}

FAKE_SQUARES = {
    56: 81, 57: 82, 58: 83, 59: 84, 60: 85, 61: 86, 62: 87, 63: 88,
    48: 71, 49: 72, 50: 73, 51: 74, 52: 75, 53: 76, 54: 77, 55: 78,
    40: 61, 41: 62, 42: 63, 43: 64, 44: 65, 45: 66, 46: 67, 47: 68,
    32: 51, 33: 52, 34: 53, 35: 54, 36: 55, 37: 56, 38: 57, 39: 58,
    24: 41, 25: 42, 26: 43, 27: 44, 28: 45, 29: 46, 30: 47, 31: 48,
    16: 31, 17: 32, 18: 33, 19: 34, 20: 35, 21: 36, 22: 37, 23: 38,
    8: 21, 9: 22, 10: 23, 11: 24, 12: 25, 13: 26, 14: 27, 15: 28,
    0: 11, 1: 12, 2: 13, 3: 14, 4: 15, 5: 16, 6: 17, 7: 18
}

CASTLE_RIGHTS = {'wk': 1, 'wq': 2, 'bk': 4, 'bq': 8}
REMOVE_CASTLE_RIGHTS = {'wk': 14, 'wq': 13, 'bk': 11, 'bq': 7}
ROOKS_POSITION = {'wk': FAKE_SQUARES[7], 'wq': FAKE_SQUARES[0], 'bk': FAKE_SQUARES[63], 'bq': FAKE_SQUARES[56]}
POSITION_ROOKS = {FAKE_SQUARES[7]: 'wk', FAKE_SQUARES[0]: 'wq', FAKE_SQUARES[63]: 'bk', FAKE_SQUARES[56]: 'bq'}
CASTLE_ROOK_POSITION = {13: (11, 14), 17: (18, 16), 83: (81, 84), 87: (88, 86)}

PROMOTION_PIECES = 'qrbn'

WHITE_PAWN_STARTING_RANK = 1
BLACK_PAWN_STARTING_RANK = 6

WHITE_PROMOTION_RANK = 7
BLACK_PROMOTION_RANK = 0

ALL_INVALID_SQUARES = {
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    10, 19,
    20, 29,
    30, 39,
    40, 49,
    50, 59,
    60, 69,
    70, 79,
    80, 89,
    90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
    100, 101, 102, 103, 104, 105, 106, 107, 108, 109
}

MATE_EVAL = INF * 4 // 5

PHASE_VALUE = {
    'k': 0,
    'p': 0,
    'r': 477,
    'n': 337,
    'b': 365,
    'q': 1025,
    '.': 0, 'x': 0
}

PHASE_VALUE_MID = {
    'k': 12000,
    'p': 82,
    'r': 477,
    'n': 337,
    'b': 365,
    'q': 1025,
    '.': 0, 'x': 0
}

PHASE_VALUE_END = {
    'k': 12000,
    'p': 94,
    'r': 512,
    'n': 281,
    'b': 297,
    'q': 936,
    '.': 0, 'x': 0
}

MVV_LVA_SCORES = {
    'pp': 105, 'pn': 205, 'pb': 305, 'pr': 405, 'pq': 505, 'pk': 605,
    'np': 104, 'nn': 204, 'nb': 304, 'nr': 404, 'nq': 504, 'nk': 604,
    'bp': 103, 'bn': 203, 'bb': 303, 'br': 403, 'bq': 503, 'bk': 603,
    'rp': 102, 'rn': 202, 'rb': 302, 'rr': 402, 'rq': 502, 'rk': 602,
    'qp': 101, 'qn': 201, 'qb': 301, 'qr': 401, 'qq': 501, 'qk': 601,
    'kp': 100, 'kn': 200, 'kb': 300, 'kr': 400, 'kq': 500, 'kk': 600
}

PAWN_TABLE_MID_WHITE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, -35, -1, -20, -23, -15, 24, 38, -22, 0,
                        0, -26, -4, -4, -10, 3, 3, 33, -12, 0,
                        0, -27, -2, -5, 12, 17, 6, 10, -25, 0,
                        0, -14, 13, 6, 21, 23, 12, 17, -23, 0,
                        0, -6, 7, 26, 31, 65, 56, 25, -20, 0,
                        0, 98, 134, 61, 95, 68, 126, 34, -11, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

PAWN_TABLE_MID_BLACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 98, 134, 61, 95, 68, 126, 34, -11, 0,
                        0, -6, 7, 26, 31, 65, 56, 25, -20, 0,
                        0, -14, 13, 6, 21, 23, 12, 17, -23, 0,
                        0, -27, -2, -5, 12, 17, 6, 10, -25, 0,
                        0, -26, -4, -4, -10, 3, 3, 33, -12, 0,
                        0, -35, -1, -20, -23, -15, 24, 38, -22, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

PAWN_TABLE_END_WHITE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 13, 8, 8, 10, 13, 0, 2, -7, 0,
                        0, 4, 7, -6, 1, 0, -5, -1, -8, 0,
                        0, 13, 9, -3, -7, -7, -8, 3, -1, 0,
                        0, 32, 24, 13, 5, -2, 4, 17, 17, 0,
                        0, 94, 100, 85, 67, 56, 53, 82, 84, 0,
                        0, 178, 173, 158, 134, 147, 132, 165, 187, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

PAWN_TABLE_END_BLACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 178, 173, 158, 134, 147, 132, 165, 187, 0,
                        0, 94, 100, 85, 67, 56, 53, 82, 84, 0,
                        0, 32, 24, 13, 5, -2, 4, 17, 17, 0,
                        0, 13, 9, -3, -7, -7, -8, 3, -1, 0,
                        0, 4, 7, -6, 1, 0, -5, -1, -8, 0,
                        0, 13, 8, 8, 10, 13, 0, 2, -7, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

KNIGHT_TABLE_MID_WHITE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, -105, -21, -58, -33, -17, -28, -19, -23, 0,
                          0, -29, -53, -12, -3, -1, 18, -14, -19, 0,
                          0, -23, -9, 12, 10, 19, 17, 25, -16, 0,
                          0, -13, 4, 16, 13, 28, 19, 21, -8, 0,
                          0, -9, 17, 19, 53, 37, 69, 18, 22, 0,
                          0, -47, 60, 37, 65, 84, 129, 73, 44, 0,
                          0, -73, -41, 72, 36, 23, 62, 7, -17, 0,
                          0, -167, -89, -34, -49, 61, -97, -15, -107, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

KNIGHT_TABLE_MID_BLACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, -167, -89, -34, -49, 61, -97, -15, -107, 0,
                          0, -73, -41, 72, 36, 23, 62, 7, -17, 0,
                          0, -47, 60, 37, 65, 84, 129, 73, 44, 0,
                          0, -9, 17, 19, 53, 37, 69, 18, 22, 0,
                          0, -13, 4, 16, 13, 28, 19, 21, -8, 0,
                          0, -23, -9, 12, 10, 19, 17, 25, -16, 0,
                          0, -29, -53, -12, -3, -1, 18, -14, -19, 0,
                          0, -105, -21, -58, -33, -17, -28, -19, -23, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

KNIGHT_TABLE_END_WHITE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, -29, -51, -23, -15, -22, -18, -50, -64, 0,
                          0, -42, -20, -10, -5, -2, -20, -23, -44, 0,
                          0, -23, -3, -1, 15, 10, -3, -20, -22, 0,
                          0, -18, -6, 16, 25, 16, 17, 4, -18, 0,
                          0, -17, 3, 22, 22, 22, 11, 8, -18, 0,
                          0, -24, -20, 10, 9, -1, -9, -19, -41, 0,
                          0, -25, -8, -25, -2, -9, -25, -24, -52, 0,
                          0, -58, -38, -13, -28, -31, -27, -63, -99, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

KNIGHT_TABLE_END_BLACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, -58, -38, -13, -28, -31, -27, -63, -99, 0,
                          0, -25, -8, -25, -2, -9, -25, -24, -52, 0,
                          0, -24, -20, 10, 9, -1, -9, -19, -41, 0,
                          0, -17, 3, 22, 22, 22, 11, 8, -18, 0,
                          0, -18, -6, 16, 25, 16, 17, 4, -18, 0,
                          0, -23, -3, -1, 15, 10, -3, -20, -22, 0,
                          0, -42, -20, -10, -5, -2, -20, -23, -44, 0,
                          0, -29, -51, -23, -15, -22, -18, -50, -64, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

BISHOP_TABLE_MID_WHITE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, -33, -3, -14, -21, -13, -12, -39, -21, 0,
                          0, 4, 15, 16, 0, 7, 21, 33, 1, 0,
                          0, 0, 15, 15, 15, 14, 27, 18, 10, 0,
                          0, -6, 13, 13, 26, 34, 12, 10, 4, 0,
                          0, -4, 5, 19, 50, 37, 37, 7, -2, 0,
                          0, -16, 37, 43, 40, 35, 50, 37, -2, 0,
                          0, -26, 16, -18, -13, 30, 59, 18, -47, 0,
                          0, -29, 4, -82, -37, -25, -42, 7, -8, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

BISHOP_TABLE_MID_BLACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, -29, 4, -82, -37, -25, -42, 7, -8, 0,
                          0, -26, 16, -18, -13, 30, 59, 18, -47, 0,
                          0, -16, 37, 43, 40, 35, 50, 37, -2, 0,
                          0, -4, 5, 19, 50, 37, 37, 7, -2, 0,
                          0, -6, 13, 13, 26, 34, 12, 10, 4, 0,
                          0, 0, 15, 15, 15, 14, 27, 18, 10, 0,
                          0, 4, 15, 16, 0, 7, 21, 33, 1, 0,
                          0, -33, -3, -14, -21, -13, -12, -39, -21, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

BISHOP_TABLE_END_WHITE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, -23, -9, -23, -5, -9, -16, -5, -17, 0,
                          0, -14, -18, -7, -1, 4, -9, -15, -27, 0,
                          0, -12, -3, 8, 10, 13, 3, -7, -15, 0,
                          0, -6, 3, 13, 19, 7, 10, -3, -9, 0,
                          0, -3, 9, 12, 9, 14, 10, 3, 2, 0,
                          0, 2, -8, 0, -1, -2, 6, 0, 4, 0,
                          0, -8, -4, 7, -12, -3, -13, -4, -14, 0,
                          0, -14, -21, -11, -8, -7, -9, -17, -24, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

BISHOP_TABLE_END_BLACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, -14, -21, -11, -8, -7, -9, -17, -24, 0,
                          0, -8, -4, 7, -12, -3, -13, -4, -14, 0,
                          0, 2, -8, 0, -1, -2, 6, 0, 4, 0,
                          0, -3, 9, 12, 9, 14, 10, 3, 2, 0,
                          0, -6, 3, 13, 19, 7, 10, -3, -9, 0,
                          0, -12, -3, 8, 10, 13, 3, -7, -15, 0,
                          0, -14, -18, -7, -1, 4, -9, -15, -27, 0,
                          0, -23, -9, -23, -5, -9, -16, -5, -17, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

ROOK_TABLE_MID_WHITE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, -19, -13, 1, 17, 16, 7, -37, -26, 0,
                        0, -44, -16, -20, -9, -1, 11, -6, -71, 0,
                        0, -45, -25, -16, -17, 3, 0, -5, -33, 0,
                        0, -36, -26, -12, -1, 9, -7, 6, -23, 0,
                        0, -24, -11, 7, 26, 24, 35, -8, -20, 0,
                        0, -5, 19, 26, 36, 17, 45, 61, 16, 0,
                        0, 27, 32, 58, 62, 80, 67, 26, 44, 0,
                        0, 32, 42, 32, 51, 63, 9, 31, 43, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

ROOK_TABLE_MID_BLACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 32, 42, 32, 51, 63, 9, 31, 43, 0,
                        0, 27, 32, 58, 62, 80, 67, 26, 44, 0,
                        0, -5, 19, 26, 36, 17, 45, 61, 16, 0,
                        0, -24, -11, 7, 26, 24, 35, -8, -20, 0,
                        0, -36, -26, -12, -1, 9, -7, 6, -23, 0,
                        0, -45, -25, -16, -17, 3, 0, -5, -33, 0,
                        0, -44, -16, -20, -9, -1, 11, -6, -71, 0,
                        0, -19, -13, 1, 17, 16, 7, -37, -26, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

ROOK_TABLE_END_WHITE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, -9, 2, 3, -1, -5, -13, 4, -20, 0,
                        0, -6, -6, 0, 2, -9, -9, -11, -3, 0,
                        0, -4, 0, -5, -1, -7, -12, -8, -16, 0,
                        0, 3, 5, 8, 4, -5, -6, -8, -11, 0,
                        0, 4, 3, 13, 1, 2, 1, -1, 2, 0,
                        0, 7, 7, 7, 5, 4, -3, -5, -3, 0,
                        0, 11, 13, 13, 11, -3, 3, 8, 3, 0,
                        0, 13, 10, 18, 15, 12, 12, 8, 5, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

ROOK_TABLE_END_BLACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 13, 10, 18, 15, 12, 12, 8, 5, 0,
                        0, 11, 13, 13, 11, -3, 3, 8, 3, 0,
                        0, 7, 7, 7, 5, 4, -3, -5, -3, 0,
                        0, 4, 3, 13, 1, 2, 1, -1, 2, 0,
                        0, 3, 5, 8, 4, -5, -6, -8, -11, 0,
                        0, -4, 0, -5, -1, -7, -12, -8, -16, 0,
                        0, -6, -6, 0, 2, -9, -9, -11, -3, 0,
                        0, -9, 2, 3, -1, -5, -13, 4, -20, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

QUEEN_TABLE_MID_WHITE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, -1, -18, -9, 10, -15, -25, -31, -50, 0,
                         0, -35, -8, 11, 2, 8, 15, -3, 1, 0,
                         0, -14, 2, -11, -2, -5, 2, 14, 5, 0,
                         0, -9, -26, -9, -10, -2, -4, 3, -3, 0,
                         0, -27, -27, -16, -16, -1, 17, -2, 1, 0,
                         0, -13, -17, 7, 8, 29, 56, 47, 57, 0,
                         0, -24, -39, -5, 1, -16, 57, 28, 54, 0,
                         0, -28, 0, 29, 12, 59, 44, 43, 45, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

QUEEN_TABLE_MID_BLACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, -28, 0, 29, 12, 59, 44, 43, 45, 0,
                         0, -24, -39, -5, 1, -16, 57, 28, 54, 0,
                         0, -13, -17, 7, 8, 29, 56, 47, 57, 0,
                         0, -27, -27, -16, -16, -1, 17, -2, 1, 0,
                         0, -9, -26, -9, -10, -2, -4, 3, -3, 0,
                         0, -14, 2, -11, -2, -5, 2, 14, 5, 0,
                         0, -35, -8, 11, 2, 8, 15, -3, 1, 0,
                         0, -1, -18, -9, 10, -15, -25, -31, -50, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

QUEEN_TABLE_END_WHITE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, -33, -28, -22, -43, -5, -32, -20, -41, 0,
                         0, -22, -23, -30, -16, -16, -23, -36, -32, 0,
                         0, -16, -27, 15, 6, 9, 17, 10, 5, 0,
                         0, -18, 28, 19, 47, 31, 34, 39, 23, 0,
                         0, 3, 22, 24, 45, 57, 40, 57, 36, 0,
                         0, -20, 6, 9, 49, 47, 35, 19, 9, 0,
                         0, -17, 20, 32, 41, 58, 25, 30, 0, 0,
                         0, -9, 22, 22, 27, 27, 19, 10, 20, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

QUEEN_TABLE_END_BLACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, -9, 22, 22, 27, 27, 19, 10, 20, 0,
                         0, -17, 20, 32, 41, 58, 25, 30, 0, 0,
                         0, -20, 6, 9, 49, 47, 35, 19, 9, 0,
                         0, 3, 22, 24, 45, 57, 40, 57, 36, 0,
                         0, -18, 28, 19, 47, 31, 34, 39, 23, 0,
                         0, -16, -27, 15, 6, 9, 17, 10, 5, 0,
                         0, -22, -23, -30, -16, -16, -23, -36, -32, 0,
                         0, -33, -28, -22, -43, -5, -32, -20, -41, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

KING_TABLE_MID_WHITE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, -15, 36, 12, -54, 8, -28, 24, 14, 0,
                        0, 1, 7, -8, -64, -43, -16, 9, 8, 0,
                        0, -14, -14, -22, -46, -44, -30, -15, -27, 0,
                        0, -49, -1, -27, -39, -46, -44, -33, -51, 0,
                        0, -17, -20, -12, -27, -30, -25, -14, -36, 0,
                        0, -9, 24, 2, -16, -20, 6, 22, -22, 0,
                        0, 29, -1, -20, -7, -8, -4, -38, -29, 0,
                        0, -65, 23, 16, -15, -56, -34, 2, 13, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

KING_TABLE_MID_BLACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, -65, 23, 16, -15, -56, -34, 2, 13, 0,
                        0, 29, -1, -20, -7, -8, -4, -38, -29, 0,
                        0, -9, 24, 2, -16, -20, 6, 22, -22, 0,
                        0, -17, -20, -12, -27, -30, -25, -14, -36, 0,
                        0, -49, -1, -27, -39, -46, -44, -33, -51, 0,
                        0, -14, -14, -22, -46, -44, -30, -15, -27, 0,
                        0, 1, 7, -8, -64, -43, -16, 9, 8, 0,
                        0, -15, 36, 12, -54, 8, -28, 24, 14, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

KING_TABLE_END_WHITE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, -53, -34, -21, -11, -28, -14, -24, -43, 0,
                        0, -27, -11, 4, 13, 14, 4, -5, -17, 0,
                        0, -19, -3, 11, 21, 23, 16, 7, -9, 0,
                        0, -18, -4, 21, 24, 27, 23, 9, -11, 0,
                        0, -8, 22, 24, 27, 26, 33, 26, 3, 0,
                        0, 10, 17, 23, 15, 20, 45, 44, 13, 0,
                        0, -12, 17, 14, 17, 17, 38, 23, 11, 0,
                        0, -74, -35, -18, -18, -11, 15, 4, -17, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

KING_TABLE_END_BLACK = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, -74, -35, -18, -18, -11, 15, 4, -17, 0,
                        0, -12, 17, 14, 17, 17, 38, 23, 11, 0,
                        0, 10, 17, 23, 15, 20, 45, 44, 13, 0,
                        0, -8, 22, 24, 27, 26, 33, 26, 3, 0,
                        0, -18, -4, 21, 24, 27, 23, 9, -11, 0,
                        0, -19, -3, 11, 21, 23, 16, 7, -9, 0,
                        0, -27, -11, 4, 13, 14, 4, -5, -17, 0,
                        0, -53, -34, -21, -11, -28, -14, -24, -43, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

EMPTY_TABLE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

MID_VALUES = {
    WhitePawn: PAWN_TABLE_MID_WHITE,
    WhiteRook: ROOK_TABLE_MID_WHITE,
    WhiteKnight: KNIGHT_TABLE_MID_WHITE,
    WhiteBishop: BISHOP_TABLE_MID_WHITE,
    WhiteQueen: QUEEN_TABLE_MID_WHITE,
    WhiteKing: KING_TABLE_MID_WHITE,
    BlackPawn: PAWN_TABLE_MID_BLACK,
    BlackRook: ROOK_TABLE_MID_BLACK,
    BlackKnight: KNIGHT_TABLE_MID_BLACK,
    BlackBishop: BISHOP_TABLE_MID_BLACK,
    BlackQueen: QUEEN_TABLE_MID_BLACK,
    BlackKing: KING_TABLE_MID_BLACK,
    EmptySquare: EMPTY_TABLE
}

END_VALUES = {
    WhitePawn: PAWN_TABLE_END_WHITE,
    WhiteRook: ROOK_TABLE_END_WHITE,
    WhiteKnight: KNIGHT_TABLE_END_WHITE,
    WhiteBishop: BISHOP_TABLE_END_WHITE,
    WhiteQueen: QUEEN_TABLE_END_WHITE,
    WhiteKing: KING_TABLE_END_WHITE,
    BlackPawn: PAWN_TABLE_END_BLACK,
    BlackRook: ROOK_TABLE_END_BLACK,
    BlackKnight: KNIGHT_TABLE_END_BLACK,
    BlackBishop: BISHOP_TABLE_END_BLACK,
    BlackQueen: QUEEN_TABLE_END_BLACK,
    BlackKing: KING_TABLE_END_BLACK,
    EmptySquare: EMPTY_TABLE
}

PREV_MOVE_BONUS = INF
PV_BONUS = INF * 2 // 3
PROMOTION_BONUS = INF // 2
MVV_LVA_BONUS = INF // 3
FIRST_KILLER_MOVE_BONUS = INF // 4
SECOND_KILLER_MOVE_BONUS = INF // 5

OPENING_PHASE = 6192
ENDGAME_PHASE = 518

MAX_DEPTH = 40
NULL_DEPTH_REDUCTION = 3
NODE_CHECK_INTERVAL = 1000
ASPIRATION = 40

MAX_HASH = 1 << 64

hash_castle = [randint(1, MAX_HASH) for _ in range(16)]
hash_pieces = [{piece: randint(1, MAX_HASH) if piece != EmptySquare else 0
                for piece in PieceToNumber} for _ in range(110)]


class Board(list):
    def __init__(self, board_state=None, colour=None, castle_rights=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.extend([Invalid] * 10)
        for _ in range(8):
            self.extend([Invalid] + [EmptySquare] * 8 + [Invalid])
        self.extend([Invalid] * 20)

        self.phase = self.board_hash = None
        self.mid_value = {'w': 0, 'b': 0, '.': 0}
        self.end_value = {'w': 0, 'b': 0, '.': 0}

        self.initialized = False
        self.white_king_position = self.black_king_position = None
        self.castle_rights = self.is_checked = self.white_turn = None

        self.moves = []
        self.repetitions = collections.Counter()

        if board_state is not None:
            if colour is None:
                raise Exception('COLOURRRRRRRRRRRRRRRR')
            self.update_board(board_state, colour, castle_rights)

    def update_board(self, board_state, colour, castle_rights=None):
        self.white_turn = colour == 'w'

        self.phase = 0
        self.mid_value = {'w': 0, 'b': 0, '.': 0}
        self.end_value = {'w': 0, 'b': 0, '.': 0}

        self.board_hash = 0

        differences_position = {}
        for rank_index, rank in enumerate(ranks):
            for file_index, file in enumerate(files):
                square = FAKE_SQUARES[rank_index * 8 + file_index]
                piece = PieceToString[board_state.piece_at(file, rank)]

                self.board_hash ^= hash_pieces[square][piece]

                self.phase += PHASE_VALUE[piece[1]]
                self.mid_value[piece[0]] += MID_VALUES[piece][square] + PHASE_VALUE_MID[piece[1]]
                self.end_value[piece[0]] += END_VALUES[piece][square] + PHASE_VALUE_END[piece[1]]

                if self[square] != piece:
                    self[square] = piece

                    if piece != EmptySquare:
                        differences_position[piece] = differences_position.get(piece, []) + [square]

                        if piece == WhiteKing:
                            self.white_king_position = square
                        if piece == BlackKing:
                            self.black_king_position = square

        prev_player = 'b' if self.white_turn else 'w'

        if self.initialized:
            if prev_player + 'k' in differences_position:
                self.castle_rights &= REMOVE_CASTLE_RIGHTS[prev_player + 'k'] & REMOVE_CASTLE_RIGHTS[prev_player + 'q']

            elif prev_player + 'r' in differences_position:
                if self[ROOKS_POSITION[prev_player + 'k']] != prev_player + 'r':
                    self.castle_rights &= REMOVE_CASTLE_RIGHTS[prev_player + 'k']
                if self[ROOKS_POSITION[prev_player + 'q']] != prev_player + 'r':
                    self.castle_rights &= REMOVE_CASTLE_RIGHTS[prev_player + 'q']

        else:
            self.initialized = True
            self.castle_rights = CASTLE_RIGHTS['wk'] | CASTLE_RIGHTS['wq'] | CASTLE_RIGHTS['bk'] | CASTLE_RIGHTS['bq']

        if castle_rights is not None:
            self.castle_rights = castle_rights

        self.board_hash ^= hash_castle[self.castle_rights]
        self.repetitions[self.board_hash] += 1

    def to_board_state(self):
        board_state_dict = {}
        for square_index, piece in enumerate(self):
            if square_index not in ALL_INVALID_SQUARES:
                board_state_dict[files[TRUE_SQUARES[square_index] % 8] +
                                 ranks[TRUE_SQUARES[square_index] // 8]] = StringToPiece[piece]

        return BoardState(board_state_dict)

    def move(self, move):
        start_piece, start, end, special = move
        self.moves.append((move, self[end], self.castle_rights, self.board_hash))

        self.board_hash ^= hash_castle[self.castle_rights]
        self.board_hash ^= hash_pieces[start][self[start]]
        self.board_hash ^= hash_pieces[end][self[end]]

        self.phase -= PHASE_VALUE[self[start][1]] + PHASE_VALUE[self[end][1]]
        self.mid_value[self[start][0]] -= MID_VALUES[self[start]][start] + PHASE_VALUE_MID[self[start][1]]
        self.mid_value[self[end][0]] -= MID_VALUES[self[end]][end] + PHASE_VALUE_MID[self[end][1]]
        self.end_value[self[start][0]] -= END_VALUES[self[start]][start] + PHASE_VALUE_END[self[start][1]]
        self.end_value[self[end][0]] -= END_VALUES[self[end]][end] + PHASE_VALUE_END[self[end][1]]

        self[start], self[end] = EmptySquare, start_piece
        start_colour = start_piece[0]

        if start_piece[1] == 'k':
            self.castle_rights &= REMOVE_CASTLE_RIGHTS[start_colour + 'k'] & REMOVE_CASTLE_RIGHTS[start_colour + 'q']

            if start_colour == 'w':
                self.white_king_position = end
            else:
                self.black_king_position = end

            if special == CASTLING:
                self.mid_value[start_colour] -= MID_VALUES[start_colour + 'r'][CASTLE_ROOK_POSITION[end][0]]
                self.end_value[start_colour] -= END_VALUES[start_colour + 'r'][CASTLE_ROOK_POSITION[end][0]]

                self[CASTLE_ROOK_POSITION[end][1]] = self[CASTLE_ROOK_POSITION[end][0]]
                self[CASTLE_ROOK_POSITION[end][0]] = EmptySquare

                self.mid_value[start_colour] += MID_VALUES[start_colour + 'r'][CASTLE_ROOK_POSITION[end][1]]
                self.end_value[start_colour] += END_VALUES[start_colour + 'r'][CASTLE_ROOK_POSITION[end][1]]

        elif start_piece[1] == 'r':
            if start in POSITION_ROOKS:
                self.castle_rights &= REMOVE_CASTLE_RIGHTS[POSITION_ROOKS[start]]

        if special[0] == PROMOTION:
            self[end] = start_colour + special[1]

        self.phase += PHASE_VALUE[self[start][1]] + PHASE_VALUE[self[end][1]]
        self.mid_value[self[start][0]] += MID_VALUES[self[start]][start] + PHASE_VALUE_MID[self[start][1]]
        self.mid_value[self[end][0]] += MID_VALUES[self[end]][end] + PHASE_VALUE_MID[self[end][1]]
        self.end_value[self[start][0]] += END_VALUES[self[start]][start] + PHASE_VALUE_END[self[start][1]]
        self.end_value[self[end][0]] += END_VALUES[self[end]][end] + PHASE_VALUE_END[self[end][1]]

        self.board_hash ^= hash_castle[self.castle_rights]
        self.board_hash ^= hash_pieces[start][self[start]]
        self.board_hash ^= hash_pieces[end][self[end]]

        self.white_turn = not self.white_turn
        self.repetitions[self.board_hash] += 1

    def unmove(self):
        self.repetitions[self.board_hash] -= 1
        if not self.repetitions[self.board_hash]:
            del self.repetitions[self.board_hash]

        self.white_turn = not self.white_turn
        (start_piece, start, end, special), end_piece, self.castle_rights, self.board_hash = self.moves.pop()

        self.phase -= PHASE_VALUE[self[start][1]] + PHASE_VALUE[self[end][1]]
        self.mid_value[self[start][0]] -= MID_VALUES[self[start]][start] + PHASE_VALUE_MID[self[start][1]]
        self.mid_value[self[end][0]] -= MID_VALUES[self[end]][end] + PHASE_VALUE_MID[self[end][1]]
        self.end_value[self[start][0]] -= END_VALUES[self[start]][start] + PHASE_VALUE_END[self[start][1]]
        self.end_value[self[end][0]] -= END_VALUES[self[end]][end] + PHASE_VALUE_END[self[end][1]]

        self[start], self[end] = start_piece, end_piece

        if start_piece[1] == 'k':
            if start_piece[0] == 'w':
                self.white_king_position = start
            else:
                self.black_king_position = start

            if special == CASTLING:
                self.mid_value[start_piece[0]] -= MID_VALUES[start_piece[0] + 'r'][CASTLE_ROOK_POSITION[end][1]]
                self.end_value[start_piece[0]] -= END_VALUES[start_piece[0] + 'r'][CASTLE_ROOK_POSITION[end][1]]

                self[CASTLE_ROOK_POSITION[end][0]] = self[CASTLE_ROOK_POSITION[end][1]]
                self[CASTLE_ROOK_POSITION[end][1]] = EmptySquare

                self.mid_value[start_piece[0]] += MID_VALUES[start_piece[0] + 'r'][CASTLE_ROOK_POSITION[end][0]]
                self.end_value[start_piece[0]] += END_VALUES[start_piece[0] + 'r'][CASTLE_ROOK_POSITION[end][0]]

        self.phase += PHASE_VALUE[self[start][1]] + PHASE_VALUE[self[end][1]]
        self.mid_value[self[start][0]] += MID_VALUES[self[start]][start] + PHASE_VALUE_MID[self[start][1]]
        self.mid_value[self[end][0]] += MID_VALUES[self[end]][end] + PHASE_VALUE_MID[self[end][1]]
        self.end_value[self[start][0]] += END_VALUES[self[start]][start] + PHASE_VALUE_END[self[start][1]]
        self.end_value[self[end][0]] += END_VALUES[self[end]][end] + PHASE_VALUE_END[self[end][1]]

    def has_check(self, square, ignore_square=None):
        players = 'wb' if self.white_turn else 'bw'
        pawn_step = UP if self.white_turn else DOWN

        if self[square + pawn_step + LEFT] == players[1] + 'p' or self[square + pawn_step + RIGHT] == players[1] + 'p':
            return True

        for direction, possible_pieces in ALL_DIRECTIONS:
            new_square = square
            while True:
                new_square += direction
                if new_square == ignore_square:
                    continue

                if self[new_square][0] in (players[0], Invalid[0]):
                    break

                if self[new_square][1] in possible_pieces:
                    return True

                elif self[new_square] != EmptySquare:
                    break

        for move in KNIGHT_MOVES:
            if self[square + move] == players[1] + 'n':
                return True

        for move in KING_MOVES:
            if self[square + move] == players[1] + 'k':
                return True

        return False

    def get_legal_moves(self, loud_moves_only=False):
        pawn_step = UP if self.white_turn else DOWN
        players = 'wb' if self.white_turn else 'bw'
        starting_rank = WHITE_PAWN_STARTING_RANK if self.white_turn else BLACK_PAWN_STARTING_RANK
        promotion_rank = WHITE_PROMOTION_RANK if self.white_turn else BLACK_PROMOTION_RANK

        def get_pawn_moves(square):
            if self[square + pawn_step] == EmptySquare and (not is_pinned or king_pin in (pawn_step, -pawn_step)):
                if TRUE_SQUARES[square + pawn_step] // 8 == promotion_rank:
                    for promotion_piece in PROMOTION_PIECES:
                        yield self[square], square, square + pawn_step, PROMOTION + promotion_piece
                else:
                    yield self[square], square, square + pawn_step, NORMAL

                if TRUE_SQUARES[square] // 8 == starting_rank and self[square + 2 * pawn_step] == EmptySquare:
                    yield self[square], square, square + 2 * pawn_step, PAWN_DOUBLE

            if self[square + pawn_step + LEFT][0] == players[1] and (not is_pinned or king_pin == pawn_step + LEFT):
                if TRUE_SQUARES[square + pawn_step + LEFT] // 8 == promotion_rank:
                    for promotion_piece in PROMOTION_PIECES:
                        yield self[square], square, square + pawn_step + LEFT, PROMOTION + promotion_piece
                else:
                    yield self[square], square, square + pawn_step + LEFT, NORMAL

            if self[square + pawn_step + RIGHT][0] == players[1] and (not is_pinned or king_pin == pawn_step + RIGHT):
                if TRUE_SQUARES[square + pawn_step + RIGHT] // 8 == promotion_rank:
                    for promotion_piece in PROMOTION_PIECES:
                        yield self[square], square, square + pawn_step + RIGHT, PROMOTION + promotion_piece
                else:
                    yield self[square], square, square + pawn_step + RIGHT, NORMAL

        def get_rook_moves(square):
            for direction in ROOK_DIRECTIONS:
                if is_pinned and king_pin not in (direction, -direction):
                    continue

                new_square = square
                while True:
                    new_square += direction
                    if self[new_square][0] in (players[0], Invalid[0]):
                        break

                    yield self[square], square, new_square, NORMAL

                    if self[new_square][0] == players[1]:
                        break

        def get_knight_moves(square):
            if not is_pinned:
                for move in KNIGHT_MOVES:
                    if self[square + move][0] not in (players[0], Invalid[0]):
                        yield self[square], square, square + move, NORMAL

        def get_bishop_moves(square):
            for direction in BISHOP_DIRECTIONS:
                if is_pinned and king_pin not in (direction, -direction):
                    continue

                new_square = square
                while True:
                    new_square += direction
                    if self[new_square][0] in (players[0], Invalid[0]):
                        break

                    yield self[square], square, new_square, NORMAL

                    if self[new_square][0] == players[1]:
                        break

        def get_queen_moves(square):
            yield from get_rook_moves(square)
            yield from get_bishop_moves(square)

        def get_king_moves(square):
            valid_castle = self[square] == players[0] + 'k' and square == (15 if self.white_turn else 85)

            if not checks and valid_castle and self[square + 1] == self[square + 2] == EmptySquare \
                    and (self.castle_rights & CASTLE_RIGHTS[players[0] + 'k']) and self[square + 3] == players[0] + 'r':
                if not self.has_check(square + 1, square) and not self.has_check(square + 2, square):
                    yield self[square], square, square + 2, CASTLING

            if not checks and valid_castle and self[square - 1] == self[square - 2] == self[square - 3] == EmptySquare \
                    and (self.castle_rights & CASTLE_RIGHTS[players[0] + 'q']) and self[square - 4] == players[0] + 'r':
                if not self.has_check(square - 1, square) and not self.has_check(square - 2, square):
                    yield self[square], square, square - 2, CASTLING

            for move in KING_MOVES:
                if self[square + move][0] not in (players[0], Invalid[0]) and not self.has_check(square + move, square):
                    yield self[square], square, square + move, NORMAL

        def process_pins():
            if self[king_pos + pawn_step + LEFT] == players[1] + 'p':
                checks.append((king_pos + pawn_step + LEFT, pawn_step + LEFT))

            if self[king_pos + pawn_step + RIGHT] == players[1] + 'p':
                checks.append((king_pos + pawn_step + RIGHT, pawn_step + RIGHT))

            for direction, possible_pieces in ALL_DIRECTIONS:
                pin, new_square = None, king_pos

                while True:
                    new_square += direction
                    if self[new_square] == Invalid:
                        break

                    cur_piece = self[new_square][1]
                    if self[new_square][0] == players[0]:
                        if pin is not None:
                            break

                        pin = new_square, direction

                    elif self[new_square][0] == players[1]:
                        if cur_piece in possible_pieces:
                            if pin is None:
                                checks.append((new_square, direction))
                            else:
                                pins[pin[0]] = pin[1]

                        break

            for move in KNIGHT_MOVES:
                if self[king_pos + move] == players[1] + 'n':
                    checks.append((king_pos + move, 0))

        all_moves = []
        king_pos = self.white_king_position if self.white_turn else self.black_king_position

        pins, checks = {}, []
        process_pins()

        if len(checks) > 1:
            all_moves.extend(get_king_moves(king_pos))
            return all_moves

        self.is_checked = True if checks else False

        for cur_square, cur_square_piece in enumerate(self):
            if cur_square_piece != Invalid and cur_square_piece[0] == players[0]:
                king_pin = pins.get(cur_square, None)
                is_pinned = king_pin is not None

                cur_piece_moves = None
                if self.is_checked:
                    cur_piece_moves = {checks[0][0]}
                    if self[checks[0][0]][1] != 'n':
                        check_square = king_pos
                        while True:
                            check_square += checks[0][1]
                            if self[check_square] == self[checks[0][0]]:
                                break

                            cur_piece_moves.add(check_square)

                g = None
                piece = cur_square_piece[1]
                if piece == 'p':
                    g = get_pawn_moves(cur_square)
                if piece == 'r':
                    g = get_rook_moves(cur_square)
                if piece == 'n':
                    g = get_knight_moves(cur_square)
                if piece == 'b':
                    g = get_bishop_moves(cur_square)
                if piece == 'q':
                    g = get_queen_moves(cur_square)
                if piece == 'k':
                    g = get_king_moves(cur_square)

                if cur_piece_moves is None or piece == 'k':
                    all_moves.extend(g)
                else:
                    all_moves.extend(move for move in g if move[2] in cur_piece_moves)

        if loud_moves_only:
            # all_moves = [move for move in all_moves if self[move[2]][0] == players[1]]
            all_moves = [move for move in all_moves if self[move[2]][0] == players[1] or move[3][0] == 'P']

        return all_moves

    def evaluate(self):
        evaluation = (((self.mid_value['w'] - self.mid_value['b']) * self.phase) +
                      ((self.end_value['w'] - self.end_value['b']) * (OPENING_PHASE - self.phase))) // OPENING_PHASE

        if self.phase <= ENDGAME_PHASE * 2:
            evaluation = 0.5 * (self.end_value['w'] - self.end_value['b'])

            rw, fw = divmod(TRUE_SQUARES[self.white_king_position], 8)
            rb, fb = divmod(TRUE_SQUARES[self.black_king_position], 8)

            mop_up = 1.6 * (14 - (abs(rw - rb) + abs(fw - fb)))
            if evaluation > 0:
                d01, d02, d11, d12 = 3 - rb, rb - 4, 3 - fb, fb - 4
                mop_up += 4.7 * ((d01 if d01 > d02 else d02) + (d11 if d11 > d12 else d12))
                evaluation += mop_up

            elif evaluation < 0:
                d01, d02, d11, d12 = 3 - rw, rw - 4, 3 - fw, fw - 4
                mop_up += 4.7 * ((d01 if d01 > d02 else d02) + (d11 if d11 > d12 else d12))
                evaluation -= mop_up

        return evaluation if self.white_turn else -evaluation


class Engine:
    def __init__(self, colour, time_per_move):
        self.name = 'OutOfStockFish'

        self.colour = 'w' if colour == PlayerColour.White else 'b'
        self.time_per_move = time_per_move
        self.board = Board()

        self.alpha, self.beta = -INF, INF
        self.pv_len = self.pv_table = self.history_table = self.first_killer = self.second_killer = None

        self.prev_move = None

        self.timeout = self.time_end = None
        self.pv_eval = self.order_pv = None
        self.node_count = 0

    def order_moves(self, moves, ply):
        all_moves = []
        for move in moves:
            score = 0

            if self.prev_move == move:
                score += PREV_MOVE_BONUS
                self.prev_move = None

            elif self.order_pv:
                if self.pv_table[0][ply] == move:
                    self.order_pv = False
                    score += PV_BONUS

            else:
                quiet = True

                if (captured := self.board[move[2]]) != EmptySquare:
                    score += MVV_LVA_BONUS + MVV_LVA_SCORES[self.board[move[1]][1] + captured[1]]
                    quiet = False

                if move[3][0] == PROMOTION:
                    score += PROMOTION_BONUS + PHASE_VALUE[move[3][1]]
                    quiet = False

                if quiet:
                    if self.first_killer[ply] == move:
                        score += FIRST_KILLER_MOVE_BONUS
                    elif self.second_killer[ply] == move:
                        score += SECOND_KILLER_MOVE_BONUS
                    else:
                        score += self.history_table[PieceToNumber[move[0]]][move[2]]

            all_moves.append((move, score))

        if all_moves:
            moves[:] = next(zip(*sorted(all_moves, key=lambda x: x[1], reverse=True)))

    def check_draw(self):
        return self.board.repetitions[self.board.board_hash] >= 3

    def get_best_move_depth(self, cur_depth, best_move=None):
        def quiesence(alpha, beta, ply):
            stand_pat = self.board.evaluate()
            if stand_pat >= beta:
                return beta
            if stand_pat < alpha - 975:
                return alpha
            if stand_pat > alpha:
                alpha = stand_pat

            self.node_count += 1
            if self.node_count % NODE_CHECK_INTERVAL == 0 and time() >= self.time_end:
                self.timeout = True
                return 0

            legal_moves = self.board.get_legal_moves(loud_moves_only=True)
            self.order_moves(legal_moves, ply)

            for move in legal_moves:
                self.board.move(move)
                evaluation = -quiesence(-beta, -alpha, ply + 1)
                self.board.unmove()

                if self.timeout or (self.node_count % NODE_CHECK_INTERVAL == 0 and time() >= self.time_end):
                    self.timeout = True
                    return 0

                if evaluation > alpha:
                    alpha = evaluation
                    if evaluation >= beta:
                        return beta

            return alpha

        def negamax(depth, alpha, beta, ply, null_move):
            self.pv_table[ply][ply], self.pv_len[ply] = None, 0

            legal_moves = self.board.get_legal_moves()
            if not legal_moves:
                if self.board.is_checked:
                    return -MATE_EVAL + ply
                return 0

            self.order_moves(legal_moves, ply)

            if self.board.is_checked:
                depth += 1

            self.node_count += 1
            if self.timeout or (self.node_count % NODE_CHECK_INTERVAL == 0 and time() >= self.time_end):
                self.timeout = True
                return 0

            if depth == 0:
                return quiesence(alpha, beta, ply)

            if null_move and depth - NULL_DEPTH_REDUCTION >= 0 and ply:
                self.board.white_turn = not self.board.white_turn
                evaluation = -negamax(depth - NULL_DEPTH_REDUCTION, -beta, -beta + 1, ply + 1, False)
                self.board.white_turn = not self.board.white_turn

                if evaluation >= beta:
                    return beta

            self.order_moves(legal_moves, ply)

            if self.pv_eval:
                self.pv_eval = False
                for move in legal_moves:
                    if move == self.pv_table[0][ply]:
                        self.pv_eval = self.order_pv = True

            for move in legal_moves:
                self.board.move(move)
                evaluation = -negamax(depth - 1, -beta, -alpha, ply + 1, True)
                self.board.unmove()

                if evaluation > alpha:
                    alpha = evaluation
                    self.pv_table[ply][ply] = move

                    if self.board[move[2]] == EmptySquare:
                        self.history_table[PieceToNumber[move[0]]][move[2]] += depth

                    if evaluation >= beta:
                        return beta

                    pv_line_start = ply + 1
                    pv_line_end = ply + 1 + self.pv_len[ply + 1]

                    self.pv_table[ply][pv_line_start: pv_line_end] = self.pv_table[ply + 1][pv_line_start: pv_line_end]
                    self.pv_len[ply] = 1 + self.pv_len[ply + 1]

                    if evaluation >= beta:
                        if self.board[move[2]] == EmptySquare:
                            self.first_killer[ply], self.second_killer[ply] = move, self.first_killer[ply]

                        return beta

                    if self.check_draw():
                        return 0

            return alpha

        self.prev_move = best_move

        self.node_count = 0
        self.pv_len = [0] * MAX_DEPTH
        self.pv_table = [[None] * MAX_DEPTH for _ in range(MAX_DEPTH)]
        self.first_killer, self.second_killer = [None] * MAX_DEPTH, [None] * MAX_DEPTH
        self.history_table = [[0] * 110 for _ in range(13)]
        self.pv_eval = True

        cur_ply = 0
        cur_evaluation = negamax(cur_depth, self.alpha, self.beta, cur_ply, False)

        if self.beta <= cur_evaluation or cur_evaluation <= self.alpha:
            self.alpha, self.beta = -INF, INF
            self.pv_len = [0] * MAX_DEPTH
            self.pv_table = [[None] * MAX_DEPTH for _ in range(MAX_DEPTH)]
            self.first_killer, self.second_killer = [None] * MAX_DEPTH, [None] * MAX_DEPTH

            cur_evaluation = negamax(cur_depth, self.alpha, self.beta, cur_ply, False)

        self.alpha, self.beta = cur_evaluation - ASPIRATION, cur_evaluation + ASPIRATION

        if not self.timeout:
            return self.pv_table[0][0]
        else:
            return best_move

    def get_best_move(self):
        best_move = None
        for depth in range(1, 10):
            best_move = self.get_best_move_depth(depth, best_move)
            if self.timeout:
                break

        return best_move
    
    def get_move(self, board_state):
        self.board.update_board(board_state, self.colour)

        time_start = time()
        self.time_end = time_start + self.time_per_move - 1
        self.timeout = False

        best_move = self.get_best_move()
        self.board.move(best_move)

        return self.board.to_board_state()
