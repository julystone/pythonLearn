# encoding: utf-8
# Upper Confidence Bound

import math

import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('../config_files/Ads_CTR_Optimisation.csv')


def ucb():
    # Implementing UCB
    ads_selected = []
    N = 10000
    d = 10
    numbers_of_selections = [0] * d
    sums_of_rewards = [0] * d
    total_reward = 0
    for n in range(0, N):
        ad = 0
        max_upper_bound = 0
        for i in range(0, d):
            if (numbers_of_selections[i] > 0):
                average_reward = sums_of_rewards[i] / numbers_of_selections[i]
                delta_i = math.sqrt(3 / 2 * math.log(n + 1) / numbers_of_selections[i])
                upper_bound = average_reward + delta_i
            else:
                upper_bound = 1e400
            if (upper_bound > max_upper_bound):
                max_upper_bound = upper_bound
                ad = i
        ads_selected.append(ad)
        numbers_of_selections[ad] = numbers_of_selections[ad] + 1
        reward = dataset.values[n, ad]
        sums_of_rewards[ad] = sums_of_rewards[ad] + reward
        total_reward = total_reward + reward

        # Visualising the results

    plt.hist(ads_selected)
    plt.title('Histogram of ads selections')
    plt.xlabel('Ads')
    plt.ylabel('Number of times each ad was selected')
    plt.show()


def random_selection():
    import random
    N = 10000
    d = 10
    ads_selected = []
    total_reward = 0
    for n in range(0, N):
        ad = random.randrange(d)
        ads_selected.append(ad)
        reward = dataset.values[n, ad]
        total_reward = total_reward + reward

    # Visualising the results
    plt.hist(ads_selected)
    plt.title('Histogram of ads selections')
    plt.xlabel('Ads')
    plt.ylabel('Number of times each ad was selected')
    plt.show()


if __name__ == '__main__':
    ucb()