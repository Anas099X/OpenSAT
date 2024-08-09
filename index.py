from fasthtml import FastHTML
from fasthtml.common import *
from pages.explore import math_objects

app = FastHTMLWithLiveReload()

Defaults = (Meta(name="viewport", content="width=device-width"),
                Title("OpenSAT"),
                Style(open("css/index.css").read()))


@app.get("/")
def home():
    return (
        Html(
            Head(
                Defaults
            ),
            Body(
                Header(
                    A(
                        Span("🎓", style="font-size:1.8rem;"),
                        H1("OpenSAT", style="color: #fc9d9a; font-weight: 700;"),
                        Class="logo", href="/",style="text-decoration: none"
                    ),
                    Nav(
                        A("Tutors", href="/tutors", Class="btn btn-primary"),
                        A("Github", href="https://github.com/Anas099X/OpenSAT", Class="btn btn-secondary"),
                        Class="nav"
                    ),
                    Class="header"
                ),
                Main(
                    Div(
                        Span("🎓", style=" display: flex; font-size: 5rem; margin-bottom: 20px; justify-content: center;"),
                        H2("Question Bank with ", Span("Endless", Class="text-primary-500 decoration-wavy"), " Possibilities",
                           style="font-size: 2.25rem; font-weight: 700; text-align: center; margin-bottom: 20px; color: #333;"),
                        P("OpenSAT, a free and open-source SAT question bank. "
                          "Dive into a massive pool of SAT practice problems, "
                          "constantly growing thanks to a dedicated community of contributors.",
                          style="text-align: center; max-width: 36rem; margin: 0 auto 20px; color: #555; font-size: 1rem;"),
                        Div(
                            A("Explore", href="/explore", Class="btn btn-primary"),
                            A("Contribute", href="https://github.com/Anas099X/OpenSAT", Class="btn btn-secondary"),
                            A("JSON Database", href="https://api.jsonsilo.com/public/942c3c3b-3a0c-4be3-81c2-12029def19f5", 
                          Class="btn btn-secondary"),
                            style="display: flex; justify-content: center; gap: 15px;"
                            
                        ),
                        Class="container"
                    )
                )
            )
        )
    )


@app.get("/explore")
def explore():
 return (
    
       Html(
            Head(
                Defaults
            ),
            Body(
                Header(
                    A(
                        Span("🎓", style="font-size:1.8rem;"),
                        H1("OpenSAT", style="color: #fc9d9a; font-weight: 700;"),
                        Class="logo",href='/',style="text-decoration: none"
                    ),
                    Nav(
                        A("Tutors", href="/tutors", Class="btn btn-primary"),
                        A("Github", href="https://github.com/Anas099X/OpenSAT", Class="btn btn-secondary"),
                        Class="nav"
                    ),
                    Class="header"
                ),
                Main(

                    Div(
                         
                        *[A(Div("📚",Class="icon"),Div(x['id'],Class="question-number"),Div(x['domain'], Class="category"),Class="card") for x in math_objects]

                        ,Class="list-content"
                   )
                   ,Style="display:flex;"
                )
        )
) 


 )

serve()