import numpy as np 
import matplotlib.pyplot as plt
# Using this guy's BG board implementation, to learn 
# https://github.com/weekend37/Backgammon/blob/master/Backgammon.py

# Then going to build my own computer AI , or alter game slightly
def init_board():
    # initializes the game board
    #-numbers represent player -1's count on a given board index,
    # positive numbers represent player 1s count on a given board index
    board = np.zeros(29)
    board[1] = -2
    board[12] = -5
    board[17] = -3
    board[19] = -5
    board[6] = 5
    board[8] = 3
    board[13] = 5
    board[24] = 2
    return board

print(init_board())    

def roll_dice():
    # rolls the dice
    # between 1,6, 2 dice
    dice = np.random.randint(1,7,2)
    return dice

print(roll_dice())
def check_for_error(board):
    # checks for obvious errors
    errorInProgram = False
    
    if (sum(board[board>0]) != 15 or sum(board[board<0]) != -15):
        # too many or too few pieces on board
        errorInProgram = True
        print("Too many or too few pieces on board!")
    return errorInProgram
def game_over(board):
    # returns True if the game is over    
    return board[27]==15 or board[28]==-15

def pretty_print(board):
    string = str(np.array2string(board[1:13])+'\n'+
                 np.array2string(board[24:12:-1])+'\n'+
                 np.array2string(board[25:29]))
    print("board: \n", string)
board = init_board()
# pretty_print(board)   
def legal_move(board, die, player):
    # finds legal moves for a board and one dice
    # inputs are some BG-board, the number on the die and which player is up
    # outputs all the moves (just for the one die)
    possible_moves = []

    if player == 1:
        
        
        ######You're stuck on rail for this if condition
        if board[25] > 0:
            #25 -die is the index that you would come into , if you are on the rail if player == 1
            # checking to see if there is not a block there, and if so, add [25, spot where you end up] 
            start_pip = 25-die
            if board[start_pip] > -2:
                possible_moves.append(np.array([25,start_pip]))
                
        ##### not stuck on rail, but all your pieces are in your zone       
        else:
            print(f"you have {sum(board[7:25]>0)} spots with pieces not in your zone")

            print(np.max(np.where(board[1:7]>0)[0]+1))
            print(np.min(np.where(board[19:25]<0)[0]))

            # adding options if player is bearing off
            possible_start_pips_list = []
            #This is checking for the actual pieces, with amounts > 0, on the board in spots 7:24, 
            #If this is 0, that means all of player 1s pieces, are in his zone, and he can start
            #taking them off
            if sum(board[7:25]>0) == 0:
                
                #Once all pieces are in your zone, this checks if the spot represented by the 
                # die has pips on it
                # in player 1's case, this is a positive number, so say there were 3 pips on the 6 spot,
                #you append [6,27] to possible moves, 27 representing player 1's rail
                if (board[die] > 0):
                    possible_moves.append(np.array([die,27]))
                    
                elif not game_over(board): 
                    #checks if all pieces are off, for player 1, and if pips can be removed:

                    # everybody's past the dice throw?
                    #He is checking to see if the maximum amount from the rail is 5, meaning a 6 could take
                    # a 5 off, but not a 4 off, because s represents furthers spot,
                    # I changed it to represent first seeing if s <6, otherwise you can't fulfill the condition
                    s = np.max(np.where(board[1:7]>0)[0]+1)
                    if s<6:
                        if s<die:
                            possible_moves.append(np.array([s,27]))
                    
            possible_start_pips = np.where(board[0:25]>0)[0]
            #Possible_start_pips for player 1 represents all positions on the board, where you have a piece,
            # as the count of pieces on each tile for player 1, is represented by a positive integer, 2 for 2, 1 for 1,
            #etc...

            possible_start_pips_list.append(possible_start_pips)
            
            # Not stuck on rail, not ready to take your pieces off, this represents all other moves
            
            for s in possible_start_pips:
                                
                #He is checking to see if position - die > 0, meaning if it is possible move on board the amount
                # of spots represented by the die
                end_pip = s-die
                if end_pip > 0:
                    #And if it is, checking to see if opponent does not have block there, block is
                    #indicated by -2 or less for player 1, as opponents pieces are represented by negative integer
                    if board[end_pip] > -2:
                        #Appends starting pip, and then where you could move, represented by end pip
                        possible_moves.append(np.array([s,end_pip]))
            
    #This represents other player, where all of his values are represented in negative integer counts                  
    elif player == -1:
        # dead piece, needs to be brought back to life
        # if player == -1, his rail is represented by index 26 on the board, and his count on the rail is 
        #the absolute value of the negative number on that rail, so if it is <1, needs to get his off the rail
        print(np.max(np.where(board[1:7]>0)[0]+1))
        print(np.min(np.where(board[19:25]<0)[0]))
        if board[26] < 0: 
            start_pip = die
            #in this case, he is coming in from the 0 spot, meaning if he rolls a 6, and opponent has value <2, 
            #opponent does not have a block, and he can come in
            if board[start_pip] < 2:
                #youre taking off the rail, and moving to the index of the die, for player -1
                possible_moves.append(np.array([26,start_pip]))
                
        # no dead pieces       
        else:
            # adding options if player is bearing off
            if sum(board[1:19]<0) == 0:
                #again, this represents player -1 having all pieces in spots 19-24, meaning he can start taking them off 
                if (board[25-die] < 0):
                    #if the index in his zone is negative, he has spots there, he can take that position off
                    #in this case, when player -1 takes pieces off, he's going to index 28, that is his spot
                    possible_moves.append(np.array([25-die,28]))
                elif not game_over(board): 
                    # everybody's past the dice throw?
                    #represents smallest count in player -1's ending zone, where you can take pieces off
                    s = np.min(np.where(board[19:25]<0)[0])
                    #this checks if you can start taking pips off from the -1 players zone, 
                    # condition is it has be on index 20 or less, otherwise, normal rolls apply
                    if s > 0:
                        if (6-s)<die:
                            possible_moves.append(np.array([19+s,28]))

            # if player -1 can not take pieces off, or is not stuck, this represents all other rolls
            # looking for negative numbers at all indexes, then since he's going the other way, adding the die
            # to that index, and if other player's count is not 2 or greater, player -1 can move to that spot
            possible_start_pips = np.where(board[0:25]<0)[0]
            for s in possible_start_pips:
                end_pip = s+die
                if end_pip < 25:
                    if board[end_pip] < 2:
                        possible_moves.append(np.array([s,end_pip]))
        
    return possible_moves
print(legal_move(board, 6, -1))
print(board[24])  
#########
# #####################
# ######################
# TODO, left off here:
# #MAYBE START YOUR OWN CODING HERE
# 
#   

def update_board(board, move, player):
    # updates the board
    # inputs are some board, one move and the player
    # outputs the updated board
    board_to_update = np.copy(board) 

    # if the move is there
    if len(move) > 0:
        startPip = move[0]
        endPip = move[1]
        
        # moving the dead piece if the move kills a piece
        kill = board_to_update[endPip]==(-1*player)
        if kill:
            board_to_update[endPip] = 0
            jail = 25+(player==1)
            board_to_update[jail] = board_to_update[jail] - player
        
        board_to_update[startPip] = board_to_update[startPip]-1*player
        board_to_update[endPip] = board_to_update[endPip]+player

    return board_to_update


def legal_moves(board, dice, player):
    # finds all possible moves and the possible board after-states
    # inputs are the BG-board, the dices rolled and which player is up
    # outputs the possible pair of moves (if they exists) and their after-states

    moves = []
    boards = []

    # try using the first dice, then the second dice
    possible_first_moves = legal_move(board, dice[0], player)
    for m1 in possible_first_moves:
        temp_board = update_board(board,m1,player)
        possible_second_moves = legal_move(temp_board,dice[1], player)
        for m2 in possible_second_moves:
            moves.append(np.array([m1,m2]))
            boards.append(update_board(temp_board,m2,player))
        
    if dice[0] != dice[1]:
        # try using the second dice, then the first one
        possible_first_moves = legal_move(board, dice[1], player)
        for m1 in possible_first_moves:
            temp_board = update_board(board,m1,player)
            possible_second_moves = legal_move(temp_board,dice[0], player)
            for m2 in possible_second_moves:
                moves.append(np.array([m1,m2]))
                boards.append(update_board(temp_board,m2,player))
            
    # if there's no pair of moves available, allow one move:
    if len(moves)==0: 
        # first dice:
        possible_first_moves = legal_move(board, dice[0], player)
        for m in possible_first_moves:
            moves.append(np.array([m]))
            boards.append(update_board(temp_board,m,player))
            
        # second dice:
        if dice[0] != dice[1]:
            possible_first_moves = legal_move(board, dice[1], player)
            for m in possible_first_moves:
                moves.append(np.array([m]))
                boards.append(update_board(temp_board,m,player))
            
    return moves, boards 

def is_legal_move(move,board_copy,dice,player,i):
    if len(move)==0: 
        return True
    global possible_moves
    possible_moves, possible_boards = legal_moves(board_copy, dice, player)
    legit_move = np.array([np.array((possible_move == move)).all() for possible_move in possible_moves]).any()
    if not legit_move:
        print("Game forfeited. Player "+str(player)+" made an illegal move")
        return False
    return True



def valid_move(move,board_copy,dice,player,i):
    # pretty_print(board_copy)
    # print("dice", dice)
    # print(move)
    # print(type(move))
    return True
    
def play_a_game(player1, player2, train=False, train_config=None, commentary = False):
    board = init_board() # initialize the board
    player = np.random.randint(2)*2-1 # which player begins?
    
    # play on
    while not game_over(board) and not check_for_error(board):
        if commentary: print("lets go player ",player)
        
        # roll dice
        dice = roll_dice()
        if commentary: print("rolled dices:", dice)
            
        # make a move (2 moves if the same number appears on the dice)
        for i in range(1+int(dice[0] == dice[1])):
            board_copy = np.copy(board) 
            
            if train:
                if player == 1:
                    move = player1.action(board_copy,dice,player,i,train=train,train_config=train_config) 
                elif player == -1:
                    move = player2.action(board_copy,dice,player,i,train=train,train_config=train_config)
            else:
                if player == 1:
                    move = player1.action(board_copy,dice,player,i) 
                elif player == -1:
                    move = player2.action(board_copy,dice,player,i)

            # check if the move is valid
            if not is_legal_move(move,board_copy,dice,player,i):
                print("Game forfeited. Player "+str(player)+" made an illegal move")
                return -1*player
                
            # update the board
            if len(move) != 0:
                for m in move:
                    board = update_board(board, m, player)
                                
            # give status after every move:         
            if commentary: 
                print("move from player",player,":")
                pretty_print(board)
                
        # players take turns 
        player = -player

        # if game_over(board) and player == -1:
        #     print("final move, dice and board:")
        #     print(move)
        #     print(dice)
        #     pretty_print(board)
        #     exit()

            
    # return the winner
    return -1*player, board

def plot_perf(performance):
    plt.plot(performance)
    plt.show()
    return

def log_status(g, wins, performance, nEpochs):
    if g == 0:
        return performance
    print("game number", g)
    win_rate = wins/nEpochs
    print("win rate:", win_rate)
    performance.append(win_rate)
    return performance     
# board[25]= 1
# board[26] = 2
# print(board)
# print(board[25])
# print(board[26])    