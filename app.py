from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = 'super_secret_jupiler_2026'

joueurs = {"BDX": {"jetons": 9999, "banni": False, "avert": ""}}
paris = []
annonce_globale = ""

matchs = [
    {"id": 0, "date": "Aujourd'hui", "heure": "23:00", "equipe_a": "Panama", "equipe_b": "Angleterre"},
    {"id": 1, "date": "Aujourd'hui", "heure": "23:00", "equipe_a": "Croatie", "equipe_b": "Ghana"},
    {"id": 2, "date": "Demain", "heure": "01:30", "equipe_a": "Rép. Démoc.", "equipe_b": "Ouzbékistan"},
    {"id": 3, "date": "Demain", "heure": "01:30", "equipe_a": "Colombie", "equipe_b": "Portugal"},
    {"id": 4, "date": "Demain", "heure": "04:00", "equipe_a": "Jordanie", "equipe_b": "Argentine"},
    {"id": 5, "date": "Demain", "heure": "04:00", "equipe_a": "Algérie", "equipe_b": "Autriche"},
    {"id": 6, "date": "Demain", "heure": "21:00", "equipe_a": "Afrique du Sud", "equipe_b": "Canada"},
    {"id": 7, "date": "lun. 29 juin", "heure": "19:00", "equipe_a": "Brésil", "equipe_b": "Japon"},
    {"id": 8, "date": "lun. 29 juin", "heure": "22:30", "equipe_a": "Allemagne", "equipe_b": "Paraguay"},
    {"id": 9, "date": "mar. 30 juin", "heure": "03:00", "equipe_a": "Pays-Bas", "equipe_b": "Maroc"},
    {"id": 10, "date": "mar. 30 juin", "heure": "19:00", "equipe_a": "Côte d'Ivoire", "equipe_b": "Norvège"},
    {"id": 11, "date": "mar. 30 juin", "heure": "23:00", "equipe_a": "France", "equipe_b": "Suède"},
    {"id": 12, "date": "jeu. 2 juil.", "heure": "02:00", "equipe_a": "Etats-Unis", "equipe_b": "Bosnie Herz."},
    {"id": 13, "date": "ven. 3 juil.", "heure": "20:00", "equipe_a": "Australie", "equipe_b": "Egypte"},
    {"id": 14, "date": "sam. 4 juil.", "heure": "00:00", "equipe_a": "Argentine", "equipe_b": "Cap Vert"}
]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pseudo = request.form.get('pseudo')
        session['user'] = pseudo
        if pseudo not in joueurs: joueurs[pseudo] = {"jetons": 100, "banni": False, "avert": ""}
        return redirect('/')
    return '<body style="background:#d40000; color:white; text-align:center; padding-top:50px;"><h1>CONNEXION</h1><form method="POST">Pseudo: <input name="pseudo"><button>Entrer</button></form></body>'

@app.route('/miser/<int:mid>', methods=['POST'])
def miser(mid):
    u = session.get('user')
    montant = int(request.form.get('montant', 0))
    equipe = request.form.get('equipe')
    if not u or joueurs[u]['jetons'] < montant or montant <= 0:
        return "<h1>Vous n'avez pas assez de Jupis !</h1><a href='/'>Retour</a>"
    joueurs[u]['jetons'] -= montant
    paris.append({'user': u, 'match_id': mid, 'equipe': equipe, 'montant': montant, 'termine': False})
    return redirect('/')

@app.route('/admin_action/<action>', methods=['POST'])
def admin_action(action):
    global annonce_globale
    if session.get('user') != "BDX": return "Accès refusé", 403
    pseudo = request.form.get('pseudo', '')
    val = request.form.get('valeur', '')
    if action == "jupis": joueurs[pseudo]['jetons'] += int(val)
    elif action == "ban": joueurs[pseudo]['banni'] = not joueurs[pseudo]['banni']
    elif action == "avert": joueurs[pseudo]['avert'] = val
    elif action == "annonce": annonce_globale = val
    elif action == "clear_annonce": annonce_globale = ""
    elif action == "valider":
        mid = int(request.form.get('match_id'))
        gagnant = request.form.get('equipe_gagnante')
        for p in paris:
            if p['match_id'] == mid:
                if p['equipe'] == gagnant: joueurs[p['user']]['jetons'] += (p['montant'] * 2)
                p['termine'] = True
    return redirect('/')

@app.route('/')
def index():
    if 'user' not in session: return redirect('/login')
    u = session['user']
    if joueurs[u]['banni']: return "<h1>Banni du site</h1>", 403
    return render_template('index.html', user=u, joueurs=joueurs, matchs=matchs, paris=paris, annonce=annonce_globale)

if __name__ == '__main__': app.run(debug=True)