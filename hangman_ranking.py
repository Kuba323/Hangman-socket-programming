def save_score(player_name, score):
    with open('scores.txt', 'a') as file:
        file.write(f'{player_name},{score}\n')

def get_scores():
    with open('scores.txt', 'r') as file:
        lines = file.readlines()
    scores = []
    for line in lines:
        player_name, score = line.strip().split(',')
        scores.append((player_name, int(score)))
    return scores

def print_ranking():
    scores = get_scores()
    send_scores = {}
    scores.sort(key=lambda x: x[1], reverse=True)
    for player_name, score in scores:
        send_scores[player_name] = score
        print(f'{player_name}: {score}')
    return  send_scores

