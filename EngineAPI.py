from random import choice

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

Pieces = {
    WHITE: [BoardPiece.WhitePawn, BoardPiece.WhiteRook, BoardPiece.WhiteKnight,
            BoardPiece.WhiteBishop, BoardPiece.WhiteQueen, BoardPiece.WhiteKing],

    BLACK: [BoardPiece.BlackPawn, BoardPiece.BlackRook, BoardPiece.BlackKnight,
            BoardPiece.BlackBishop, BoardPiece.BlackQueen, BoardPiece.BlackKing]
}

INF = 1000000000000000000

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
    BoardPiece.EmptySquare: 0
}

PAWN_MOVES = (-1, 0, 1)
ROOK_DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))
BISHOP_DIRECTIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
KNIGHT_MOVES = ((1, 2), (2, 1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1))
KING_MOVES = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


class Engine:
    class Move:
        def __init__(self, coord1, coord2, capture=False, promotion=None):
            self.coord1 = coord1
            self.coord2 = coord2
            self.capture = capture
            self.promotion = promotion

    # TODO:
    #  Implement Castling, En Passant
    #  Implement Minimax
    #  Implement Alpha-Beta-Pruning
    #  Implement Position Tables

    def __init__(self, colour, time_per_move):
        self.board = None
        self.colour = colour
        self.time_per_move = time_per_move
        self.move_count = 0

    @staticmethod
    def to_dict(board_state):
        return {(ranks.index(rank), files.index(file)): board_state.piece_at(file, rank)
                for rank in ranks for file in files if board_state.piece_at(file, rank) != EMPTY}

    @staticmethod
    def get_opponent_colour(colour):
        return WHITE if colour == BLACK else BLACK

    @staticmethod
    def get_valid_moves(board, colour):
        other_colour = Engine.get_opponent_colour(colour)

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
                    straight = hori == 0 and (rank + step, file) not in board
                    diagonal = hori != 0 and board.get((rank + step, file + hori), EMPTY) in Pieces[other_colour]

                    if straight or diagonal:
                        if rank + step == promotion:
                            for promotion_piece in promotion_pieces:
                                yield (rank, file), (rank + step, file + hori), promotion_piece

                        else:
                            yield (rank, file), (rank + step, file + hori)

            if rank == starting and (rank + step, file) not in board and (rank + 2 * step, file) not in board:
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

        for (rank_index, file_index), piece in board.items():
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
    def make_move(board, coord1, coord2, promotion_piece=None):
        board[coord2] = promotion_piece or board[coord1]
        del board[coord1]

    @staticmethod
    def get_legal_moves(board, colour):
        all_legal_moves = []
        for move in Engine.get_valid_moves(board, colour):
            board_copy = board.copy()
            Engine.make_move(board_copy, *move)

            if not Engine.has_check(board_copy, colour):
                all_legal_moves.append(move)

        return all_legal_moves

    @staticmethod
    def has_check(board, colour):
        other_colour = Engine.get_opponent_colour(colour)
        king = BoardPiece.WhiteKing if colour == WHITE else BoardPiece.BlackKing

        for opponent_move in Engine.get_valid_moves(board, other_colour):
            if board.get(opponent_move[1], EMPTY) == king:
                return True

        return False

    @staticmethod
    def evaluate(board):
        return sum(PieceValue[piece] for piece in board.values())

    @staticmethod
    def minimax(board, colour, depth, alpha=-INF, beta=INF):
        legal_moves = Engine.get_legal_moves(board, colour)

        if not legal_moves:
            if Engine.has_check(board, colour):
                return -INF if colour == WHITE else +INF
            return 0

        if depth == 0:
            return Engine.evaluate(board)

        if colour == WHITE:
            eval_max = -INF
            for move in legal_moves:
                board_copy = board.copy()
                Engine.make_move(board_copy, *move)

                eval_cur = Engine.minimax(board_copy, BLACK, depth - 1, alpha, beta)
                eval_max = eval_cur if eval_cur > eval_max else eval_max
                alpha = eval_cur if eval_cur > alpha else alpha
                if beta <= alpha:
                    break

            return eval_max

        else:
            eval_min = INF
            for move in legal_moves:
                board_copy = board.copy()
                Engine.make_move(board_copy, *move)

                eval_cur = Engine.minimax(board_copy, WHITE, depth - 1, alpha, beta)
                eval_min = eval_cur if eval_cur < eval_min else eval_min
                beta = eval_cur if eval_cur < beta else beta
                if beta <= alpha:
                    break

            return eval_min

    @staticmethod
    def get_minimax_move(board, colour):
        legal_moves = Engine.get_legal_moves(board, colour)

        max_eval, max_eval_moves = -INF if colour == WHITE else INF, []
        for move in legal_moves:
            board_copy = board.copy()
            Engine.make_move(board_copy, *move)

            evaluation = Engine.minimax(board_copy, Engine.get_opponent_colour(colour), 2)

            if (colour == WHITE and evaluation > max_eval) or (colour == BLACK and evaluation < max_eval):
                max_eval, max_eval_moves = evaluation, [move]

            elif evaluation == max_eval:
                max_eval_moves.append(move)

        return choice(max_eval_moves)

    @staticmethod
    def get_greedy_move(board, colour):
        other_colour = Engine.get_opponent_colour(colour)
        legal_moves = Engine.get_legal_moves(board, colour)

        max_eval, max_eval_moves = -1e5 if colour == WHITE else 1e5, []
        for move in legal_moves:
            board_copy = board.copy()
            Engine.make_move(board_copy, *move)

            opponent_legal_moves = Engine.get_legal_moves(board_copy, other_colour)

            if not opponent_legal_moves:
                if Engine.has_check(board_copy, other_colour):
                    return move

                continue

            evaluation = Engine.evaluate(board_copy)

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
        self.make_move(self.board, *minimax_move)

        return self.convert_board(self.board)

    def legal_move_tester(self, board_state):
        self.board = self.to_dict(board_state)

        for move in self.get_legal_moves(self.board, self.colour):
            board_copy = self.board.copy()

            self.make_move(self.board, *move)

            print(self.convert_board(self.board))
            print('-' * 40)

            self.board = board_copy

    def greedy_move_tester(self, board_state):
        self.board = self.to_dict(board_state)

        greedy_move = self.get_greedy_move(self.board, self.colour)

        if not greedy_move:
            return None

        self.make_move(self.board, *greedy_move)

        print(self.convert_board(self.board))
        return self.convert_board(self.board)


class Engine2(Engine):
    def __init__(self, colour, time_per_move, greedy):
        super().__init__(colour, time_per_move)
        self.greedy = greedy

    def get_move(self, board_state):
        self.board = self.to_dict(board_state)
        self.move_count += 1

        if self.greedy:
            greedy_move = self.get_greedy_move(self.board, self.colour)
            self.make_move(self.board, *greedy_move)
        else:
            random_move = choice(self.get_legal_moves(self.board, self.colour))
            self.make_move(self.board, *random_move)

        print(self.convert_board(self.board))
        return self.convert_board(self.board)


def main():
    import cProfile
    import pstats

    c = 0
    ew = Engine(WHITE, 5)
    # eb = Engine2(BLACK, 5, False)
    b = BoardState.from_fen(STARTING_FEN)

    print(ew.get_move(b))

    # while True:
    #     c += 1
    #     print(c)
    #
    #     b = ew.get_move(b)
    #     if b is None:
    #         break
    #
    #     print('-' * 50)
    #
    #     b = eb.get_move(b)
    #     if b is None:
    #         break
    #
    #     print('-' * 50)


if __name__ == '__main__':
    main()
