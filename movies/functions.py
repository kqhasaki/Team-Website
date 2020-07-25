def is_similar(user1, user2):
    # determine the similarity between two users
    preference1 = [
        movie.id for movie in user1.moviepreference.favorite_movie.all()
    ]
    preference2 = [
        movie.id for movie in user2.moviepreference.favorite_movie.all()
    ]

    outcome = False
    if compare_movie_list(preference1, preference2):
        outcome = True
    return outcome


def compare_movie_list(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    joint_set = set1.intersection(set2)
    return len(joint_set) >= .3 * min(len(list1), len(list2))
