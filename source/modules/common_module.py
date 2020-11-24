def parse_pages(query_params):
    """
    Return the value of pagination
    Parameters
    ----------
    query_params: dict
        Query parameters of request
    """
    if query_params.get('page', 0) == 0:
        return { 'page': 0, 'page_size': 0 }

    page = 0 if query_params.get('page') == '1' else int(query_params.get('page')) - 1
    page_size = int(query_params.get('page_size'))
    return { 'page': page, 'page_size': page_size }

def get_type_ordering_object(sort):
    """
    Return sort object
    Parameters
    ----------
    sort: str
        Property used to sort documents
    """
    is_ascending = '-' in sort
    property = sort.split('-').pop() if is_ascending else sort
    return { property: -1 if is_ascending else 1 }