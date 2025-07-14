from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from fastapi import Request, Response
from uuid import uuid4

def replace_query_params(url: str, **params) -> str:
    parsed_url = urlparse(url)
    query = parse_qs(parsed_url.query)
    query.update({k: [str(v)] for k, v in params.items()})
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed_url._replace(query=new_query))


SESSION_COOKIE_NAME = "session667"

def get_or_create_session_id(request: Request, response: Response) -> str:
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if not session_id:
        session_id = str(uuid4())
        response.set_cookie(SESSION_COOKIE_NAME, session_id, max_age=60*60*24*30)  # 30 дней
    return session_id
