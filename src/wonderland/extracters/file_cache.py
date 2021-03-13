from .. import cache


def get_post_title(id):
    return cache.PostFileCache.from_file(cache.title)[str(id)]


def get_question_id(id):
    return cache.PostFileCache.from_file(cache.question_id)[str(id)]


def get_user_name(id):
    return cache.UserFileCache.from_file(cache.user_name)[str(id)]


def get_author_id(q_id, p_id):
    return cache.PostFileCache.from_file(cache.author_id(q_id, p_id))[str(p_id)]


def get_post_license(q_id, p_id):
    return cache.PostFileCache.from_file(cache.post_license(q_id, p_id))[str(p_id)]
