"""
Tic Tac Toe Player
"""

import math
import collections

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    winner( board )
    x_count = 0
    o_count = 0
    for i in range( 3 ):
        for j in range( 3 ):
            if board[ i ][ j ] == O:
                o_count += 1
            elif board[ i ][ j ] == X:
                x_count += 1

    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    possible_actions = []
    for i in range( 3 ):
        for j in range( 3 ):
            if board[ i ][ j ] == EMPTY:
                possible_actions.append( ( i , j ) )
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy_board( board )
    x, y = action
        
    if board_copy[ x ][ y ] == EMPTY:
        board_copy[ x ][ y ] = player( board_copy )
        
        return board_copy

    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] and board[0][0] == board[0][2]:
        return board[0][0]

    elif board[1][0] == board[1][1] and board[1][0] == board[1][2]:
        return board[1][0]

    elif board[2][0] == board[2][1] and board[2][0] == board[2][2]:
        return board[2][0]

    elif board[0][0] == board[1][0] and board[0][0] == board[2][0]:
        return board[0][0]

    elif board[0][1] == board[1][1] and board[0][1] == board[2][1]:
        return board[0][1]

    elif board[0][2] == board[1][2] and board[0][2] == board[2][2]:
        return board[0][2]

    elif board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        return board[0][0]
    
    elif board[2][0] == board[1][1] and board[2][0] == board[0][2]:
        return board[2][0]
    else:
        return None

def terminal(board):
    result = winner(board)
    if result == None:
        filled = True
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    filled = False
        return filled
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    player_who_won = winner( board )
    return 1 if player_who_won is X else -1 if player_who_won is O else 0


def copy_board( board ):
    board_copy = []
    for i in range( 3 ):
        row = []
        for j in range( 3 ):
            row.append( board[i][j] )
        board_copy.append( row )
    return board_copy

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    board_copy = copy_board( board )
    
    who_plays = player( board_copy )

    possible_actions = actions( board_copy )
    if len( possible_actions) > 0:
        return  obtain_best_move(minimax_helper( board_copy , possible_actions, who_plays ), board_copy, who_plays)
    else:
        terminal(board)
        return None

 
def minimax_helper( board, possible_actions, who_plays ):
    action_results = {}
    for action in possible_actions:
        action_results[ action ] = 0

    node = minimax_node( board, possible_actions, None)
    q = collections.deque()
    q.append( node )
    
    while len( q ) > 0:
        node = q.popleft()
        current_board = node.board
        current_actions = node.actions
        current_original_action = node.original_action
        
        if len( current_actions) > 0:
            for action in current_actions:
                x, y = action
                temp_board = copy_board( current_board )
                temp_board[x][y] = player( temp_board )
                temp_actions = [a for a in current_actions]
                temp_actions.pop( temp_actions.index( action ) )
                current_original_action = action
                if current_original_action is None:
                    current_original_action = action
                temp_node = minimax_node( temp_board, temp_actions , current_original_action)
                if winner(temp_board) == None:
                    q.append( temp_node )
                else:
                    action_results[current_original_action] += utility(temp_board)
        else:
            action_results[current_original_action] += utility( current_board) 
    print(action_results)
    return action_results

def obtain_best_move(action_results,board_copy, who_plays):
    actions = [key for key in action_results]
    actions_utility = [action_results[key] for key in action_results]
    if who_plays == X:
        return actions[actions_utility.index(min(actions_utility))]
    return actions[actions_utility.index(max(actions_utility))]
            

class minimax_node:
    def __init__( self, board, actions, original_action ):
        self.board = [row for row in board]
        self.actions = actions
        self.original_action = original_action
