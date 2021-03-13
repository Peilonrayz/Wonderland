from .. import cache


def get_post_title(id):
    return cache.get(str(id), cache.title)
