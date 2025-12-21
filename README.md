## 🎓OpenSAT: Free SAT Question Databank

OpenSAT is a collaborative project dedicated to providing a comprehensive and freely accessible database of SAT practice questions. Our mission is to ensure equal access to high-quality educational resources for all students preparing for the SAT exam.

**What OpenSAT Offers:**

- **Extensive Question Bank:** Access a wide range of SAT practice questions covering Reading, Writing and Language, and Math sections.
- **Custom Question Generator:** Utilize our AI-powered question generator to create or reuse SAT questions.
- **Open Source:** The entire question bank and codebase are openly available on GitHub, allowing for continuous improvement and community contributions.
- **Free to Use and Modify:** OpenSAT API is accessible to everyone, free of charge.


## Public JSON Database

* Explore our public JSON database containing SAT practice questions
  👉 [https://api.jsonsilo.com/public/942c3c3b-3a0c-4be3-81c2-12029def19f5](https://api.jsonsilo.com/public/942c3c3b-3a0c-4be3-81c2-12029def19f5) 📚

### Example Question Object

```json
{
  "id": "70ced8dc",
  "domain": "Standard English Conventions",
  "question": {
    "paragraph": "Typically, underlines, scribbles, and notes left in the margins by a former owner lower a book’s ______ when the former owner is a famous poet like Walt Whitman, such markings, known as marginalia, can be a gold mine to literary scholars.",
    "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
    "choices": {
      "A": "value, but",
      "B": "value",
      "C": "value,",
      "D": "value but"
    },
    "correct_answer": "A",
    "explanation": "Choice A is the best answer. The convention being tested is the coordination of independent clauses within a sentence..."
  }
}
```

---

## API Access (Questions Endpoint)

### GET `/api/questions`

Retrieve SAT practice questions with optional filters.

### Query Parameters

| Parameter | Type    | Default | Description                                                    |
| --------- | ------- | ------- | -------------------------------------------------------------- |
| section   | string  | english | Question section (case-insensitive, e.g. `english`, `ENGLISH`) |
| domain    | string  | any     | Domain name (case-insensitive)                                 |
| limit     | integer | null    | Maximum number of questions to return                          |

---

### Examples

**Filter by section (case-insensitive)**

```
/api/questions?section=MATH
```

```
/api/questions?section=english
```

---

**Filter by section and domain**

```
/api/questions?section=English&domain=standard%20english%20conventions
```

---

**Use all filters together**

```
/api/questions?section=ENGLISH&domain=Standard%20English%20Conventions&limit=3
```

---

### Response Behavior

* Uppercase and lowercase differences are ignored for all query parameters.
* If no matching domain is found, all questions for the selected section are returned.
* If a domain matches, filtered questions are returned (up to the specified limit).
* All query parameters are optional and can be combined.


## How to Contribute:

Join us in improving OpenSAT:

- **Improve the Question Generator:** Enhance our AI question generator system to provide better SAT questions.
- **Report Question Issues:** Help us identify and address issues with specific questions by reporting them on GitHub under the 'report question' tag.
- **Fix Bugs and Enhance Features:** Share your ideas for improving the platform or report any bugs you encounter on GitHub.

## Getting Started:

1. **Fork the Repository:** Create your own copy of the OpenSAT repository on GitHub by forking it.
2. **Clone Your Fork:** Clone your forked repository to your local machine using Git.
3. **Contribute:** Make changes to the question bank or codebase as needed.
4. **Submit a Pull Request:** Once you're satisfied with your changes, submit a pull request to the main OpenSAT repository for review and potential inclusion.
> [!TIP]
>   For any questions, Message `Anas099` on Discord.

**Let's collaborate to build a comprehensive SAT practice platform accessible to all!** 🌟
