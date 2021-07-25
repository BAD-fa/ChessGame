class Rules:
    def is_checkmate(self, board, color):
        if color == '\033[1;37m':
            my_color = "\033[0;34m"
        elif color == "\033[0;34m":
            my_color = '\033[1;37m'

        my_color_valid_moves = []
        for row in range(8):
            for col in range(8):
                piece = board[3 * row + 2][3 * col + 2]
                if my_color in piece:
                    my_color_valid_moves.extend(self.get_list_of_valid_moves(board, my_color, [3 * col + 2, 3 * row+2]))
        if len(my_color_valid_moves) == 0:
            return True
        else:
            return False

    def get_list_of_valid_moves(self, board, color, start_pos):
        legal_destination_spaces = []
        for row in range(8):
            for col in range(8):
                d = [3 * col + 2, 3 * row + 2]
                if self.is_legal_move(board, color, start_pos, d):
                    if not self.does_move_put_player_in_check(board, color, start_pos, d):
                        legal_destination_spaces.append(d)
        return legal_destination_spaces

    def is_legal_move(self, board, color, start_pos, end_pos):
        start_pos_r = start_pos[1]
        start_pos_c = start_pos[0]
        end_pos_r = end_pos[1]
        end_pos_c = end_pos[0]
        start_piece = board[start_pos_r][start_pos_c]
        end_piece = board[end_pos_r][end_pos_c]

        if color == "\033[0;34m":
            enemy_color = '\033[1;37m'
        elif color == '\033[1;37m':
            enemy_color = "\033[0;34m"

        if start_pos == end_pos:
            return False

        if "P" in start_piece:
            # Pawn
            if color == '\033[1;37m':
                if end_pos_r == (start_pos_r - 3) and end_pos_c == start_pos_c and end_piece == ' ':
                    # moving forward one space
                    return True
                if start_pos_r == 20 and end_pos_r == (
                        start_pos_r - 6) and end_pos_c == start_pos_c and end_piece == ' ':
                    # white pawn on starting row can move forward 2 spaces if there is no one directly ahead
                    if self.is_clear_path(board, start_pos, end_pos):

                        return True
                if end_pos_r == start_pos_r - 3 and (
                        end_pos_c == start_pos_c + 3 or end_pos_c == start_pos_c - 3) and enemy_color in end_piece:
                    # attacking
                    return True

            elif color == "\033[0;34m":
                if end_pos_r == start_pos_r + 3 and end_pos_c == start_pos_c and end_piece == ' ':
                    # moving forward one space
                    return True
                if start_pos_r == 5 and end_pos_r == start_pos_r + 6 and end_pos_c == start_pos_c and end_piece == ' ':
                    # blue pawn on starting row can move forward 2 spaces if there is no one directly ahead
                    if self.is_clear_path(board, start_pos, end_pos):
                        return True
                if end_pos_r == start_pos_r + 3 and (
                        end_pos_c == start_pos_c + 3 or end_pos_c == start_pos_c - 3) and enemy_color in end_piece:
                    # attacking
                    return True

        elif "R" in start_piece:
            # Rook
            if (end_pos_r == start_pos_r or end_pos_c == start_pos_c) and (
                    end_piece == ' ' or enemy_color in end_piece):
                if self.is_clear_path(board, start_pos, end_pos):
                    return True

        elif "N" in start_piece:
            # Knight
            col_diff = end_pos_c - start_pos_c
            row_diff = end_pos_r - start_pos_r
            if end_piece == ' ' or enemy_color in end_piece:
                if col_diff == 3 and row_diff == -6:
                    return True
                if col_diff == 6 and row_diff == -3:
                    return True
                if col_diff == 6 and row_diff == 3:
                    return True
                if col_diff == 3 and row_diff == 6:
                    return True
                if col_diff == -3 and row_diff == 6:
                    return True
                if col_diff == -6 and row_diff == 3:
                    return True
                if col_diff == -6 and row_diff == -3:
                    return True
                if col_diff == -3 and row_diff == -6:
                    return True

        elif "B" in start_piece:
            # Bishop
            if (abs(end_pos_r - start_pos_r) == abs(end_pos_c - start_pos_c)) and (
                    end_piece == ' ' or enemy_color in end_piece):
                if self.is_clear_path(board, start_pos, end_pos):
                    return True

        elif "Q" in start_piece:
            # Queen
            if (end_pos_r == start_pos_r or end_pos_c == start_pos_c) and (
                    end_piece == ' ' or enemy_color in end_piece):
                if self.is_clear_path(board, start_pos, end_pos):
                    return True
            if (abs(end_pos_r - start_pos_r) == abs(end_pos_c - start_pos_c)) and (
                    end_piece == ' ' or enemy_color in end_piece):
                if self.is_clear_path(board, start_pos, end_pos):
                    return True

        elif "K" in start_piece:
            # King
            col_diff = end_pos_c - start_pos_c
            row_diff = end_pos_r - start_pos_r
            if end_piece == ' ' or enemy_color in end_piece:
                if abs(col_diff) == 3 and abs(row_diff) == 0:
                    return True
                if abs(col_diff) == 0 and abs(row_diff) == 3:
                    return True
                if abs(col_diff) == 3 and abs(row_diff) == 3:
                    return True
                if abs(col_diff) == 6 and abs(row_diff) == 0:
                    return self.castling(board, color, start_pos, end_pos)

        return False

    def does_move_put_player_in_check(self, board, color, start_pos, end_pos):
        # makes a hypothetical move; returns True if it puts current player into check
        start_pos_r = start_pos[1]
        start_pos_c = start_pos[0]
        end_pos_r = end_pos[1]
        end_pos_c = end_pos[0]
        start_piece = board[start_pos_r][start_pos_c]
        end_piece = board[end_pos_r][end_pos_c]

        # make the move, then test if 'color' is in check
        board[end_pos_r][end_pos_c] = start_piece
        board[start_pos_r][start_pos_c] = ' '

        ret_val = self.is_in_check(board, color)

        # undo temporary move
        board[end_pos_r][end_pos_c] = end_piece
        board[start_pos_r][start_pos_c] = start_piece

        return ret_val

    def is_in_check(self, board, color):
        # check if 'color' is in check
        # scan through squares for all enemy pieces; if there IsLegalMove to color's king, then return True.
        if color == "\033[0;34m":
            my_color = "\033[0;34m"
            enemy_color = '\033[1;37m'
        else:
            my_color = '\033[1;37m'
            enemy_color = "\033[0;34m"

        king_pos = [0, 0]
        # First, get current player's king location
        for row in range(8):
            for col in range(8):
                piece = board[3 * row + 2][3 * col + 2]
                if 'K' in piece and my_color in piece:
                    king_pos = [3 * col + 2, 3 * row + 2]

        # Check if any of enemy player's pieces has a legal move to current player's king
        for row in range(8):
            for col in range(8):
                piece = board[3 * col + 2][3 * row + 2]
                if enemy_color in piece:
                    if self.is_legal_move(board, enemy_color, [3 * row + 2, 3 * col + 2], king_pos):
                        return True
        return False

    def is_clear_path(self, board, start_pos, end_pos):
        # Return true if there is nothing in a straight line between start_pos and end_pos, non-inclusive
        # Direction could be +/- vertical, +/- horizontal, +/- diagonal
        start_pos_r = start_pos[1]
        start_pos_c = start_pos[0]
        end_pos_r = end_pos[1]
        end_pos_c = end_pos[0]

        if abs(start_pos_r - end_pos_r) <= 3 and abs(start_pos_c - end_pos_c) <= 3:
            return True
        else:
            if end_pos_r > start_pos_r and end_pos_c == start_pos_c:
                new_pos = [start_pos_r + 3, start_pos_c]
            elif end_pos_r < start_pos_r and end_pos_c == start_pos_c:
                new_pos = [start_pos_r - 3, start_pos_c]
            elif end_pos_r == start_pos_r and end_pos_c > start_pos_c:
                new_pos = [start_pos_r, start_pos_c + 3]
            elif end_pos_r == start_pos_r and end_pos_c < start_pos_c:
                new_pos = [start_pos_r, start_pos_c - 3]
            elif end_pos_r > start_pos_r and end_pos_c > start_pos_c:
                new_pos = [start_pos_r + 3, start_pos_c + 3]
            elif end_pos_r > start_pos_r and end_pos_c < start_pos_c:
                new_pos = [start_pos_r + 3, start_pos_c - 3]
            elif end_pos_r < start_pos_r and end_pos_c > start_pos_c:
                new_pos = [start_pos_r - 3, start_pos_c + 3]
            elif end_pos_r < start_pos_r and end_pos_c < start_pos_c:
                new_pos = [start_pos_r - 3, start_pos_c - 3]

        if board[new_pos[0]][new_pos[1]] != ' ':
            return False
        else:
            new_pos.reverse()
            return self.is_clear_path(board, new_pos, end_pos)

    def castling(self, board, color, start_pos, end_pos):

        col_diff = end_pos[0] - start_pos[0]
        row_diff = end_pos[1] - start_pos[1]

        if color == '\033[1;37m':
            if start_pos == [14, 23] and col_diff == 6 and abs(row_diff) == 0:
                if 'R' in board[start_pos[1]][start_pos[0] + 9]:
                    if self.is_legal_move(board, color, [23, 23], [17, 23]):
                        if self.is_clear_path(board, start_pos, end_pos):
                            return True

            elif start_pos == [14, 23] and col_diff == -6 and abs(row_diff) == 0:
                if 'R' in board[start_pos[1]][start_pos[0] - 12]:
                    if self.is_legal_move(board, color, [2, 23], [11, 23]):
                        if self.is_clear_path(board, start_pos, end_pos):
                            return True

        if color == "\033[0;34m":
            if start_pos == [14, 2] and col_diff == -6 and abs(row_diff) == 0:
                if 'R' in board[start_pos[1]][start_pos[0] - 12]:
                    if self.is_legal_move(board, color, [2, 2], [11, 2]):
                        if self.is_clear_path(board, start_pos, end_pos):
                            return True
            elif start_pos == [14, 2] and col_diff == 6 and abs(row_diff) == 0:
                if 'R' in board[start_pos[1]][start_pos[0] + 9]:
                    if self.is_legal_move(board, color, [23, 2], [17, 2]):
                        if self.is_clear_path(board, start_pos, end_pos):
                            return True

        return False
