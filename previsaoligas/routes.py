from flask import render_template, redirect, url_for, flash, request, jsonify
from previsaoligas import app, database, bcrypt
from previsaoligas.forms import FormLogin, FormCriarConta
from previsaoligas.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required
from previsaoligas.database import df, homeData, awayData, last_results_text_home, last_results_text_away, ml_pred,\
    df_odds, tips_original_result
import json


@app.route('/', methods=['GET', 'POST'])
#@login_required
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
#@login_required
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

@app.route('/next_games')
#@login_required
def next_games():
    return render_template('next_games.html', dataframe=df_odds)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
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
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data
                          , senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
#@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/evolution')
#@login_required
def evolution():
    return render_template('evolution.html', dataframe=tips_original_result)


@app.route('/output3', methods=['GET', 'POST'])
#@login_required
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
#@login_required
def performance():
    return render_template('performance.html', dataframe=tips_original_result)


@app.route('/output2', methods=['GET', 'POST'])
#@login_required
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
