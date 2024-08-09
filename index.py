from fasthtml import FastHTML
from fasthtml.common import *
from pages.explore import question_objects

app,rt = fast_app()

Defaults = (Meta(name="viewport", content="width=device-width"),
            Script('''MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global'
  }
};'''),
            Script(src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"),
                Title("OpenSAT"),
                Style(open("css/index.css").read()))



def hide_switch(input):
   return not input




@rt("/")
def get():
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
                        Span("🎓", style="display: flex; font-size: 5rem; margin-bottom: 20px; justify-content: center;"),
                        H2("Question Bank with ", Span("Endless", Class="text-primary-500 decoration-wavy"), " Possibilities",
                           style="font-size: 2.25rem; font-weight: 700; text-align: center; margin-bottom: 20px; color: #333;"),
                        P("OpenSAT, a free and open-source SAT question bank. "
                          "Dive into a massive pool of SAT practice problems, "
                          "constantly growing thanks to a dedicated community of contributors.",
                          style="text-align: center; max-width: 36rem; margin: 0 auto 20px; color: #555; font-size: 1rem;"),
                        Div(
                            A("Explore", href="/explore/english", Class="btn btn-primary"),
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


@rt("/explore/{section}")
def get(section:str):
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
                       
                         A("English", href=f'/explore/english',Class="btn btn-secondary card", style="background-color: #fc9d9a; font-size:0.9em;"),
                         A("Math", href=f'/explore/math',Class="btn btn-secondary card", style="background-color: #fc9d9a; font-size:0.9em;"),
                        *[A(Div("📚",Class="icon"),Div(f'Question #{i}',Class="question-number"),Div(x['domain'], Class="category"),Class="card",href=f"/questions/{section}/{i}/True") for i, x in enumerate(question_objects(section))]

                        ,Class="list-content"
                   )
                   ,Style="display:flex;"
                )
        )
) 

)



@rt('/questions/{section}/{num}/{answer}')
def get(section:str,num:int,answer:bool):
   question_obj = question_objects(section)[num]
   return ( Html(
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
                         
                        H2(f"Question #{question_obj['id']}"),
                        P(question_obj['question'].get('paragraph', "")),
                        B(question_obj['question']['question'].replace('$','$')),
                        
                        Div(f"A. {question_obj['question']['choices']['A']}"),
                        Div(f"B. {question_obj['question']['choices']['B']}"),
                        Div(f"C. {question_obj['question']['choices']['C']}"),
                        Div(f"D. {question_obj['question']['choices']['D']}"),
                        Br(),
                        A("Reveal Answers", href=f'/questions/{section}/{num}/{hide_switch(answer)}',Class="btn btn-secondary", style="font-size:0.9em;"),
                        Div(
                        Br(),
                        B(f"Correct Answer is: {question_obj['question']['correct_answer']}"),
                        P(question_obj['question']['explanation']), 
                         hidden=bool(answer)
                        )

                        ,Class="container",style="max-width:80vh;"
                   )
                   ,Style="display:flex;"
                )
        )
) 
)

serve()