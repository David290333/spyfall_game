from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
import string
from locations import locations

app = Flask(__name__)
app.secret_key = "tajny-klic"
rooms = {}

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def create_empty_room():
    return {
        "players": [],
        "location": None,
        "spy": None,
        "status": "not_started",
        "timer": 300,
        "player_roles": {},
        "host": None,
        "paused": False
    }

def assign_roles(players, location, spy_name):
    return {player: "spy" if player == spy_name else "not_spy" for player in players}

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
    return jsonify({"room_code": room_code})

@app.route('/join_room_post', methods=['POST'])
def join_room_post():
    room_code = request.form['room_code']
    username = request.form['username']

    if room_code not in rooms:
        return "Místnost neexistuje!", 404

    players = rooms[room_code]['players']
    new_username = username
    counter = 2
    while new_username in players:
        new_username = f"{username} ({counter})"
        counter += 1

    players.append(new_username)
    if rooms[room_code]['host'] is None:
        rooms[room_code]['host'] = new_username

    session['username'] = new_username
    session['room_code'] = room_code

    return redirect(url_for('room', room_code=room_code))

@app.route('/room')
def room():
    room_code = request.args.get('room_code')
    if room_code not in rooms:
        return "Místnost neexistuje!", 404
    players = rooms[room_code]['players']
    return render_template('room.html', room_code=room_code, players=players, locations=locations)

@app.route('/start_game', methods=['POST'])
def start_game():
    room_code = request.form['room_code']
    timer_minutes = int(request.form.get('timer', 5))
    timer_seconds = timer_minutes * 60

    if room_code not in rooms:
        return "Místnost neexistuje!", 404

    room = rooms[room_code]
    username = session.get('username')
    if room['host'] != username:
        return "Pouze host může spustit hru.", 403

    if room['status'] == 'in_progress':
        return "Hra už běží.", 400

    players = room['players']
    if not players:
        return "Žádní hráči.", 400

    location = random.choice(locations)
    spy = random.choice(players)
    room.update({
        'status': 'in_progress',
        'location': location,
        'spy': spy,
        'timer': timer_seconds,
        'player_roles': assign_roles(players, location, spy),
        'paused': False
    })

    return redirect(url_for('game', room_code=room_code, username=username))

@app.route('/pause_game', methods=['POST'])
def pause_game():
    room_code = request.form['room_code']
    username = session.get('username')

    if room_code not in rooms:
        return "Místnost neexistuje!", 404

    room = rooms[room_code]
    if room['host'] != username:
        return "Pouze host může pozastavit hru.", 403

    room['paused'] = not room['paused']
    return redirect(url_for('game', room_code=room_code, username=username))

@app.route('/end_game', methods=['POST'])
def end_game():
    room_code = request.form['room_code']
    username = session.get('username')

    if room_code not in rooms:
        return "Místnost neexistuje!", 404

    room = rooms[room_code]
    if room['host'] != username:
        return "Pouze host může ukončit hru.", 403

    return redirect(url_for('game_over', room_code=room_code))

@app.route('/game')
def game():
    room_code = request.args.get('room_code')
    username = request.args.get('username')

    if room_code not in rooms or username not in rooms[room_code]['players']:
        return "Neplatný přístup.", 400

    room = rooms[room_code]
    role = room['player_roles'].get(username)
    if not role:
        return redirect(url_for('room', room_code=room_code))

    is_spy = role == "spy"
    location = None if is_spy else room['location']

    return render_template('game.html',
        room_code=room_code,
        is_spy=is_spy,
        location=location,
        room=room,
        all_locations=locations
    )

@app.route('/game_over')
def game_over():
    room_code = request.args.get('room_code')
    if room_code not in rooms:
        return "Místnost neexistuje!", 404
    return render_template('game_over.html',
        room_code=room_code,
        spy=rooms[room_code]['spy'],
        location=rooms[room_code]['location'])

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
    room = rooms[room_code]
    room.update({
        'status': 'not_started',
        'location': None,
        'spy': None,
        'player_roles': {},
        'paused': False
    })
    return redirect(url_for('room', room_code=room_code))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
