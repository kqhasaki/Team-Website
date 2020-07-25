def get_similarity(user1, user2):
    # determine the similarity between two users
    preference1 = [
        movie.id for movie in user1.moviepreference.favorite_movie.all()
    ]
    preference2 = [
        movie.id for movie in user2.moviepreference.favorite_movie.all()
    ]

    return compare_movie_list(preference1, preference2)


def compare_movie_list(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    joint_set = set1.intersection(set2)
    is_similar = len(joint_set) >= min(len(list1), len(list2)) * 0.5
    similarity = len(joint_set)
    return is_similar, similarity
