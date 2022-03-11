from flask import make_response, jsonify


def make_common_response(data, message='', error=False, status_code=200):
    """
    Make response for restful api
    :param data:
    :param message:
    :param error: True or False
    :param status_code:
    :return:
    """
    result = 'ok'
    if error:
        result = 'fail'

    response = {
        'result': result,
        'message': message,
        'data': data
    }

    return make_response(jsonify(response), status_code)


def paging_response(page, per_page, total):
    prev = None
    has_prev = False
    next = None
    has_next = False
    last, _ = divmod(total, per_page)
    last += 1

    if page > 1:
        prev = page - 1
        has_prev = True

    if total > (page * per_page):
        next = page + 1
        has_next = True

    paging = {
        "current": page,
        "per_page": per_page,
        "prev": prev,
        "has_prev": has_prev,
        "next": next,
        "has_next": has_next,
        "total": total,
        "first": 1,
        "last": last,
    }

    return paging
