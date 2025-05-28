from main import *
import secrets

# Add global variable for storing checked questions
checked_questions = []

@rt("/tools")
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
                                hx_post="/add_question",
                                hx_target="#questions-container",
                                hx_trigger="load",
                                cls="question-block bg-base-200 rounded-lg p-4 mb-4 border border-base-300"
                            ),
                            id="questions-container"
                        ),
                        Button(
                            "Add Question",
                            type="button",
                            hx_post="/add_question",
                            hx_target="#questions-container",
                            hx_swap="beforeend",
                            cls="btn btn-outline btn-warning w-full mb-4"
                        ),
                        Button("Create Quiz", type="submit", cls="btn btn-warning w-full mt-4"),
                        hx_post="/create_custom_quiz",
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

@rt("/create_custom_quiz")
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
        "questions": questions_list
    }

    for key, value in form.items():
    # Only proceed if it's a question field and not empty
     if key.startswith("question_") and value:
        # Build the answers by getting corresponding values from the form
        question_number = key.split("_")[1]  # Assuming keys are like 'question_1', 'answer_a_1'

        questions_data = {
            "question": value,
            "answers": {
                "A": form.get(f"answer_a_{question_number}", ""),
                "B": form.get(f"answer_b_{question_number}", ""),
                "C": form.get(f"answer_c_{question_number}", ""),
                "D": form.get(f"answer_d_{question_number}", "")
            }
        }

        questions_list.append(questions_data)

    practice_ref.add(quiz_data)




@rt("/add_question")
def post():
    n = secrets.token_urlsafe(2)
    return Div(
        Button(
            hx_get="/tools",
            hx_swap="delete",
            hx_target="closest .question-block",
            cls="ti ti-trash text-2xl text-red-600 m-1"
        ),

        Div(f"Question #{n}", cls="font-semibold mb-3 text-lg flex self-start"),
        Textarea(name=f"question_{n}",placeholder="this is example paragraph in which could be used for sentences and questions", cls="textarea w-full textarea-ghost textarea-bordered mb-2", required=True),
        
        Div(
            Div(B("A. "), Input(type="text", placeholder="Choice A", name=f"answer_a_{n}", cls="input input-ghost input-bordered w-full mb-2", required=True), cls="py-0.5"),
            Div(B("B. "), Input(type="text", placeholder="Choice B", name=f"answer_b_{n}", cls="input input-ghost input-bordered w-full mb-2", required=True), cls="py-0.5"),
            Div(B("C. "), Input(type="text", placeholder="Choice C", name=f"answer_c_{n}", cls="input input-ghost input-bordered w-full mb-2", required=True), cls="py-0.5"),
            Div(B("D. "), Input(type="text", placeholder="Choice D", name=f"answer_d_{n}", cls="input input-ghost input-bordered w-full mb-2", required=True), cls="py-0.5"),
            cls="text"
        ),
        cls="question-block bg-base-200 rounded-lg p-4 mb-4 border border-base-300",
    )




@rt("/my_custom_quizzes")
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
            "questions": data.get("questions", [])
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
                    *[
                        Div(
                            H2(f"Quiz {i+1}", cls="font-bold text-lg mb-2"),
                            Button(
                                "Edit",
                                hx_get=f"/edit_custom_quiz?id={quiz['id']}",
                                hx_target="#edit-quiz-modal",
                                cls="btn btn-warning btn-sm mt-2"
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

@rt("/edit_custom_quiz")
def get(request, session, id: str):
    email = session.get("user", {}).get("email")
    if not email:
        return Div("You must be logged in.", cls="alert alert-error")
    practice_ref = db.collection("practices")
    quiz_doc = practice_ref.document(id).get()
    if not quiz_doc.exists:
        return Div("Quiz not found.", cls="alert alert-error")
    quiz = quiz_doc.to_dict()
    questions = quiz.get("questions", [])
    # Render all questions for editing
    return Div(
        Form(
            *[
                Div(
                    Div(f"Question {i+1}:", cls="font-semibold mb-2"),
                    Textarea(name=f"question_{i}", value=q.get("question", ""), cls="textarea textarea-bordered w-full mb-2", required=True),
                    Div("Answer A:", cls="font-semibold mb-1"),
                    Input(type="text", name=f"answer_{i}_a", value=q["answers"].get("A", ""), cls="input input-bordered w-full mb-2", required=True),
                    Div("Answer B:", cls="font-semibold mb-1"),
                    Input(type="text", name=f"answer_{i}_b", value=q["answers"].get("B", ""), cls="input input-bordered w-full mb-2", required=True),
                    Div("Answer C:", cls="font-semibold mb-1"),
                    Input(type="text", name=f"answer_{i}_c", value=q["answers"].get("C", ""), cls="input input-bordered w-full mb-2", required=True),
                    Div("Answer D:", cls="font-semibold mb-1"),
                    Input(type="text", name=f"answer_{i}_d", value=q["answers"].get("D", ""), cls="input input-bordered w-full mb-2", required=True),
                    cls="question-block bg-base-200 rounded-lg p-4 mb-4 border border-base-300"
                )
                for i, q in enumerate(questions)
            ],
            Button("Save Changes", type="submit", cls="btn btn-success w-full mt-4"),
            hx_post=f"/edit_custom_quiz_post?id={id}",
            hx_target="#edit-quiz-modal",
            id="edit-quiz-form"
        ),
        cls="bg-base-300 p-6 rounded-lg shadow-xl"
    )

@rt("/edit_custom_quiz_post")
async def post(session, request: "Request", id: str):
    email = session.get("user", {}).get("email")
    if not email:
        return Div("You must be logged in.", cls="alert alert-error")
    practice_ref = db.collection("practices")
    form = await request.form()
    # Rebuild questions list from form data
    questions = []
    i = 0
    while True:
        q_text = form.get(f"question_{i}")
        if not q_text:
            break
        answers = {
            "A": form.get(f"answer_{i}_a", ""),
            "B": form.get(f"answer_{i}_b", ""),
            "C": form.get(f"answer_{i}_c", ""),
            "D": form.get(f"answer_{i}_d", ""),
        }
        questions.append({
            "question": q_text,
            "answers": answers
        })
        i += 1
    if not questions:
        return Div("At least one question is required.", cls="alert alert-error")
    practice_ref.document(id).update({"questions": questions})
    return Div("Quiz updated successfully!", cls="alert alert-success")

# ...existing code...
