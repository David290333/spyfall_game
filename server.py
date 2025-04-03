from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
import string
from locations import locations

app = Flask(__name__)
app.secret_key = "tajny-klic"
rooms = {}

# === Pomocné funkce ===

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def create_empty_room():
    return {
        "players": [],
        "location": None,
        "spy": None,
        "status": "not_started",
        "timer": 300,
        "player_roles": {}
    }

def assign_roles(players, location, spy_name):
    roles = {}
    for player in players:
        roles[player] = "spy" if player == spy_name else "not_spy"
    return roles

# === Různé stránky ===

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/create_room', methods=['POST'])
def handle_create_room():
    room_code = generate_room_code()
    rooms[room_code] = create_empty_room()
    return redirect(url_for('room', room_code=room_code))

@app.route('/join_room')
def join_room_form():
    room_code = request.args.get('room_code')
    if room_code not in rooms:
        return "Místnost neexistuje!", 404
    return redirect(url_for('room', room_code=room_code))

@app.route('/room')
def room():
    room_code = request.args.get('room_code')
    if not room_code or room_code not in rooms:
        return "Místnost neexistuje!", 404
    players = rooms[room_code]['players']
    return render_template('room.html', room_code=room_code, players=players, locations=locations)

@app.route('/join_room_post', methods=['POST'])
def join_room_post():
    room_code = request.form['room_code']
    username = request.form['username']

    if room_code not in rooms:
        return "Místnost neexistuje!", 404

    existing_players = rooms[room_code]['players']
    new_username = username
    counter = 2

    while new_username in existing_players:
        new_username = f"{username} ({counter})"
        counter += 1

    existing_players.append(new_username)
    session['username'] = new_username
    session['room_code'] = room_code

    return render_template(
        'room.html',
        room_code=room_code,
        players=rooms[room_code]['players'],
        locations=locations
    )

@app.route('/start_game', methods=['POST'])
def start_game():
    room_code = request.form['room_code']
    timer_minutes = int(request.form.get('timer', 5))
    timer_seconds = timer_minutes * 60
    if room_code not in rooms:
        return "Místnost neexistuje!", 404
    room = rooms[room_code]
    players = room['players']
    if not players:
        return "Nelze spustit hru bez hráčů.", 400
    location = random.choice(locations)
    spy = random.choice(players)
    room['status'] = 'in_progress'
    room['location'] = location
    room['spy'] = spy
    room['timer'] = timer_seconds
    room['player_roles'] = assign_roles(players, location, spy)
    current_username = session.get('username')
    return redirect(url_for('game', room_code=room_code, username=current_username))


@app.route('/game')
def game():
    room_code = request.args.get('room_code')
    username = request.args.get('username')
    if not room_code or room_code not in rooms:
        return "Místnost neexistuje!", 404
    if not username or username not in rooms[room_code]['players']:
        return "Neplatný hráč.", 400

    room = rooms[room_code]

    # Ošetření, zda má hráč roli
    if username not in room['player_roles']:
        return redirect(url_for('room', room_code=room_code))

    role = room['player_roles'][username]
    is_spy = role == "spy"
    location = None if is_spy else room['location']


    return render_template(
        'game.html',
        room_code=room_code,
        is_spy=is_spy,
        location=location,
        room=room,
        all_locations=locations
    )

@app.route('/game_over')
def game_over():
    room_code = request.args.get('room_code')
    if not room_code or room_code not in rooms:
        return "Místnost neexistuje!", 404
    spy = rooms[room_code]['spy']
    location = rooms[room_code]['location']
    return render_template('game_over.html', room_code=room_code, spy=spy, location=location)

@app.route('/game_over_json')
def game_over_json():
    room_code = request.args.get('room_code')
    if room_code not in rooms:
        return jsonify({'error': 'Room not found'}), 404

    room = rooms[room_code]
    return jsonify({
        'spy': room['spy'],
        'location': room['location']['name']
    })

@app.route('/restart_game', methods=['POST'])
def restart_game():
    room_code = request.form['room_code']
    if room_code not in rooms:
        return "Místnost neexistuje!", 404
    rooms[room_code]['status'] = 'not_started'
    rooms[room_code]['location'] = None
    rooms[room_code]['spy'] = None
    rooms[room_code]['player_roles'] = {}
    return redirect(url_for('room', room_code=room_code))

if __name__ == '__main__':
    app.run(debug=True, port=5001)