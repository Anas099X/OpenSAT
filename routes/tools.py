from main import *
import secrets

# Add global variable for storing checked questions
checked_questions = []



@rt("/tools")
def get(request, session):
    email = session.get("user", {}).get("email")

    if not email:
        return Redirect("/login")

    subscribed = False
    if email:
        doc = db.collection("users").document(email).get()
        subscribed = doc.exists and doc.to_dict().get("subscribed", False)

    if not subscribed:
        return Redirect("/subscription")
    navigation = mobile_menu if is_mobile(request) else Navbar()
    return (
        site_title,
        Head(Defaults),
        Body(
            Header(
                navigation,
                cls="sticky top-0 bg-warning z-50"
            ),
            Main(
                H1("Tools", cls="text-4xl font-extrabold text-center my-8"),
                Div(
                    Div(
                        H2("Available Tools", cls="font-bold text-lg mb-4"),
                        Div(
                            A(
                                "Custom Quizzes",
                                href="/tools/custom_quizzes",
                                cls="btn btn-warning btn-lg w-full mb-4"
                            ),
                            # Placeholder for future tools
                            # Div(
                            #     A("Tool Name", href="/tools/tool_route", cls="btn btn-outline btn-primary w-full mb-4"),
                            #     P("Description of the tool.", cls="mb-2"),
                            # ),
                        ),
                        cls="max-w-xl mx-auto bg-base-300 p-8 rounded-lg shadow-xl"
                    ),
                    cls="container mx-auto py-4"
                ),
                cls="container mx-auto py-4"
            ),
            data_theme="silk",
            cls="bg-base-200"
        )
    )


@rt("/tools/create_custom_quiz")
def get(request, session):
    # Check if user is logged in
    email = session.get("user", {}).get("email")
    if not email:
        return Redirect("/login")
    navigation = mobile_menu if is_mobile(request) else Navbar()
    return (
        site_title,
        Head(Defaults),
        Body(
            Header(
                # ...existing header code...
                navigation,
                cls="sticky top-0 bg-warning z-50"
            ),
            Main(
                H1("Create a Custom Quiz", cls="text-4xl font-extrabold text-center my-8"),
                Div(
                    Form(
                        Div(
                            # Initial question block
                            Div("Practice Test Name", cls="font-semibold mb-1"),
                            Input(type="text", name="quiz_title", cls="input input-bordered w-full mb-2", required=True),
                            Div(
                                hx_post="/tools/add_question",
                                hx_target="#questions-container",
                                hx_swap="end",
                                hx_trigger="load",
                                cls="question-block rounded-lg"
                            ),
                            id="questions-container",
                            cls="overflow-y-auto max-h-96"
                        ),
                        Button(
                            "Add Question",
                            type="button",
                            hx_post="/tools/add_question",
                            hx_target="#questions-container",
                            hx_swap="beforeend",
                            cls="btn btn-outline btn-warning w-full mb-4"
                        ),
                        Button("Create Quiz", type="submit", cls="btn btn-warning w-full mt-4"),
                        hx_post="/tools/create_custom_quiz",
                        hx_target="#quiz-message",
                        id="custom-quiz-form"
                    ),
                    Div(id="quiz-message", cls="mt-4"),
                    cls="max-w-xl mx-auto bg-base-300 p-8 rounded-lg shadow-xl"
                ),
                cls="container mx-auto py-4"
            ),
            data_theme="silk",
            cls="bg-base-200"
        )
    )

@rt("/tools/create_custom_quiz")
async def post(session,request: Request):
    email = session.get("user", {}).get("email")
    if not email:
        return Div("You must be logged in to create a quiz.", cls="alert alert-error")
    # Store the quiz as a document in a subcollection under the user
    practice_ref = db.collection("practices")
    form = await request.form()

    questions_list = []

    quiz_data = {
        "owner": email,
        "title": form.get("quiz_title", "Custom Quiz"),
        "question": questions_list
    }

    for key, value in form.items():
    # Only proceed if it's a question field and not empty
     if key.startswith("question_") and value:
        # Build the choices by getting corresponding values from the form
        question_number = key.split("_")[1]  # Assuming keys are like 'question_1', 'choice_a_1'

        questions_data = {
            "paragraph": form.get(f"paragraph_{question_number}", ""),
            "question": value,
            "choices": {
                "A": form.get(f"choice_a_{question_number}", ""),
                "B": form.get(f"choice_b_{question_number}", ""),
                "C": form.get(f"choice_c_{question_number}", ""),
                "D": form.get(f"choice_d_{question_number}", "")
            }
        }

        questions_list.append(questions_data)

    practice_ref.add(quiz_data)
    return Div("Test created successfully!", cls="alert alert-success"),Script("setTimeout(() => window.location.href = '/tools/custom_quizzes', 2000);")




@rt("/tools/add_question")
def post():
    n = secrets.token_urlsafe(2)
    return Div(
        Button(
            hx_get="/tools/create_custom_quiz",
            hx_swap="delete",
            hx_target="closest .question-block",
            cls="ti ti-trash text-2xl text-red-600 m-1"
        ),

        Div(f"Question #{n}", cls="font-semibold mb-3 text-lg flex self-start"),
        Textarea(name=f"paragraph_{n}",placeholder="this is example paragraph in which could be used for sentences", cls="textarea w-full textarea-ghost textarea-bordered mb-2", required=True),
        Input(type="text", placeholder="Write Queston here", name=f"question_{n}", cls="input input-ghost input-bordered w-full mb-2", required=True),
        Div(
            Div(B("A. "), Input(type="text", placeholder="Choice A", name=f"choice_a_{n}", cls="input input-ghost input-bordered w-full mb-2", required=True), cls="py-0.5"),
            Div(B("B. "), Input(type="text", placeholder="Choice B", name=f"choice_b_{n}", cls="input input-ghost input-bordered w-full mb-2", required=True), cls="py-0.5"),
            Div(B("C. "), Input(type="text", placeholder="Choice C", name=f"choice_c_{n}", cls="input input-ghost input-bordered w-full mb-2", required=True), cls="py-0.5"),
            Div(B("D. "), Input(type="text", placeholder="Choice D", name=f"choice_d_{n}", cls="input input-ghost input-bordered w-full mb-2", required=True), cls="py-0.5"),
            cls="text"
        ),
        cls="question-block bg-base-200 rounded-lg p-4 mb-4 border border-base-300",
    )




@rt("/tools/custom_quizzes")
def get(request, session):
    email = session.get("user", {}).get("email")
    if not email:
        return Redirect("/login")
    navigation = mobile_menu if is_mobile(request) else Navbar()
    practice_ref = db.collection("practices")
    
    quizzes = []
    for doc in practice_ref.where("owner", "==", email).stream():
        data = doc.to_dict()
        quizzes.append({
            "id": doc.id,
            "title": data.get("title", f"Quiz {doc.id}"),
            "questions": data.get("question", [])  # Use "question" field for questions
        })
    return (
        site_title,
        Head(Defaults),
        Body(
            Header(
                # ...existing header code...
                navigation,
                cls="sticky top-0 bg-warning z-50"
            ),
            Main(
                H1("My Custom Quizzes", cls="text-4xl font-extrabold text-center my-8"),
                Div(
                    A("create a new quiz", href="/tools/create_custom_quiz", cls="btn btn-warning btn-lg justify-center mb-4"),
                    P("Here you can create, edit, and take your custom quizzes.", cls="text-center mb-8 text-lg"),
                    cls="text-center mb-6"
                ),
                Div(
                    *[
                        Div(
                            H2(quiz["title"], cls="font-bold text-lg mb-2"),
                            Button(
                                "Take Quiz",
                                hx_get=f"/practice/{quiz['id']}/custom/true",
                                hx_target="#edit-quiz-modal",
                                cls="btn btn-warning btn-sm mt-2"
                            ),
                            A(
                                "Edit",
                                href=f"/tools/edit_custom_quiz_page?id={quiz['id']}",
                                cls="btn btn-warning btn-sm mt-2"
                            ),
                            Button(
                                "Delete",
                                hx_post=f"/tools/delete_custom_quiz?id={quiz['id']}",
                                hx_target="#edit-quiz-modal",
                                hx_confirm="Are you sure you want to delete this quiz?",
                                cls="btn btn-error btn-sm mt-2"
                            ),
                            cls="card bg-base-300 p-4 mb-4 shadow"
                        )
                        for i, quiz in enumerate(quizzes)
                    ],
                    Div(id="edit-quiz-modal"),
                    cls="max-w-xl mx-auto"
                ),
                cls="container mx-auto py-4"
            ),
            data_theme="silk",
            cls="bg-base-200"
        )
    )

@rt("/tools/edit_custom_quiz_page")
def get(request, session, id: str):
    email = session.get("user", {}).get("email")
    if not email:
        return Redirect("/login")
    navigation = mobile_menu if is_mobile(request) else Navbar()
    practice_ref = db.collection("practices")
    quiz_doc = practice_ref.document(id).get()
    if not quiz_doc.exists:
        return Div("Quiz not found.", cls="alert alert-error")
    quiz = quiz_doc.to_dict()
    questions = quiz.get("question", [])  # Use "question" field for questions
    quiz_title = quiz.get("title", "Custom Quiz")
    # Render quiz title and all questions for editing
    return (
        site_title,
        Head(Defaults),
        Body(
            Header(
                navigation,
                cls="sticky top-0 bg-warning z-50"
            ),
            Main(
                H1("Edit Custom Quiz", cls="text-4xl font-extrabold text-center my-8"),
                Div(
                    Form(
                        Div(
                            Div("Quiz Title:", cls="font-semibold mb-2"),
                            Input(type="text", name="quiz_title", value=quiz_title, cls="input input-bordered w-full mb-4", required=True),
                        ),
                        Div(
                        *[
                            Div(
                                Div(f"Question {i+1}:", cls="font-semibold mb-2"),
                                Textarea(name=f"paragraph_{i}", value=q.get("paragraph", ""), cls="textarea textarea-bordered w-full mb-2", required=False),
                                Div("Question:", cls="font-semibold mb-1"),
                                Input(type="text", name=f"question_{i}", value=q.get("question", ""), cls="input input-bordered w-full mb-2", required=True),
                                Div("choice A:", cls="font-semibold mb-1"),
                                Input(type="text", name=f"choice_{i}_a", value=q["choices"].get("A", ""), cls="input input-bordered w-full mb-2", required=True),
                                Div("choice B:", cls="font-semibold mb-1"),
                                Input(type="text", name=f"choice_{i}_b", value=q["choices"].get("B", ""), cls="input input-bordered w-full mb-2", required=True),
                                Div("choice C:", cls="font-semibold mb-1"),
                                Input(type="text", name=f"choice_{i}_c", value=q["choices"].get("C", ""), cls="input input-bordered w-full mb-2", required=True),
                                Div("choice D:", cls="font-semibold mb-1"),
                                Input(type="text", name=f"choice_{i}_d", value=q["choices"].get("D", ""), cls="input input-bordered w-full mb-2", required=True),
                                cls="question-block bg-base-200 rounded-lg p-4 mb-4 border border-base-300"
                            )
                            for i, q in enumerate(questions)
                        ]
                        ,cls="overflow-y-auto max-h-96"),
                        Button("Save Changes", type="submit", cls="btn btn-success w-full mt-4"),
                        action=f"/tools/edit_custom_quiz_page?id={id}",
                        method="post",
                        id="edit-quiz-form"
                    ),
                    cls="max-w-xl bg-base-300 p-6 rounded-lg shadow-xl max-w-2xl mx-auto"
                ),
                cls="container mx-auto py-4"
            ),
            data_theme="silk",
            cls="bg-base-200"
        )
    )

@rt("/tools/edit_custom_quiz_page", methods=["POST"])
async def post(request, session, id: str):
    email = session.get("user", {}).get("email")
    if not email:
        return Redirect("/login")
    practice_ref = db.collection("practices")
    form = await request.form()
    questions = []
    i = 0
    while True:
        q_text = form.get(f"question_{i}")
        if not q_text:
            break
        paragraph = form.get(f"paragraph_{i}", "")
        choices = {
            "A": form.get(f"choice_{i}_a", ""),
            "B": form.get(f"choice_{i}_b", ""),
            "C": form.get(f"choice_{i}_c", ""),
            "D": form.get(f"choice_{i}_d", ""),
        }
        questions.append({
            "paragraph": paragraph,
            "question": q_text,
            "choices": choices
        })
        i += 1
    quiz_title = form.get("quiz_title", "Custom Quiz")
    if not questions:
        return Div("At least one question is required.", cls="alert alert-error")
    practice_ref.document(id).update({"question": questions, "title": quiz_title})
    return Redirect("/tools/custom_quizzes")

@rt("/tools/delete_custom_quiz")
def post(request, session, id: str):
    email = session.get("user", {}).get("email")
    if not email:
        return Div("You must be logged in.", cls="alert alert-error")
    practice_ref = db.collection("practices")
    quiz_doc = practice_ref.document(id).get()
    if not quiz_doc.exists:
        return Div("Quiz not found.", cls="alert alert-error")
    quiz = quiz_doc.to_dict()
    if quiz.get("owner") != email:
        return Div("You do not have permission to delete this quiz.", cls="alert alert-error")
    practice_ref.document(id).delete()
    return Div("Quiz deleted successfully!", cls="alert alert-success"), Script("setTimeout(() => window.location.reload(), 1000);")


# ...existing code...
