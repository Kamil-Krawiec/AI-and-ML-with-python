import pandas as pd
import matplotlib.pyplot as plt

def alpha_beta():
    df = pd.read_csv('test.csv')

    for index, row in df.iterrows():
        y_p1 = list(row['p1_eval_times'][1:len(row['p1_eval_times']) - 1].split(','))
        y_p1 = [float(x) for x in y_p1 if x != '']
        x_p1 = [x for x in range(1, len(y_p1) + 1)]

        y_p2 = list(row['p2_eval_times'][1:len(row['p2_eval_times']) - 1].split(','))
        y_p2 = [float(x) for x in y_p2 if x != '']
        x_p2 = [x for x in range(1, len(y_p2) + 1)]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(x_p1, y_p1, color='red', alpha=0.5, label=f"P1 heuristic{row['heuristic_p1']}")
        ax.set_title(f"Time of eval in rounds depth={row['minimax_depth_p2']}  WON {row['game_result']}", fontsize=18)
        ax.set_xlabel('Round', fontsize=14)
        ax.set_ylabel('Time [s]', fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12)

        ax.scatter(x_p2, y_p2, color='blue', alpha=0.5, label=f"P2 heuristic{row['heuristic_p2']}")
        ax.legend(loc='upper right', fontsize=12, frameon=True, framealpha=0.9)

        ax.grid(True)
        plt.show()


def miniaxi():
    df = pd.read_csv('test_alpha_beta.csv')

    for x in range(len(df)//2 ):
        game = df[df['game_id']==x]
        alpha_beta = game[game['alpha-beta'] == True]
        casual = game[game['alpha-beta'] == False]

        alpha_beta_str = list(alpha_beta['p1_eval_times'])[0]
        casual_str = list(casual['p1_eval_times'])[0]


        y_ab = alpha_beta_str[1:len(alpha_beta_str)-1].split(',')
        y_ab = [float(x) for x in y_ab if x!='']
        x_ab = [x for x in range(1, len(y_ab) + 1)]


        y_c = casual_str[1:len(casual_str)-1].split(',')
        y_c = [float(x) for x in y_c if x!='']
        x_c = [x for x in range(1, len(y_c) + 1)]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(x_ab, y_ab, color='red', alpha=0.5, label=f"Heuristic {df['heuristic_p1'][2*x+1]} alfa-beta mm")
        ax.set_title(f"Time of eval in rounds depth={df['minimax_depth_p2'][2*x+1]}  WON {df['game_result'][2*x+1]}", fontsize=18)

        ax.set_xlabel('Round', fontsize=14)
        ax.set_ylabel('Time [s]', fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12)

        ax.scatter(x_c, y_c, color='blue', alpha=0.5, label=f"Heuristic {df['heuristic_p1'][2*x+1]} casual mm")
        ax.legend(loc='upper right', fontsize=12, frameon=True, framealpha=0.9)

        ax.grid(True)
        plt.show()


# miniaxi()
alpha_beta()