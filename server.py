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
    return redirect(url_for('room', room_code=room_code))

@app.route('/join_room', methods=['GET'])
def join_room_redirect():
    room_code = request.args.get('room_code')
    if not room_code or room_code not in rooms:
        return "Místnost neexistuje!", 404
    return redirect(url_for('room', room_code=room_code))

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

    room = rooms[room_code]
    return render_template(
        'room.html',
        room_code=room_code,
        players=room['players'],
        locations=locations,
        room=room  # 🔧 potřebné pro zobrazení tlačítka hosta
    )

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

    room['status'] = 'finished'  # ⬅️ klíčová změna!

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

# 🔧 Nová pomocná route pro automatické přesměrování po startu hry
@app.route('/room_status')
def room_status():
    room_code = request.args.get('room_code')
    if room_code not in rooms:
        return jsonify({'error': 'Room not found'}), 404
    return jsonify({
        'status': rooms[room_code]['status'],
        'paused': rooms[room_code]['paused']
    })

@app.route('/game_status')
def game_status():
    room_code = request.args.get('room_code')
    if room_code not in rooms:
        return jsonify({'error': 'Room not found'}), 404

    is_over = rooms[room_code]['status'] == 'finished'
    return jsonify({'game_over': is_over})

@app.route('/leave_room')
def leave_room():
    room_code = request.args.get('room_code')
    username = request.args.get('username')

    if room_code in rooms and username in rooms[room_code]['players']:
        rooms[room_code]['players'].remove(username)

        # pokud hráč byl hostitelem, předáme hostitelství dalšímu hráči
        if rooms[room_code]['host'] == username:
            if rooms[room_code]['players']:
                rooms[room_code]['host'] = rooms[room_code]['players'][0]
            else:
                rooms[room_code]['host'] = None

    return '', 204  # no content

@app.route('/update_timer', methods=['POST'])
def update_timer():
    data = request.get_json()
    room_code = data.get('room_code')
    seconds = data.get('seconds')

    if room_code in rooms:
        rooms[room_code]['timer'] = seconds
        return '', 204
    return 'Room not found', 404

@app.route('/player_list')
def player_list():
    room_code = request.args.get('room_code')
    if room_code not in rooms:
        return jsonify({'error': 'Room not found'}), 404
    return jsonify({'players': rooms[room_code]['players']})

if __name__ == '__main__':
    app.run(debug=True, port=5001)