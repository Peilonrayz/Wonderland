from .. import cache


def get_post_title(id):
    return cache.PostFileCache.from_file(cache.title)[str(id)]
