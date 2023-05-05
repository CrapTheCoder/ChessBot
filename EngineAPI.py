from random import choice, randint
from functools import reduce
"""
Write your code in this file to participate in the Chess Bot challenge!

Username: crap_the_coder
"""
from ContestUtils import PlayerColour, BoardState, BoardPiece
from ContestUtils import files, ranks

WHITE = PlayerColour.White
BLACK = PlayerColour.Black
EMPTY = BoardPiece.EmptySquare

STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

files_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
ranks_index = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}

Pieces = {
    WHITE: [BoardPiece.WhitePawn, BoardPiece.WhiteRook, BoardPiece.WhiteKnight,
            BoardPiece.WhiteBishop, BoardPiece.WhiteQueen, BoardPiece.WhiteKing],

    BLACK: [BoardPiece.BlackPawn, BoardPiece.BlackRook, BoardPiece.BlackKnight,
            BoardPiece.BlackBishop, BoardPiece.BlackQueen, BoardPiece.BlackKing]
}

INF = int(1e18)

PieceValue = {
    BoardPiece.WhitePawn: 100,
    BoardPiece.WhiteRook: 500,
    BoardPiece.WhiteKnight: 290,
    BoardPiece.WhiteBishop: 310,
    BoardPiece.WhiteQueen: 900,
    BoardPiece.WhiteKing: INF,
    BoardPiece.BlackPawn: -100,
    BoardPiece.BlackRook: -500,
    BoardPiece.BlackKnight: -290,
    BoardPiece.BlackBishop: -310,
    BoardPiece.BlackQueen: -900,
    BoardPiece.BlackKing: -INF,
    EMPTY: 0
}

HashIndexing = {
    BoardPiece.WhitePawn: 0,
    BoardPiece.WhiteRook: 1,
    BoardPiece.WhiteKnight: 2,
    BoardPiece.WhiteBishop: 3,
    BoardPiece.WhiteQueen: 4,
    BoardPiece.WhiteKing: 5,
    BoardPiece.BlackPawn: 6,
    BoardPiece.BlackRook: 7,
    BoardPiece.BlackKnight: 8,
    BoardPiece.BlackBishop: 9,
    BoardPiece.BlackQueen: 10,
    BoardPiece.BlackKing: 11,
}

PAWN_MOVES = (-1, 0, 1)
ROOK_DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))
BISHOP_DIRECTIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
KNIGHT_MOVES = ((1, 2), (2, 1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1))
KING_MOVES = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

hash_range = (1 << 128) - 1
turn_hash = randint(1, hash_range)
hash_table = {(i, j): {piece: randint(1, hash_range) if piece != EMPTY else 0
                       for piece in PieceValue} for i in range(8) for j in range(8)}

# TODO:
#  Implement Minimax
#  Implement Alpha-Beta-Pruning
#  Implement Position Tables
#  Implement Castling, En Passant
#  Use MultiProcessing

class Engine:
    @staticmethod
    def move(board, start, end, promotion=None, cur_hash=None):
        start_value, end_value = board.get(start, EMPTY), board.get(end, EMPTY)

        if cur_hash is not None:
            cur_hash ^= hash_table[start][start_value]
            cur_hash ^= hash_table[end][end_value]

        board[end] = promotion or board.get(start, EMPTY)

        if cur_hash is not None:
            cur_hash ^= hash_table[start][board.get(start, EMPTY)]
            cur_hash ^= hash_table[end][board.get(end, EMPTY)]

        del board[start]

        if cur_hash is not None:
            return start_value, end_value, cur_hash
        else:
            return start_value, end_value

    @staticmethod
    def unmove(board, start_value, end_value, start, end, promotion=None):
        board[start] = start_value
        board[end] = end_value

    memo = {}
    moves = []

    def __init__(self, colour, time_per_move):
        self.board = None
        self.colour = colour
        self.time_per_move = time_per_move
        self.move_count = 0

    @staticmethod
    def compute_hash(board):
        return reduce(int.__xor__, (hash_table[index][piece] for index, piece in board.items()))

    @staticmethod
    def to_dict(board_state):
        return {(ranks_index[rank], files_index[file]): board_state.piece_at(file, rank)
                for rank in ranks_index for file in files_index if board_state.piece_at(file, rank) != EMPTY}

    @staticmethod
    def opponent_colour(colour):
        return WHITE if colour == BLACK else BLACK

    @staticmethod
    def get_valid_moves(board, colour):
        other_colour = Engine.opponent_colour(colour)

        def valid(rank, file):
            return 0 <= rank <= 7 and 0 <= file <= 7

        def get_pawn_moves(rank, file):
            step = 1 if colour == WHITE else -1
            starting = 1 if colour == WHITE else 6
            promotion = 7 if colour == WHITE else 0

            if colour == WHITE:
                promotion_pieces = (BoardPiece.WhiteRook, BoardPiece.WhiteKnight,
                                    BoardPiece.WhiteBishop, BoardPiece.WhiteQueen)
            else:
                promotion_pieces = (BoardPiece.BlackRook, BoardPiece.BlackKnight,
                                    BoardPiece.BlackBishop, BoardPiece.BlackQueen)

            for hori in PAWN_MOVES:
                if valid(rank + step, file + hori):
                    next_square = board.get((rank + step, file + hori), EMPTY)

                    if (hori == 0 and next_square == EMPTY) or (hori != 0 and next_square in Pieces[other_colour]):
                        if rank + step == promotion:
                            for promotion_piece in promotion_pieces:
                                yield (rank, file), (rank + step, file + hori), promotion_piece

                        else:
                            yield (rank, file), (rank + step, file + hori)

            if rank == starting and board.get((rank + step, file), EMPTY) == board.get((rank + 2 * step, file), EMPTY) == EMPTY:
                yield (rank, file), (rank + 2 * step, file)

        def get_rook_moves(rank, file):
            for vert, hori in ROOK_DIRECTIONS:
                rank_, file_ = rank + vert, file + hori
                while valid(rank_, file_):
                    if board.get((rank_, file_), EMPTY) in Pieces[colour]:
                        break

                    yield (rank, file), (rank_, file_)

                    if board.get((rank_, file_), EMPTY) in Pieces[other_colour]:
                        break

                    rank_ += vert
                    file_ += hori

        def get_knight_moves(rank, file):
            for vert, hori in KNIGHT_MOVES:
                if valid(rank + vert, file + hori):
                    if board.get((rank + vert, file + hori), EMPTY) not in Pieces[colour]:
                        yield (rank, file), (rank + vert, file + hori)

        def get_bishop_moves(rank, file):
            for vert, hori in BISHOP_DIRECTIONS:
                rank_, file_ = rank + vert, file + hori
                while valid(rank_, file_):
                    if board.get((rank_, file_), EMPTY) in Pieces[colour]:
                        break

                    yield (rank, file), (rank_, file_)

                    if board.get((rank_, file_), EMPTY) in Pieces[other_colour]:
                        break

                    rank_ += vert
                    file_ += hori

        def get_queen_moves(rank, file):
            yield from get_bishop_moves(rank, file)
            yield from get_rook_moves(rank, file)

        def get_king_moves(rank, file):
            for vert, hori in KING_MOVES:
                if valid(rank + vert, file + hori):
                    if board.get((rank + vert, file + hori), EMPTY) not in Pieces[colour]:
                        yield (rank, file), (rank + vert, file + hori)

        for (rank_index, file_index), piece in list(board.items()):
            if piece in Pieces[colour]:
                if piece in (BoardPiece.WhitePawn, BoardPiece.BlackPawn):
                    yield from get_pawn_moves(rank_index, file_index)
                if piece in (BoardPiece.WhiteRook, BoardPiece.BlackRook):
                    yield from get_rook_moves(rank_index, file_index)
                if piece in (BoardPiece.WhiteKnight, BoardPiece.BlackKnight):
                    yield from get_knight_moves(rank_index, file_index)
                if piece in (BoardPiece.WhiteBishop, BoardPiece.BlackBishop):
                    yield from get_bishop_moves(rank_index, file_index)
                if piece in (BoardPiece.WhiteQueen, BoardPiece.BlackQueen):
                    yield from get_queen_moves(rank_index, file_index)
                if piece in (BoardPiece.WhiteKing, BoardPiece.BlackKing):
                    yield from get_king_moves(rank_index, file_index)

    @staticmethod
    def get_legal_moves(board, colour):
        all_legal_moves = []
        for move in Engine.get_valid_moves(board, colour):
            start_value, end_value = Engine.move(board, *move)
            if not Engine.has_check(board, colour):
                all_legal_moves.append(move)

            Engine.unmove(board, start_value, end_value, *move)

        return all_legal_moves

    @staticmethod
    def has_check(board, colour):
        other_colour = Engine.opponent_colour(colour)
        king = BoardPiece.WhiteKing if colour == WHITE else BoardPiece.BlackKing

        for opponent_move in Engine.get_valid_moves(board, other_colour):
            if board.get(opponent_move[1], EMPTY) == king:
                return True

        return False

    @staticmethod
    def evaluate(board):
        return sum(PieceValue[piece] for piece in board.values())

    @staticmethod
    def minimax(board, cur_hash, colour, depth, alpha=-INF, beta=INF):
        if (cur_hash, depth) in Engine.memo:
            return Engine.memo[cur_hash, depth]

        legal_moves = Engine.get_legal_moves(board, colour)

        if not legal_moves:
            if Engine.has_check(board, colour):
                Engine.memo[cur_hash, depth] = -INF if colour == WHITE else INF
            else:
                Engine.memo[cur_hash, depth] = 0

            return Engine.memo[cur_hash, depth]

        if depth == 0:
            Engine.memo[cur_hash, depth] = Engine.evaluate(board)
            return Engine.memo[cur_hash, depth]

        best_eval = -INF if colour == WHITE else INF
        for move in legal_moves:
            start_value, end_value, new_hash = Engine.move(board, *move, cur_hash=cur_hash)
            new_hash ^= turn_hash

            eval_cur = Engine.minimax(board, new_hash, Engine.opponent_colour(colour), depth - 1, alpha, beta)

            if colour == WHITE:
                best_eval = eval_cur if eval_cur > best_eval else best_eval
                alpha = eval_cur if eval_cur > alpha else alpha

            else:
                best_eval = eval_cur if eval_cur < best_eval else best_eval
                beta = eval_cur if eval_cur < beta else beta

            Engine.unmove(board, start_value, end_value, *move)

            if beta <= alpha:
                break

        Engine.memo[cur_hash, depth] = best_eval
        return Engine.memo[cur_hash, depth]

    @staticmethod
    def get_minimax_move(board, colour):
        legal_moves = Engine.get_legal_moves(board, colour)

        cur_hash = Engine.compute_hash(board)

        max_eval, max_eval_moves = -INF if colour == WHITE else INF, []
        for move in legal_moves:
            start_value, end_value, new_hash = Engine.move(board, *move, cur_hash=cur_hash)
            evaluation = Engine.minimax(board, new_hash, Engine.opponent_colour(colour), 1)
            Engine.unmove(board, start_value, end_value, *move)

            if (colour == WHITE and evaluation > max_eval) or (colour == BLACK and evaluation < max_eval):
                max_eval, max_eval_moves = evaluation, [move]

            elif evaluation == max_eval:
                max_eval_moves.append(move)

        return choice(max_eval_moves)

    @staticmethod
    def convert_board(board):
        return BoardState({
            files[file_index] + ranks[rank_index]: piece
            for (rank_index, file_index), piece in board.items()
        })

    def get_move(self, board_state):
        self.board = self.to_dict(board_state)
        self.move_count += 1

        minimax_move = self.get_minimax_move(self.board, self.colour)
        Engine.move(self.board, *minimax_move)

        return self.convert_board(self.board)


class Engine2(Engine):
    def __init__(self, colour, time_per_move, greedy):
        super().__init__(colour, time_per_move)
        self.greedy = greedy

    @staticmethod
    def get_greedy_move(board, colour):
        other_colour = Engine2.opponent_colour(colour)
        legal_moves = Engine2.get_legal_moves(board, colour)

        max_eval, max_eval_moves = -1e5 if colour == WHITE else 1e5, []
        for move in legal_moves:
            start_value, end_value = Engine.move(board, *move)
            opponent_legal_moves = Engine2.get_legal_moves(board, other_colour)

            if not opponent_legal_moves:
                if Engine2.has_check(board, other_colour):
                    return move

                continue

            evaluation = Engine2.evaluate(board)
            Engine.unmove(board, start_value, end_value, *move)

            if (colour == WHITE and evaluation > max_eval) or (colour == BLACK and evaluation < max_eval):
                max_eval, max_eval_moves = evaluation, [move]

            elif evaluation == max_eval:
                max_eval_moves.append(move)

        return choice(max_eval_moves)

    def get_move(self, board_state):
        self.board = self.to_dict(board_state)
        self.move_count += 1

        if self.greedy:
            greedy_move = self.get_greedy_move(self.board, self.colour)
            Engine.move(self.board, *greedy_move)
        else:
            random_move = choice(self.get_legal_moves(self.board, self.colour))
            Engine.move(self.board, *random_move)

        print(self.convert_board(self.board))
        return self.convert_board(self.board)


def main():
    import cProfile
    import pstats

    ew = Engine(WHITE, 5)
    b = BoardState.from_fen('r1bq1rk1/1pp1bpp1/p1np1n1p/4p3/2B1P3/P1NPBN2/1PPQ1PPP/R4RK1')

    with cProfile.Profile() as pr:
        print(ew.get_move(b))

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='profiled.prof')


if __name__ == '__main__':
    main()
