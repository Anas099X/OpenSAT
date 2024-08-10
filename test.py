from fasthtml.common import *

app,rt = fast_app()

@rt('/')
def get(): return Div(P('Hello World!'), hx_get="/change"), Button("ss",hx_post='/change')

serve()

@rt('/change')
def post(): return P('Nice to be here!')