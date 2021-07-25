class Board:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.board_creator()
        self.placing_pieces()

    def board_creator(self):
        color = False
        for i in range(24):
            self.board.append([])
            if i % 3 == 1:
                self.board[i].append(str(int(8 - (i-1)/3)) + ' ')
                for j in range(24):
                    if j % 3 == 0 and color:
                        self.board[i].append("\033[0;34m" + "| " + '\033[0m')
                    elif j % 3 == 0 and not color:
                        self.board[i].append("| ")
                    elif j % 3 == 1:
                        self.board[i].append(' ')
                    elif j % 3 == 2 and color:
                        self.board[i].append("\033[0;34m" + " |" + '\033[0m')
                        color = not color
                    elif j % 3 == 2 and not color:
                        self.board[i].append(" |")
                        color = not color
                self.board[i].append(' ' + str(int(8 - (i-1)/3)))

            else:
                self.board[i].append('  ')
                for k in range(8):
                    if color:
                        self.board[i].append("\033[0;34m" + ' --- ' + '\033[0m')
                    else:
                        self.board[i].append(' --- ')
                    color = not color
            if i % 3 == 2:
                color = not color

        self.board.insert(0, [
            '  ',
            '  a  ',
            '  b  ',
            '  c  ',
            '  d  ',
            '  e  ',
            '  f  ',
            '  g  ',
            '  h  ',
        ])
        self.board.append([
            '  ',
            '  a  ',
            '  b  ',
            '  c  ',
            '  d  ',
            '  e  ',
            '  f  ',
            '  g  ',
            '  h  ',
        ])

    def placing_pieces(self):
        temp_piece = ['R', 'N', 'B']
        for p in range(8):
            self.board[20][3 * p + 2] = ('P' + '\033[1;37m' + '\033[0m')
            self.board[5][3 * p + 2] = ("\033[0;34m" + 'P' + '\033[0m')

        for i in range(2):
            self.board[23][15 * i + 2] = (temp_piece[0] + '\033[1;37m' + '\033[0m')
            self.board[23][15 * i + 5] = (temp_piece[1] + '\033[1;37m' + '\033[0m')
            self.board[23][15 * i + 8] = (temp_piece[2] + '\033[1;37m' + '\033[0m')
            self.board[2][15 * i + 2] = ("\033[0;34m" + temp_piece[0] + '\033[0m')
            self.board[2][15 * i + 5] = ("\033[0;34m" + temp_piece[1] + '\033[0m')
            self.board[2][15 * i + 8] = ("\033[0;34m" + temp_piece[2] + '\033[0m')
            temp_piece.reverse()

        self.board[23][11] = ('Q' + '\033[1;37m' + '\033[0m')
        self.board[23][14] = ('K' + '\033[1;37m' + '\033[0m')
        self.board[2][11] = ("\033[0;34m" + 'Q' + '\033[0m')
        self.board[2][14] = ("\033[0;34m" + 'K' + '\033[0m')
