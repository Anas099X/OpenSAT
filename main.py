from fasthtml.common import *
from settings import *

app,rt = fast_app(debug=True)

Defaults = (Meta(name="viewport", content="width=device-width"),
            Title("OpenSAT"),
            Link(rel="icon",href="public/graduation-cap-solid.svg", sizes="any", type="image/svg+xml"),
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
                Style(open("./main.css").read()))



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
                            A("Explore", href="/explore/english/any", Class="btn btn-primary"),
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


@rt("/explore/{section}/{domain}")
def get(section:str,domain:str):
 
 def domain_lower(input):
  return str(input).lower()
 
 def filter_switch():
   if section == 'english':
     return (  
     A("Information and Ideas", href=f'/explore/{section}/information and ideas',Class="btn btn-filter"),
     A("Craft and Structure", href=f'/explore/{section}/craft and structure',Class="btn btn-filter"),
     A("Expression of Ideas", href=f'/explore/{section}/expression of ideas',Class="btn btn-filter"),
     A("Standard English Conventions", href=f'/explore/{section}/standard english conventions',Class="btn btn-filter")
    )
   else:
     return (
     A("Algebra", href=f'/explore/{section}/algebra',Class="btn btn-filter"),
     A("Advanced Math", href=f'/explore/{section}/advanced math',Class="btn btn-filter"),
     A("Problem-Solving and Data Analysis", href=f'/explore/{section}/problem solving and data analysis',Class="btn btn-filter"),
     A("Geometry and Trigonometry", href=f'/explore/{section}/geometry and trigonometry',Class="btn btn-filter")
    )
   
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
                       Div(
                         A("English", href=f'/explore/english/any',Class="btn btn-primary"),
                         A("Math", href=f'/explore/math/any',Class="btn btn-primary"),
                         Br(),
                         Br(),

                         Div(filter_switch()),
                        Class="filter-container"),
                        *[ A(Div("📚", Class="icon"), Div(f'Question #{i}', Class="question-number"), Div(x['domain'], Class="category"), Class="card", href=f"/questions/{section}/{i}/True" ) if domain.lower() == 'any' or domain_lower(x['domain']) == domain.lower() else Div('', hidden=True) for i, x in enumerate(question_objects(section)) ]
                        

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
                         
                        H2(f"Question #{question_obj['id']}"),
                        P(question_obj['question'].get('paragraph', "")),
                        B(question_obj['question']['question'].replace('$','$')),
                        
                        Div(B("A."), question_obj['question']['choices']['A']),
                        Div(B("B."), question_obj['question']['choices']['B']),
                        Div(B("C."), question_obj['question']['choices']['C']),
                        Div(B("D."), question_obj['question']['choices']['D']),
                        Br(),
                        A("Reveal Answers", href=f'/questions/{section}/{num}/{hide_switch(answer)}',Class="btn btn-primary", style="font-size:0.9em;"),
                        A("Go Back", href=f'/explore/{section}/any',Class="btn btn-secondary", style="font-size:0.9em;"),
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


@rt("/tutors")
def get():
 firestore_docs = db.collection('users').stream()

   
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
                        #*[Div(doc.to_dict()['age'],Class="card") for doc in firestore_docs],

                       *[Div(Img(src=doc.to_dict()['banner'],Class="avatar"),Div(H3(doc.to_dict()['username']),P(doc.to_dict()['description'],Class="description"),P(doc.to_dict()['availability'],Class="status"),P(doc.to_dict()['email'],Class="email"),Div(doc.to_dict()['country'],Class="location"),Class="info"),Button(f"Contact: {doc.to_dict()['contact']}",Class="contact-btn"),Class="profile-card") for doc in firestore_docs]
                        

                        ,Class="list-content"
                   )
                   ,Style="display:flex;"
                )
        )
) 

)


serve()