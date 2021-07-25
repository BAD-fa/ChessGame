from Rules import Rules
from ChessBoard import Board
import os


class Manager:
    def __init__(self):
        self.color = "\033[0;34m"
        self.board = Board([], self.color).board
        self.rules = Rules()
        self.white_turn = True
        self.print_board()

    def print_board(self):
        os.system('cls')
        s = ''
        for r in self.board:
            for c in r:
                s += c
            s += '\n'
        print(s)

    def update_board(self, move):
        self.board[move[1][1]][move[1][0]] = self.board[move[0][1]][move[0][0]]
        self.board[move[0][1]][move[0][0]] = ' '
        self.print_board()

    def move_piece(self):
        check = ' '
        if self.white_turn:
            if self.rules.is_in_check(self.board, "\033[1;37m"):
                check = "\033[31m" + '    !!!  IN CHECK  !!!' + '\033[0m'

            if self.rules.is_checkmate(self.board, "\033[0;34m"):
                print("BLUE has won!")
                return False
            else:
                turn = 'WHITE TURN'
        else:
            if self.rules.is_in_check(self.board, "\033[0;34m"):
                check = "\033[31m" + '    !!!  IN CHECK  !!!' + '\033[0m'

            if self.rules.is_checkmate(self.board, "\033[1;37m"):
                print("WHITE has won!")
                return False
            else:
                turn = 'BLUE TURN'

        movement = input('Please enter a move (ex: a2 to a4) : {} {}\n'.format(turn, check)).split(' ')

        if self.move_validator(movement):
            if self.white_turn:
                move = self.move_converter(movement)
                if self.rules.is_legal_move(self.board, '\033[1;37m', move[0], move[1]):
                    if self.rules.does_move_put_player_in_check(self.board, '\033[1;37m', move[0], move[1]):
                        print("Can't put king in check! Try again")
                    else:
                        if self.rules.castling(self.board, '\033[1;37m', move[0], move[1]):
                            self.castling_detector(move)
                        self.update_board(move)
                        self.white_turn = False
                else:
                    print("Can't move '{}' to given coordinates! Try again".format(self.board[move[0][1]][move[0][0]]))
            else:
                move = self.move_converter(movement)
                if self.rules.is_legal_move(self.board, '\033[0;34m', move[0], move[1]):
                    if self.rules.does_move_put_player_in_check(self.board, '\033[0;34m', move[0], move[1]):
                        print("Can't put king in check! Try again")
                    else:
                        if self.rules.castling(self.board, '\033[0;34m', move[0], move[1]):
                            self.castling_detector(move)
                        self.update_board(move)
                        self.white_turn = True
                else:
                    print("Can't move '{}' to given coordinates! Try again".format(self.board[move[0][1]][move[0][0]]))
        else:
            print('Invalid input! Try again')

        return True

    def move_validator(self, move):
        chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ints = ['1', '2', '3', '4', '5', '6', '7', '8']
        if move[0][0] in chars and move[0][1] in ints and move[2][0] in chars and move[2][1] in ints:
            return True
        return False

    def move_converter(self, movement):
        move = [[], []]
        char_convert = {'a': 2, 'b': 5, 'c': 8, 'd': 11, 'e': 14, 'f': 17, 'g': 20, 'h': 23}
        int_convert = {'1': 23, '2': 20, '3': 17, '4': 14, '5': 11, '6': 8, '7': 5, '8': 2}
        for i in char_convert:
            if i == movement[0][0]:
                move[0].append(char_convert[i])
            if i == movement[2][0]:
                move[1].append(char_convert[i])
        for j in int_convert:
            if j == movement[0][1]:
                move[0].append(int_convert[j])
            if j == movement[2][1]:
                move[1].append(int_convert[j])
        return move

    def castling_detector(self, move):
        if move == self.move_converter(['e1', 'to', 'c1']):
            self.update_board(self.move_converter(['a1', 'to', 'd1']))
        if move == self.move_converter(['e1', 'to', 'g1']):
            self.update_board(self.move_converter(['h1', 'to', 'f1']))
        if move == self.move_converter(['e8', 'to', 'c8']):
            self.update_board(self.move_converter(['a8', 'to', 'd8']))
        if move == self.move_converter(['e8', 'to', 'g8']):
            self.update_board(self.move_converter(['h8', 'to', 'f8']))


if __name__ == "__main__":
    G = Manager()
    continue_game = True
    while continue_game:
        continue_game = G.move_piece()
    input("Press 'ENTER' to exit")
