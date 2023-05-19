import os
from collections import Counter
import argparse
import pickle

def movielens_process(dir):
    # process the user whose number of interactions < 3
    user_list, movie_list, score_list = [], [], []
    with open(os.path.join(dir, "user_movie.dat"), "r") as f:
        for line in f.readlines():
            line = line.rstrip().split("\t")
            user, movie, score = int(line[0]), int(line[1]), int(line[2])
            user_list.append(user)
            movie_list.append(movie)
            score_list.append(score)
    user_count_dict = dict( Counter(user_list) )
    useless_users = list(filter(
        lambda (user, cnt): cnt < 3, user_count_dict.items()
    ))
    print(f"Those users' number of interactions less than 3: {useless_users}")
    filter_interaction = {
        "remain_user_number": max(user_list) - len(useless_users),
        "useless_users": useless_users,
        "score": []
    }
    for user, movie, score in zip(user_list, movie_list, score_list):
        if user not in useless_users:
            filter_interaction["score"].append(
                (user, movie, score)
            )
    path = os.path.join(dir, "filter_interaction.pkl")
    print(f"Store the result to \"{filter_interaction}\"...")
    with open(path, "wb") as f:
        pickle.dump(filter_interaction, f)

def yelp_process(dir):
    # process the user whose number of interactions < 3
    user_list, business_list, score_list = [], [], []
    with open(os.path.join(dir, "user_business.dat"), "r") as f:
        for line in f.readlines():
            line = line.rstrip().split("\t")
            user, business, score = int(line[0]), int(line[1]), int(line[2])
            user_list.append(user)
            business_list.append(business)
            score_list.append(score)
    user_count_dict = dict( Counter(user_list) )
    useless_users = list(filter(
        lambda (user, cnt): cnt < 3, user_count_dict.items()
    ))
    print(f"Those users' number of interactions less than 3: {useless_users}")
    filter_interaction = {
        "remain_user_number": max(user_list) - len(useless_users),
        "useless_users": useless_users,
        "score": []
    }
    for user, business, score in zip(user_list, business_list, score_list):
        if user not in useless_users:
            filter_interaction["score"].append(
                (user, business, score)
            )
    path = os.path.join(dir, "filter_interaction.pkl")
    print(f"Store the result to \"{filter_interaction}\"...")
    with open(path, "wb") as f:
        pickle.dump(filter_interaction, f)

def douban_process(dir):
    # process the user whose number of interactions < 3
    user_list, book_list, score_list = [], [], []
    with open(os.path.join(dir, "user_book.dat"), "r") as f:
        for line in f.readlines():
            line = line.rstrip().split("\t")
            user, book, score = int(line[0]), int(line[1]), int(line[2])
            user_list.append(user)
            book_list.append(book)
            score_list.append(score)
    user_count_dict = dict( Counter(user_list) )
    useless_users = list(filter(
        lambda (user, cnt): cnt < 3, user_count_dict.items()
    ))
    print(f"Those users' number of interactions less than 3: {useless_users}")
    filter_interaction = {
        "remain_user_number": max(user_list) - len(useless_users),
        "useless_users": useless_users,
        "score": []
    }
    for user, book, score in zip(user_list, book_list, score_list):
        if user not in useless_users:
            filter_interaction["score"].append(
                (user, book, score)
            )
    path = os.path.join(dir, "filter_interaction.pkl")
    print(f"Store the result to \"{filter_interaction}\"...")
    with open(path, "wb") as f:
        pickle.dump(filter_interaction, f)


if __name__ == "__main__":
    dataset_list = ['movielens', 'yelp', 'douban']
    process_list = [movielens_process, yelp_process, douban_process]
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--dir", type=str, required=True)
    args = parser.parse_args()
    idx = dataset_list.find(args.dataset)
    if idx == -1:
        print("Processing does not support that dataset!!")
    else:
        print(f"Start processing dataset: {dataset_list[idx]}")
        process_list[idx](args.dir)
