from flask import render_template, redirect, url_for, flash, request, jsonify, session
from previsaoligas import app, database, bcrypt
from previsaoligas.forms import FormLogin, FormCriarConta
from previsaoligas.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required
from previsaoligas.database import df, homeData, awayData, last_results_text_home, last_results_text_away, ml_pred,\
    df_odds, tips_original_result
import json
import stripe 
from uuid import uuid4
from dotenv import load_dotenv
import os

load_dotenv()

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Create a dictionary to store the teams for each competition
    teams_dict = {}

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        comp = row["comp"]
        home = row["home"]
        away = row["away"]
        
        # Add home and away teams to the competition's list of teams
        if comp not in teams_dict:
            teams_dict[comp] = set()
        teams_dict[comp].add(home)
        teams_dict[comp].add(away)

    # Convert the sets to lists in the dictionary
    for comp, teams in teams_dict.items():
        teams_dict[comp] = sorted(list(teams))

    # Convert the home_teams_map to a JSON string
    teams_map_json = json.dumps(teams_dict)
    return render_template('home.html', teams_map_json=teams_map_json)

@app.route('/output', methods=['GET', 'POST'])
@login_required
def output():
    team1_data = request.json['team1_input']
    team2_data = request.json['team2_input']

    points_last_season = homeData(df, team1_data)['Points last season'][0]
    gf_rolling = homeData(df, team1_data).gf_rolling[0]
    ga_rolling = homeData(df, team1_data).ga_rolling[0]
    pont_rolling = homeData(df, team1_data).pont_rolling[0]
    last_results = last_results_text_home(team1_data, team2_data)

    points_last_season2 = awayData(df, team2_data)['Points last season'][0]
    gf_rolling2 = awayData(df, team2_data).gf_rolling[0]
    ga_rolling2 = awayData(df, team2_data).ga_rolling[0]
    pont_rolling2 = awayData(df, team2_data).pont_rolling[0]
    last_results2 = last_results_text_away(team1_data, team2_data)

    prediction = f'{(ml_pred(team1_data, team2_data)*100).round(1)}%'
    prediction2 = f'{((1-(ml_pred(team1_data, team2_data)))*100).round(1)}%'

    response = {
        'points_last_season': float(points_last_season),
        'gf_rolling': int(gf_rolling),
        'ga_rolling': int(ga_rolling),
        'pont_rolling': int(pont_rolling),
        'points_last_season2': float(points_last_season2),
        'gf_rolling2': int(gf_rolling2),
        'ga_rolling2': int(ga_rolling2),
        'pont_rolling2': int(pont_rolling2),
        'last_results': last_results,
        'last_results2': last_results2,
        'prediction': prediction,
        'prediction2': prediction2
    }
    return jsonify(response)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/next_games')
@login_required
def next_games():
    return render_template('next_games.html', dataframe=df_odds)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos', 'alert-danger')
    return render_template('login.html', form_login=form_login)        

@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # Store the user's information in the session for later use
        session['user_info'] = {
            'username': form_criarconta.username.data,
            'email': form_criarconta.email.data,
            'senha': form_criarconta.senha.data
        }        


        # Redirect to the payment page
        return redirect(url_for('payment'))
    return render_template('criar_conta.html', form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/evolution')
@login_required
def evolution():
    return render_template('evolution.html', dataframe=tips_original_result)


@app.route('/output3', methods=['GET', 'POST'])
@login_required
def output3():
    filter_choice = request.json['filter_choice']
    inicial = 100
    multiplier_map = {
        'safest_bet': (20/100)*inicial,
        'safe_bet': (10/100)*inicial,
        'risky_bet': (5/100)*inicial
    }
    if filter_choice == 'all':
        atual = inicial + tips_original_result.apply(
            lambda row: multiplier_map[row['bet_type']] * row['Winning_bet'] - multiplier_map[row['bet_type']] if row['bet_right'] == 1 else multiplier_map[row['bet_type']]*-1, axis=1).sum()
        lucro = atual - inicial
        lucro_perc = (lucro/inicial)*100

    else:
        atual = inicial + tips_original_result[tips_original_result['bet_type'] == filter_choice].apply(
            lambda row: multiplier_map[row['bet_type']] * row['Winning_bet'] - multiplier_map[row['bet_type']] if row['bet_right'] == 1 else multiplier_map[row['bet_type']]*-1, axis=1).sum()
        lucro = atual - inicial
        lucro_perc = (lucro/inicial)*100


    # Process the filter choice

    if filter_choice == 'all':
        filtered_data = tips_original_result
    else:
        filtered_data = tips_original_result[tips_original_result['bet_type'] == filter_choice]

    def calculate_profit(group):
        profits = []
        for _, row in group.iterrows():
            bet_type = row['bet_type']
            multiplier = multiplier_map.get(bet_type, 0)
            if row['bet_right'] == 1:
                profit = multiplier * row['Winning_bet'] - multiplier
            else:
                profit = -1 * multiplier
            profits.append(profit)
        return sum(profits)

    # Group the DataFrame by 'Date' and calculate the profit for each group

    grouped_profit = filtered_data.groupby('Date').apply(calculate_profit).reset_index(name='Profit')

    grouped_profit['cum_profit'] = grouped_profit['Profit'].cumsum()

    # Convert the 'Date' column to a string representation to make it JSON serializable
    grouped_profit['Date'] = grouped_profit['Date'].astype(str)

    # Assuming 'Date' and 'bet_right' are columns in the DataFrame
    chart_labels = grouped_profit['Date'].tolist()

    # Get the count of correct and incorrect bets for each date (y-axis values)
    chart_profit = grouped_profit['cum_profit'].tolist()

    chart_data = {'labels': chart_labels,
                  'chart_profit': chart_profit,
                  }

    print(chart_data)

    response = {
        'inicial': f'R$ {round(inicial, 1)}',
        'atual': f'R$ {round(atual, 1)}',
        'lucro': f'R$ {round(lucro, 1)}',
        'lucro_perc': f'{round(lucro_perc, 1)}%',
        'chart_data': chart_data,  # Convert the DataFrame to a list of dictionaries
    }

    return jsonify(response)


@app.route('/performance')
@login_required
def performance():
    return render_template('performance.html', dataframe=tips_original_result)


@app.route('/output2', methods=['GET', 'POST'])
@login_required
def output2():
    filter_choice = request.json['filter_choice']
    if filter_choice == 'all':
        corretas_all = len(tips_original_result[(tips_original_result["bet_right"] == 1)])
        incorretas_all = len(tips_original_result[(tips_original_result["bet_right"] == 0)])
        precision = f'{round((corretas_all / (corretas_all + incorretas_all)) * 100, 1)}%'
        bet_media_all = round(tips_original_result['Winning_bet'].mean(), 2)
        response = {'corretas': corretas_all,
                    'incorretas': incorretas_all,
                    'precision': str(precision),
                    'bet_media': float(bet_media_all)}
    else:
        corretas = len(tips_original_result[(tips_original_result["bet_right"] == 1) & (tips_original_result["bet_type"] == filter_choice)])
        incorretas = len(tips_original_result[(tips_original_result["bet_right"] == 0) & (tips_original_result["bet_type"] == filter_choice)])
        precision = f'{round((corretas / (corretas + incorretas)) * 100, 1)}%'
        bet_media = round(tips_original_result[tips_original_result["bet_type"] == filter_choice]['Winning_bet'].mean(),2)
        response = {'corretas': corretas,
                    'incorretas': incorretas,
                    'precision': str(precision),
                    'bet_media': float(bet_media)}

    # Process the filter choice

    if filter_choice == 'all':
        filtered_data = tips_original_result
    else:
        filtered_data = tips_original_result[tips_original_result['bet_type'] == filter_choice]

    # Group data by date and calculate count of correct and incorrect bets
    grouped_data = filtered_data.groupby('Date')['bet_right'].value_counts().unstack(fill_value=0)

    # Assuming 'Date' and 'bet_right' are columns in the DataFrame
    chart_labels = grouped_data.index.tolist()

    # Get the count of correct and incorrect bets for each date (y-axis values)
    chart_bet_right = grouped_data[1].tolist()  # 1 represents correct bets
    chart_bet_wrong = grouped_data[0].tolist()  # 0 represents incorrect bets

    chart_data = {'labels': chart_labels,
                  'bet_right': chart_bet_right,
                  'bet_wrong': chart_bet_wrong,
                  }

    response['chart_data'] = chart_data

    return jsonify(response)

stripe.api_key = os.getenv('stripe_api_key')


@app.route('/payment_success')
def payment_success():
    try:
        # Retrieve user information from the session
        user_info = session.get('user_info') 

        if user_info:
            senha_cript = bcrypt.generate_password_hash(user_info['senha']).decode("utf-8")
            usuario = Usuario(username=user_info['username'], email=user_info['email'], senha=senha_cript)
            database.session.add(usuario)
            database.session.commit()
            flash(f'Conta criada para o e-mail: {user_info["email"]}', 'alert-success')
            session.pop('user_info')  # Clear user information from the session
        else:
            flash('Payment was successful, but user information is missing.', 'alert-danger')
    except Exception as e:
        flash('An error occurred while processing payment: ' + str(e), 'alert-danger')

    return render_template('payment_success.html')


@app.route("/create_checkout_session", methods=["POST"])
def create_checkout_session():
    # Get the price ID from the request (you can pass it as a parameter)
    price_id = request.json["price_id"]

    # Determine the cancel URL based on whether the app is running locally or on the live website
    if request.host.startswith("127.0.0.1"):
        cancel_url = "http://127.0.0.1:5000/criar_conta"
        success_url = "http://127.0.0.1:5000/payment_success"
    else:
        cancel_url = "https://soccerpred.up.railway.app/criar_conta"
        success_url = "https://soccerpred.up.railway.app/payment_success"

    # Create a Checkout session
    stripe_session = stripe.checkout.Session.create(
        mode="subscription",
        success_url=success_url,
        cancel_url= cancel_url,
        line_items=[{"price": price_id, "quantity": 1}],
        subscription_data={
            "trial_settings": {"end_behavior": {"missing_payment_method": "cancel"}},
            "trial_period_days": 15,
        },
        payment_method_types=["card"],
    )

    # Store the session ID in the user's session
    session['stripe_session_id'] = stripe_session.id

    return jsonify({"sessionId": stripe_session.id})



@app.route('/payment')
def payment():
    return render_template('subscription.html', stripe_public_key=os.getenv('stripe_public_key'))