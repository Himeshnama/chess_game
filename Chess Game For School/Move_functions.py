import copy


class Move_Functions:
    def __init__(self, App):
        self.App = App
        self.pins = self.App.pins

    def get_all_B_movable_poses(self, B_Pos, W_Pos, pins):
        self.pins = pins
        B_movable_poses = {}
        for piece_t in B_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in B_Pos[piece_t]:
                    if "R" in piece:
                        B_movable_poses[piece] = (self.get_B_Rook_movable_pos(B_Pos[piece_t][piece], B_Pos, W_Pos))
                    elif "H" in piece:
                        B_movable_poses[piece] = (self.get_B_Horse_movable_pos(B_Pos[piece_t][piece], B_Pos, W_Pos))
                    elif "P" in piece:
                        B_movable_poses[piece] = (self.get_B_Pawn_movable_pos(B_Pos[piece_t][piece], B_Pos, W_Pos))
                    else:
                        B_movable_poses[piece] = (self.get_B_Bishop_movable_pos(B_Pos[piece_t][piece], B_Pos, W_Pos))

            else:
                if "Minister" in piece_t:
                    B_movable_poses[piece_t] = (self.get_B_Minister_movable_pos(B_Pos[piece_t], B_Pos, W_Pos))
        B_movable_poses["Black King"] = (
            self.get_B_King_movable_pos(self.App.get_pos_for_piece("Black", "Black King", B_Pos, W_Pos), B_Pos, W_Pos))

        return B_movable_poses

    def get_all_W_movable_poses(self, B_Pos, W_Pos, pins):
        self.pins = pins
        W_movable_poses = {}
        for piece_t in W_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece in W_Pos[piece_t]:
                    if "R" in piece:
                        W_movable_poses[piece] = (self.get_W_Rook_movable_pos(W_Pos[piece_t][piece], B_Pos, W_Pos))
                    elif "H" in piece:
                        W_movable_poses[piece] = (self.get_W_Horse_movable_pos(W_Pos[piece_t][piece], B_Pos, W_Pos))
                    elif "P" in piece:
                        W_movable_poses[piece] = (self.get_W_Pawn_movable_pos(W_Pos[piece_t][piece], B_Pos, W_Pos))
                    else:
                        W_movable_poses[piece] = (self.get_W_Bishop_movable_pos(W_Pos[piece_t][piece], B_Pos, W_Pos))

            else:
                if "Minister" in piece_t:
                    W_movable_poses[piece_t] = (self.get_W_Minister_movable_pos(W_Pos[piece_t], B_Pos, W_Pos))
        W_movable_poses["White King"] = (
            self.get_W_King_movable_pos(self.App.get_pos_for_piece("White", "White King", B_Pos, W_Pos), B_Pos, W_Pos))
        return W_movable_poses

    def get_B_Minister_movable_pos(self, pos, B_Pos, W_Pos):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == pos[0] and self.pins[i][1] == pos[1]:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                break
        movable_pos = []
        add = True
        for x in range(pos[0] + 1, 9):
            add = True
            to_add_pos = (x, pos[1])
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] - 1, 0, -1):
            add = True
            to_add_pos = (x, pos[1])
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for y in range(pos[1] + 1, 9):
            add = True
            to_add_pos = (pos[0], y)
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for y in range(pos[1] - 1, 0, -1):
            add = True
            to_add_pos = (pos[0], y)
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] + 1, 9):
            y = pos[1] + (x - pos[0])
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] + 1, 9):
            y = pos[1] - (x - pos[0])
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] - 1, 0, -1):
            y = pos[1] + (pos[0] - x)
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] - 1, 0, -1):
            y = pos[1] - (pos[0] - x)
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        movable_pos_copy = copy.deepcopy(movable_pos)
        for move in movable_pos_copy:
            if piece_pinned and self.App.find_direction(pos, move) != pin_direction:
                movable_pos.remove(move)

        return movable_pos

    def get_B_Rook_movable_pos(self, pos, B_Pos, W_Pos):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == pos[0] and self.pins[i][1] == pos[1]:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                break
        movable_pos = []
        add = True
        for x in range(pos[0] + 1, 9):
            add = True
            to_add_pos = (x, pos[1])
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] - 1, 0, -1):
            add = True
            to_add_pos = (x, pos[1])
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for y in range(pos[1] + 1, 9):
            add = True
            to_add_pos = (pos[0], y)
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for y in range(pos[1] - 1, 0, -1):
            add = True
            to_add_pos = (pos[0], y)
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        movable_pos_copy = copy.deepcopy(movable_pos)
        for move in movable_pos_copy:
            if piece_pinned and self.App.find_direction(pos, move) != pin_direction:
                movable_pos.remove(move)

        return movable_pos

    def get_B_Bishop_movable_pos(self, pos, B_Pos, W_Pos):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == pos[0] and self.pins[i][1] == pos[1]:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                break
        movable_pos = []
        add = True
        for x in range(pos[0] + 1, 9):
            y = pos[1] + (x - pos[0])
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] + 1, 9):
            y = pos[1] - (x - pos[0])
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] - 1, 0, -1):
            y = pos[1] + (pos[0] - x)
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] - 1, 0, -1):
            y = pos[1] - (pos[0] - x)
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        add = False
                        break

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        movable_pos_copy = copy.deepcopy(movable_pos)
        for move in movable_pos_copy:
            if piece_pinned and self.App.find_direction(pos, move) != pin_direction:
                movable_pos.remove(move)

        return movable_pos

    def get_B_Horse_movable_pos(self, pos, B_Pos, W_Pos):
        piece_pinned = False
        movable_pos = []
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == pos[0] and self.pins[i][1] == pos[1]:
                piece_pinned = True
                break
        if not piece_pinned:
            movable_pos = [
                (pos[0] - 1, pos[1] + 2),
                (pos[0] + 1, pos[1] + 2),
                (pos[0] - 1, pos[1] - 2),
                (pos[0] + 1, pos[1] - 2),
                (pos[0] + 2, pos[1] + 1),
                (pos[0] - 2, pos[1] + 1),
                (pos[0] + 2, pos[1] - 1),
                (pos[0] - 2, pos[1] - 1),
            ]
            check_movable_pos = movable_pos.copy()

            for check_pos in movable_pos:
                if check_pos[0] > 8 or check_pos[0] < 1 or check_pos[1] > 8 or check_pos[1] < 1:
                    check_movable_pos.remove(check_pos)
                else:
                    for piece_t in B_Pos:
                        if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                            for piece in B_Pos[piece_t]:
                                if check_pos == B_Pos[piece_t][piece]:
                                    check_movable_pos.remove(check_pos)
                        else:
                            if check_pos == B_Pos[piece_t]:
                                check_movable_pos.remove(check_pos)
            movable_pos = check_movable_pos.copy()

        return movable_pos

    def get_B_Pawn_movable_pos(self, pos, B_Pos, W_Pos):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == pos[0] and self.pins[i][1] == pos[1]:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                break
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == pos[0] and self.App.pins[i][1] == pos[1]:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                break
        movable_pos = []

        if pos[1] == 7:
            to_add_poses = [(pos[0], pos[1] - 1), (pos[0], pos[1] - 2)]
        else:
            to_add_poses = [(pos[0], pos[1] - 1)]

        add = True
        for check_pos in to_add_poses:
            add = True
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if check_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if check_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if check_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if check_pos == B_Pos[piece_t]:
                        add = False
                        break

            if add:
                movable_pos.append(check_pos)
            else:
                break

        to_add_poses = [(pos[0] - 1, pos[1] - 1), (pos[0] + 1, pos[1] - 1)]
        add = False
        for check_pos in to_add_poses:
            add = False
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if check_pos == W_Pos[piece_t][piece]:
                            add = True
                            break
                else:
                    if check_pos == W_Pos[piece_t]:
                        add = True
                        break
            if add:
                movable_pos.append(check_pos)

        movable_pos_copy = copy.deepcopy(movable_pos)
        for move in movable_pos_copy:
            if piece_pinned and self.App.find_direction(pos, move) != pin_direction:
                movable_pos.remove(move)

        return movable_pos

    def get_B_King_movable_pos(self, pos, B_Pos, W_Pos):
        movable_pos = [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1] + 1),
            (pos[0] + 1, pos[1] - 1),
            (pos[0] - 1, pos[1] + 1),
            (pos[0] - 1, pos[1] - 1),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1)
        ]
        check_movable_pos = movable_pos.copy()

        for check_pos in movable_pos:
            if check_pos[0] > 8 or check_pos[0] < 1 or check_pos[1] > 8 or check_pos[1] < 1:
                check_movable_pos.remove(check_pos)
            else:
                for piece_t in B_Pos:
                    if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                        for piece in B_Pos[piece_t]:
                            if check_pos == B_Pos[piece_t][piece]:
                                check_movable_pos.remove(check_pos)
                    else:
                        if check_pos == B_Pos[piece_t]:
                            check_movable_pos.remove(check_pos)
        movable_pos = check_movable_pos.copy()

        movable_pos_copy = copy.deepcopy(movable_pos)
        for move in movable_pos_copy:
            B_Pos_copy = copy.deepcopy(B_Pos)
            W_Pos_copy = copy.deepcopy(W_Pos)
            B_Pos_copy["Black King"] = (move[0], move[1])

            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if move == W_Pos[piece_t][piece]:
                            W_Pos_copy[piece_t].pop(piece)
                else:
                    if move == W_Pos[piece_t]:
                        W_Pos_copy.pop(piece_t)

            pins, checks, in_check = self.App.find_pins_and_checks(B_Pos_copy, W_Pos_copy, "Black")
            if in_check:
                movable_pos.remove(move)
        '''for piece_t in B_Pos:
            if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                for piece_st in B_Pos[piece_t]:
                    if pos == B_Pos[piece_t][piece_st]:
                        piece_B, piece = piece_t, piece_st
        movable_pos_copy = copy.deepcopy(movable_pos)
        for poses in movable_pos_copy:
            Altered_B_Pos, Altered_W_Pos = copy.deepcopy(B_Pos), copy.deepcopy(W_Pos)
            Altered_B_Pos[piece_B][piece] = poses
            for t in W_Pos:
                if "Rook" in t or "Bishop" in t or "Horse" in t or "Pawn" in t:
                    for p in W_Pos[t]:
                        if poses == W_Pos[t][p]:
                            del Altered_W_Pos[t][p]
                else:
                    if poses == W_Pos[t]:
                        del Altered_W_Pos[t]
            if self.is_check(B_Pos["Black King"], "Black", Altered_B_Pos, Altered_W_Pos):
                movable_pos.remove(poses)'''
        return movable_pos

    def get_W_Minister_movable_pos(self, pos, B_Pos, W_Pos):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == pos[0] and self.pins[i][1] == pos[1]:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                break
        movable_pos = []
        add = True
        for x in range(pos[0] + 1, 9):
            y = pos[1] + (x - pos[0])
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] + 1, 9):
            y = pos[1] - (x - pos[0])
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] - 1, 0, -1):
            y = pos[1] + (pos[0] - x)
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] - 1, 0, -1):
            y = pos[1] - (pos[0] - x)
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] + 1, 9):
            add = True
            to_add_pos = (x, pos[1])
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] - 1, 0, -1):
            add = True
            to_add_pos = (x, pos[1])
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for y in range(pos[1] + 1, 9):
            add = True
            to_add_pos = (pos[0], y)
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for y in range(pos[1] - 1, 0, -1):
            add = True
            to_add_pos = (pos[0], y)
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        movable_pos_copy = copy.deepcopy(movable_pos)
        for move in movable_pos_copy:
            if piece_pinned and self.App.find_direction(pos, move) != pin_direction:
                movable_pos.remove(move)

        return movable_pos

    def get_W_Rook_movable_pos(self, pos, B_Pos, W_Pos):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == pos[0] and self.pins[i][1] == pos[1]:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                break
        movable_pos = []
        add = True
        for x in range(pos[0] + 1, 9):
            add = True
            to_add_pos = (x, pos[1])
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] - 1, 0, -1):
            add = True
            to_add_pos = (x, pos[1])
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for y in range(pos[1] + 1, 9):
            add = True
            to_add_pos = (pos[0], y)
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for y in range(pos[1] - 1, 0, -1):
            add = True
            to_add_pos = (pos[0], y)
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        movable_pos_copy = copy.deepcopy(movable_pos)
        for move in movable_pos_copy:
            if piece_pinned and self.App.find_direction(pos, move) != pin_direction:
                movable_pos.remove(move)

        return movable_pos

    def get_W_Bishop_movable_pos(self, pos, B_Pos, W_Pos):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == pos[0] and self.pins[i][1] == pos[1]:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                break
        movable_pos = []
        add = True
        for x in range(pos[0] + 1, 9):
            y = pos[1] + (x - pos[0])
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] + 1, 9):
            y = pos[1] - (x - pos[0])
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] - 1, 0, -1):
            y = pos[1] + (pos[0] - x)
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        for x in range(pos[0] - 1, 0, -1):
            y = pos[1] - (pos[0] - x)
            add = True
            to_add_pos = (x, y)
            if to_add_pos[1] > 8 or to_add_pos[1] < 1:
                break
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if to_add_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if to_add_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if to_add_pos == B_Pos[piece_t][piece]:
                            movable_pos.append(to_add_pos)
                            add = False
                            break
                else:
                    if to_add_pos == B_Pos[piece_t]:
                        movable_pos.append(to_add_pos)
                        add = False
                        break

            if add:
                movable_pos.append(to_add_pos)
            else:
                break

        movable_pos_copy = copy.deepcopy(movable_pos)
        for move in movable_pos_copy:
            if piece_pinned and self.App.find_direction(pos, move) != pin_direction:
                movable_pos.remove(move)

        return movable_pos

    def get_W_Horse_movable_pos(self, pos, B_Pos, W_Pos):
        piece_pinned = False
        movable_pos = []
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == pos[0] and self.pins[i][1] == pos[1]:
                piece_pinned = True
                break

        if not piece_pinned:
            movable_pos = [
                (pos[0] - 1, pos[1] + 2),
                (pos[0] + 1, pos[1] + 2),
                (pos[0] - 1, pos[1] - 2),
                (pos[0] + 1, pos[1] - 2),
                (pos[0] + 2, pos[1] + 1),
                (pos[0] - 2, pos[1] + 1),
                (pos[0] + 2, pos[1] - 1),
                (pos[0] - 2, pos[1] - 1),
            ]
            check_movable_pos = movable_pos.copy()

            for check_pos in movable_pos:
                if check_pos[0] > 8 or check_pos[0] < 1 or check_pos[1] > 8 or check_pos[1] < 1:
                    check_movable_pos.remove(check_pos)
                else:
                    for piece_t in W_Pos:
                        if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                            for piece in W_Pos[piece_t]:
                                if check_pos == W_Pos[piece_t][piece]:
                                    check_movable_pos.remove(check_pos)
                        else:
                            if check_pos == W_Pos[piece_t]:
                                check_movable_pos.remove(check_pos)
            movable_pos = check_movable_pos.copy()

        return movable_pos

    def get_W_Pawn_movable_pos(self, pos, B_Pos, W_Pos):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == pos[0] and self.pins[i][1] == pos[1]:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                break
        movable_pos = []
        if pos[1] == 2:
            to_add_poses = [(pos[0], pos[1] + 1), (pos[0], pos[1] + 2)]
        else:
            to_add_poses = [(pos[0], pos[1] + 1)]

        add = True
        for check_pos in to_add_poses:
            add = True
            for piece_t in W_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in W_Pos[piece_t]:
                        if check_pos == W_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if check_pos == W_Pos[piece_t]:
                        add = False
                        break

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if check_pos == B_Pos[piece_t][piece]:
                            add = False
                            break
                else:
                    if check_pos == B_Pos[piece_t]:
                        add = False
                        break

            if add:
                movable_pos.append(check_pos)
            else:
                break

        to_add_poses = [(pos[0] - 1, pos[1] + 1), (pos[0] + 1, pos[1] + 1)]
        add = False
        for check_pos in to_add_poses:
            add = False
            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if check_pos == B_Pos[piece_t][piece]:
                            add = True
                            break
                else:
                    if check_pos == B_Pos[piece_t]:
                        add = True
                        break
            if add:
                movable_pos.append(check_pos)

        movable_pos_copy = copy.deepcopy(movable_pos)
        for move in movable_pos_copy:
            if piece_pinned and self.App.find_direction(pos, move) != pin_direction:
                movable_pos.remove(move)

        return movable_pos

    def get_W_King_movable_pos(self, pos, B_Pos, W_Pos):
        movable_pos = [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1] + 1),
            (pos[0] + 1, pos[1] - 1),
            (pos[0] - 1, pos[1] + 1),
            (pos[0] - 1, pos[1] - 1),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1)
        ]

        check_movable_pos = movable_pos.copy()

        for check_pos in movable_pos:
            if check_pos[0] > 8 or check_pos[0] < 1 or check_pos[1] > 8 or check_pos[1] < 1:
                check_movable_pos.remove(check_pos)
            else:
                for piece_t in W_Pos:
                    if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                        for piece in W_Pos[piece_t]:
                            if check_pos == W_Pos[piece_t][piece]:
                                check_movable_pos.remove(check_pos)
                    else:
                        if check_pos == W_Pos[piece_t]:
                            check_movable_pos.remove(check_pos)

        movable_pos = check_movable_pos.copy()

        movable_pos_copy = copy.deepcopy(movable_pos)
        for move in movable_pos_copy:
            B_Pos_copy = copy.deepcopy(B_Pos)
            W_Pos_copy = copy.deepcopy(W_Pos)
            W_Pos_copy["White King"] = (move[0], move[1])

            for piece_t in B_Pos:
                if "Rook" in piece_t or "Bishop" in piece_t or "Horse" in piece_t or "Pawn" in piece_t:
                    for piece in B_Pos[piece_t]:
                        if move == B_Pos[piece_t][piece]:
                            B_Pos_copy[piece_t].pop(piece)
                else:
                    if move == B_Pos[piece_t]:
                        B_Pos_copy.pop(piece_t)
            pins, checks, in_check = self.App.find_pins_and_checks(B_Pos_copy, W_Pos_copy, "White")
            if in_check:
                movable_pos.remove(move)

        return movable_pos
