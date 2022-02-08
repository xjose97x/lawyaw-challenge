def get_next_position(direction, last_position):
    return {
        'r': (last_position[0], last_position[1] + 1),
        'l': (last_position[0], last_position[1] - 1),
        'u': (last_position[0] - 1, last_position[1]),
        'd': (last_position[0] + 1, last_position[1]),
    }[direction]

def player_died(matrix, next_position):
    # check out of bounds
    if next_position[0] < 0 or next_position[0] >= 10 or next_position[1] < 0 or next_position[1] >= 10:
        return True
    if matrix[next_position[0]][next_position[1]] in ('1l', '2l'):
        return True
    return False

def determine_winner(p1_moves, p2_moves):
    matrix = [[0 for i  in range(10)] for i in range(10)]
    matrix[0][0] = '1l'
    matrix[9][9] = '2l'
    last_position_p1 = (0,0)
    last_position_p2 = (9,9)
    for p1_direction, p2_direction in zip(p1_moves, p2_moves):
        #P1
        next_position = get_next_position(p1_direction, last_position_p1)
        player1_died = player_died(matrix, next_position)
        last_position_p1 = next_position
        if not player1_died:
            matrix[next_position[0]][next_position[1]] = '1l'
        #P2
        next_position = get_next_position(p2_direction, last_position_p2)
        player2_died = player_died(matrix, next_position)
        last_position_p2 = next_position
        if not player2_died:
            matrix[next_position[0]][next_position[1]] = '2l'
        #Decide if game continues or not
        if last_position_p1 == last_position_p2 or (player1_died and player2_died):
            return 0 
        if player1_died:
            return 2
        if player2_died:
            return 1
    return 0

# player 2 should win (player 1 runs into his/her own path)
def test_self_collision():
    player1 = ['r', 'd', 'd', 'r', 'r', 'r', 'l', 'l', 'l', 'd', 'd', 'd', 'l', 'd', 'd', 'd', 'd', 'r']
    player2 = ['u', 'l', 'l', 'u', 'l', 'l', 'u', 'l', 'l', 'd', 'd', 'l', 'l', 'u', 'u', 'r', 'u', 'l']
    assert determine_winner(player1, player2) == 2
 
# draw (both eliminated on same turn)
def test_double_death():
    player1 = ['d', 'd', 'r', 'r', 'r', 'u', 'r', 'd', 'd', 'd', 'd', 'l', 'd', 'r', 'r', 'r', 'u', 'u']
    player2 = ['l', 'l', 'l', 'u', 'u', 'l', 'u', 'u', 'u', 'r', 'r', 'u', 'l', 'l', 'l', 'l', 'u', 'r']
    assert determine_winner(player1, player2) == 0
 
# draw (both alive)
def test_double_alive():
    player1 = ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'r', 'u', 'u', 'u', 'u', 'u']
    player2 = ['u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'l', 'l', 'l', 'l', 'l', 'd', 'd', 'd', 'd', 'd']
    assert determine_winner(player1, player2) == 0
 
# draw (same space on same turn)
def test_same_space():
    player1 = ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r', 'r', 'u', 'u', 'u', 'u', 'u']
    player2 = ['u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'l', 'l', 'l', 'l', 'l', 'd', 'd', 'd', 'r', 'd']
    assert determine_winner(player1, player2) == 0
 
# draw (eliminated on 5th round)
def test_double_collision():
    player1 = ['d', 'd', 'd', 'd', 'u', 'u', 'r', 'd', 'd', 'd', 'd', 'l', 'd', 'r', 'r', 'r', 'u', 'u']
    player2 = ['l', 'l', 'l', 'l', 'r', 'l', 'u', 'u', 'u', 'r', 'r', 'u', 'l', 'l', 'l', 'l', 'u', 'r']
    assert determine_winner(player1, player2) == 0
 
# player 2 should win
def test_p2_win():
    player1 = ['r', 'd', 'd', 'r', 'r', 'r', 'd', 'r', 'r', 'd', 'd', 'd', 'l', 'd', 'd', 'd', 'd', 'r']
    player2 = ['u', 'l', 'l', 'u', 'l', 'l', 'u', 'l', 'l', 'd', 'd', 'l', 'l', 'u', 'u', 'r', 'u', 'l']
    assert determine_winner(player1, player2) == 2
    
# player 1 should win
def test_p1_win():
    player1 = ['r', 'd', 'd', 'r', 'r', 'r', 'd', 'r', 'r', 'd', 'd', 'd', 'r', 'u', 'u', 'u', 'd', 'r']
    player2 = ['u', 'l', 'l', 'u', 'l', 'l', 'u', 'u', 'u', 'u', 'u', 'l', 'l', 'u', 'u', 'r', 'u', 'l']
    assert determine_winner(player1, player2) == 1
 
# player 2 should win (player 1 goes out of bounds)
def test_p2_win_out_of_bounds():
    player1 = ['r', 'd', 'r', 'r', 'u', 'r', 'u', 'u', 'u', 'd', 'd', 'd', 'r', 'u', 'u', 'u', 'd', 'r']
    player2 = ['u', 'l', 'l', 'u', 'l', 'l', 'u', 'l', 'l', 'd', 'd', 'l', 'l', 'u', 'u', 'r', 'u', 'l']
    assert determine_winner(player1, player2) == 2