from fasthtml.common import *
from settings import *

app,rt = fast_app(debug=True)

Defaults = (Meta(name="viewport", content="width=device-width"),
            Meta(property="og:title" ,content="OpenSAT: Question Bank with Endless Possibilities"),
            Meta(property="og:description" ,content="OpenSAT, a free and open-source SAT question bank. Dive into a massive pool of SAT practice problems, constantly growing thanks to a dedicated community of contributors."),
            Meta(property="og:image" ,content="https://github.com/Anas099X/OpenSAT/blob/main/public/banner.png?raw=true"),
            Meta(property="og:url" ,content="https://opensat.fun/"),
            Meta(property="og:type" ,content="website"),
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
            Script(src="/_vercel/insights/script.js"),
                Title("OpenSAT"),
                Style(open("main.css").read())
                
)



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
                        cls="logo", href="/",style="text-decoration: none"
                    ),
                    Nav(
                        A("Tutors", href="/tutors", cls="btn btn-primary"),
                        A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn btn-secondary"),
                        cls="nav"
                    ),
                    cls="header"
                ),
                Main(
                    Div(
                        Span("🎓", style="display: flex; font-size: 5rem; margin-bottom: 20px; justify-content: center;"),
                        H2("Question Bank with ", Span("Endless", cls="text-primary-500 decoration-wavy"), " Possibilities",
                           style="font-size: 2.25rem; font-weight: 700; text-align: center; margin-bottom: 20px; color: #333;"),
                        P("OpenSAT, a free and open-source SAT question bank. "
                          "Dive into a massive pool of SAT practice problems, "
                          "constantly growing thanks to a dedicated community of contributors.",
                          style="text-align: center; max-width: 36rem; margin: 0 auto 20px; color: #555; font-size: 1rem;"),
                        Div(
                            A("Explore", href="/explore/english/any", cls="btn btn-primary"),
                            A("Contribute", href="https://github.com/Anas099X/OpenSAT", cls="btn btn-secondary"),
                            style="display: flex; justify-content: center; gap: 15px;"
                            
                        ),
                        cls="container"
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
     A("Information and Ideas", href=f'/explore/{section}/information and ideas',cls="btn btn-filter"),
     A("Craft and Structure", href=f'/explore/{section}/craft and structure',cls="btn btn-filter"),
     A("Expression of Ideas", href=f'/explore/{section}/expression of ideas',cls="btn btn-filter"),
     A("Standard English Conventions", href=f'/explore/{section}/standard english conventions',cls="btn btn-filter")
    )
   else:
     return (
     A("Algebra", href=f'/explore/{section}/algebra',cls="btn btn-filter"),
     A("Advanced Math", href=f'/explore/{section}/advanced math',cls="btn btn-filter"),
     A("Problem-Solving and Data Analysis", href=f'/explore/{section}/problem solving and data analysis',cls="btn btn-filter"),
     A("Geometry and Trigonometry", href=f'/explore/{section}/geometry and trigonometry',cls="btn btn-filter")
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
                        cls="logo",href='/',style="text-decoration: none"
                    ),
                    Nav(
                        A("Tutors", href="/tutors", cls="btn btn-primary"),
                        A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn btn-secondary"),
                        cls="nav"
                    ),
                    cls="header"
                ),
                Main(
                    Div(
                       Div(
                         A("English", href=f'/explore/english/any',cls="btn btn-primary"),
                         A("Math", href=f'/explore/math/any',cls="btn btn-primary"),
                         Br(),
                         Br(),

                         Div(filter_switch()),
                        cls="filter-container"),
                        *[ A(Div("📚", cls="icon"), Div(f'Question #{i}', cls="question-number"), Div(x['domain'], cls="category"), cls="card", href=f"/questions/{section}/{i}/True" ) if domain.lower().replace('%20',' ') == 'any' or domain_lower(x['domain']) == domain.lower().replace('%20',' ') else Div('', hidden=True) for i, x in enumerate(question_objects(section)) ]
                        

                        ,cls="list-content"
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
                        cls="logo",href='/',style="text-decoration: none"
                    ),
                    Nav(
                        A("Tutors", href="/tutors", cls="btn btn-primary"),
                        A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn btn-secondary"),
                        cls="nav"
                    ),
                    cls="header"
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
                        A("Reveal Answers", href=f'/questions/{section}/{num}/{hide_switch(answer)}',cls="btn btn-primary", style="font-size:0.9em;"),
                        A("Go Back", href=f'/explore/{section}/any',cls="btn btn-secondary", style="font-size:0.9em;"),
                        Div(
                        Br(),
                        B(f"Correct Answer is: {question_obj['question']['correct_answer']}"),
                        P(question_obj['question']['explanation']), 
                         hidden=bool(answer)
                        )

                        ,cls="container",style="max-width:80vh;"
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
                        cls="logo",href='/',style="text-decoration: none"
                    ),
                    Nav(
                        A("Tutors", href="/tutors", cls="btn btn-primary"),
                        A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn btn-secondary"),
                        cls="nav"
                    ),
                    cls="header"
                ),
                Main(
                    Div(
                        #*[Div(doc.to_dict()['age'],cls="card") for doc in firestore_docs],

                       *[Div(Img(src=doc.to_dict()['banner'],cls="avatar"),Div(H3(doc.to_dict()['username']),P(doc.to_dict()['description'],cls="description"),P(doc.to_dict()['availability'],cls="status"),P(doc.to_dict()['email'],cls="email"),Div(doc.to_dict()['country'],cls="location"),cls="info"),Button(f"Contact: {doc.to_dict()['contact']}",cls="contact-btn"),cls="profile-card") for doc in firestore_docs]
                        

                        ,cls="list-content"
                   )
                   ,Style="display:flex;"
                )
        )
) 

)


serve()