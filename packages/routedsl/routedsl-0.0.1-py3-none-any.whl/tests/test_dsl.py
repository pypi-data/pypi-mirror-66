from routedsl.dsl import *


def test_dsl():
    DefaultHandler = HANDLER | get_user_info

    routes = Routes() (
        GET / 'users' / ('user_id', User, "User identifier")
        | HEADERS | Headers
        | RETURNS | JSON[ User]
        | DefaultHandler
        | GUARDS | (Headers.content_type | IS | 'application/json'
                    )
        | DOCS | """Get a user profile in JSON format"""
    )(
        POST / 'users' / ('user_id', User)
        | HEADERS | Headers
        | PAYLOAD | JSON[ User]
        | RETURNS | OK [ JSON[ bool]]
        | HANDLER | update_user_info
    )

    routes = (routes / 'users' / ('user_id', User)) (
        POST / 'edit'
        | HEADERS | Headers
        | RETURNS | JSON[ User]
        | HANDLER | update_user_info
    )

    DefaultHeaders = HEADERS | Headers
    DefaultHandler = HANDLER | empty_handler

    DefaultEndpoint = GET / DefaultHeaders | DefaultHandler

    routes3 = Routes() | DefaultEndpoint

    print(routes)

    router, type_constructors = generate_router(routes)
    matched_map, route = router.mapper.routematch(url='/users/4', environ={})
    schema: HTTP = route._kargs['controller']
    print(matched_map)
    query_args = {name: schema.query_types[name][0](val) for name, val in matched_map.items()}
