from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Game

import json
import random

# Home Page View
def home(request):
    games = Game.objects.all()  # Fetch all available games
    return render(request, 'connect_row/home.html', {'games': games})

# Load a specific game based on the game ID
def load_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # Reset locked rows count on page reload
    game.locked_rows_count = 0
    game.save()


    game.current_state = get_words_from_connections(game)
    game.save()

    context = {
        'game': game,
        'words': game.current_state,
        'range_list': range(4),
    }
    return render(request, 'connect_row/game.html', context)

# Handle locking the top row
def lock_top_row(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if game.locked_rows_count == 4:
        return JsonResponse({'success': True, 'message': "Congratulations! You've won the game!"})    

    top_row = game.current_state[0 + game.locked_rows_count]

    connections = [
            game.connection1,
            game.connection2,
            game.connection3,
            game.connection4
        ]

    for connection in connections:
        if set(top_row) == {connection.word1.word, connection.word2.word, connection.word3.word, connection.word4.word}:
            game.locked_rows_count += 1
            game.save()
            return JsonResponse({'success': True, 'difficulty': connection.difficulty, 'message': f"You found {connection.description}!"})
    
    return JsonResponse({'success': False})

def get_words_from_connections(game):
    words = []
    # Collect all words from the connections
    for connection in [game.connection1, game.connection2, game.connection3, game.connection4]:
        words.extend([connection.word1.word, connection.word2.word, connection.word3.word, connection.word4.word])
    
    # Shuffle the words to randomize their order
    random.shuffle(words)
    
    # Return the words split into 4 rows (assuming a 4x4 grid)
    return [words[i:i + 4] for i in range(0, len(words), 4)]


def connect_all(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    connections = [
        game.connection1,
        game.connection2,
        game.connection3,
        game.connection4
    ]
    
    all_rows_connected = True  # Assume all rows are connected initially

    # Check each row for a connection
    for row_index in range(len(game.current_state)):
        row = game.current_state[row_index]
        row_set = set(row)  # Create a set of the words in the current row
        # Check if the row matches any connection
        if not any(row_set == {connection.word1.word, connection.word2.word, connection.word3.word, connection.word4.word} for connection in connections):
            all_rows_connected = False
            break  # No need to check further if one row is not connected

    if all_rows_connected:
        game.locked_rows_count = 4
        game.save()
        return JsonResponse({'success': True, 'message': "Congratulations! You've won the game!"})
    
    return JsonResponse({'success': False, 'message': "Not all rows are connected."})



# Handle the game movement and shifting
def make_move(request, game_id):
    if request.method == 'POST':
        game = get_object_or_404(Game, id=game_id)
        data = json.loads(request.body)
        direction = data['direction']
        index = data['index']
        words = game.current_state  # Get the current state from the database
        
        if direction == 'up':
            shift_column_up(words, index, game.locked_rows_count)
        elif direction == 'down':
            shift_column_down(words, index, game.locked_rows_count)
        elif direction == 'left':
            shift_row_left(words, index)
        elif direction == 'right':
            shift_row_right(words, index)

        # Save the updated state
        game.current_state = words
        game.save()

        return JsonResponse({'success': True, 'words': words})
    return JsonResponse({'success': False})


# Movement functions
def shift_row_left(words, row_index):
    row = words[row_index]
    words[row_index] = row[1:] + [row[0]]  # Move the first element to the end

def shift_row_right(words, row_index):
    row = words[row_index]
    words[row_index] = [row[-1]] + row[:-1]  # Move the last element to the front

def shift_column_up(words, col_index, locked_rows_count):
    first_item = words[locked_rows_count][col_index]
    for i in range(locked_rows_count + 1, len(words)):
        words[i - 1][col_index] = words[i][col_index]
    words[-1][col_index] = first_item  # Move the first element to the bottom

def shift_column_down(words, col_index, locked_rows_count):
    last_item = words[-1][col_index]
    for i in range(len(words) - 1, locked_rows_count, -1):
        words[i][col_index] = words[i - 1][col_index]
    words[locked_rows_count][col_index] = last_item  # Move the last element to the top
