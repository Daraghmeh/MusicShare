import operator


def find_top_ten(songsplayed):
    """
    ~ Creates organic playlist that stores top ten songs
    that players love which can be used whenever ~
    :param songsplayed:
    :return:
    """
    if len(songsplayed) <= 10:
        return songsplayed
    else:
        least_popular = 0  # least popular song of top_ten
        least_popular_key = None
        top_ten = dict()
        for key, value in songsplayed.items():
            if len(top_ten) <= 10:
                top_ten[key] = value
            elif value[2] > least_popular and len(top_ten) >= 10:
                del dict[least_popular_key]
                top_ten[key] = value
        return top_ten

def sort_top_ten(top_ten):
    """
    ~ Sorts the playlist based on popularity ~
    :param top_ten: Top ten songs in an array
    :return: A sorted playlst depending on the popularity of each song
    """
    sorted_playlist = sorted(top_ten.items(), key=operator.itemgetter(1))
    return sorted_playlist

def build_playlist(songsplayed):
    """
    ~ Builds the playlist to be reused ~
    :param songsplayed:
    :return:
    Uses the top ten method as well as sorting to build
    the reusable playlist
    """
    top_ten = find_top_ten(songsplayed)
    hot_playlist = sort_top_ten(top_ten)
    return hot_playlist
