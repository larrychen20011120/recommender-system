import os
from collections import Counter
import argparse
import pickle

def create_new_usermap(useless_users, user_num):
    useless_users = list(sorted(useless_users))
    new_usermap = [user for user in range(user_num+1)]
    for useless_user in useless_users:
        for idx in range(useless_user, user_num+1):
            new_usermap[idx] -= 1
    print(f"Create the map! Totally {max(new_usermap)} users")
    return new_usermap

def general_process(dir, filename):
    # process the user whose number of interactions < 3
    user_list, item_list, score_list = [], [], []
    with open(os.path.join(dir, filename), "r") as f:
        for line in f.readlines():
            line = line.rstrip().split("\t")
            user, item, score = int(line[0]), int(line[1]), int(line[2])
            user_list.append(user)
            item_list.append(item)
            score_list.append(score)
    user_count_dict = dict( Counter(user_list) )
    useless_users = list(filter(
        lambda (user, cnt): cnt < 3, user_count_dict.items()
    ))
    user_num = max(user_list) - len(useless_users)
    new_usermap = create_new_usermap(useless_users, user_num)
    print(f"Those users' number of interactions less than 3: {useless_users}")
    filter_interaction = {
        "remain_user_number": user_num,
        "remain_item_number": max(item_list),
        "new_usermap": new_usermap,
        "score": []
    }
    for user, item, score in zip(user_list, item_list, score_list):
        if user not in useless_users:
            filter_interaction["score"].append(
                (user, item, score)
            )
    path = os.path.join(dir, "filter_interaction.pkl")
    print(f"Store the result to \"{filter_interaction}\"...")
    with open(path, "wb") as f:
        pickle.dump(filter_interaction, f)

def movielens_process(dir):
    filename = "user_movie.dat"
    general_process(dir, filename)

def yelp_process(dir):
    filename = "user_business.dat"
    general_process(dir, filename)

def douban_process(dir):
    filename = "user_book.dat"
    general_process(dir, filename)


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
