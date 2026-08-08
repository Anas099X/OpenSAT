

## 🎓OpenSAT: Banco gratuito de preguntas para el SAT

OpenSAT es un proyecto colaborativo dedicado a proporcionar una base de datos completa y de acceso gratuito de preguntas de práctica para el SAT. Nuestra misión es garantizar un acceso igualitario a recursos educativos de alta calidad para todos los estudiantes que se preparan para el examen SAT.

**¿Qué ofrece OpenSAT?:**

- **Amplio banco de preguntas:** Accede a una amplia gama de preguntas de práctica para el SAT que cubren las secciones de Lectura, Escritura y Lenguaje, y Matemáticas.
- **Generador personalizado de preguntas:** Utiliza nuestro generador de preguntas impulsado por IA para crear o reutilizar preguntas del SAT.
- **Código abierto:** Todo el banco de preguntas y la base de código están disponibles públicamente en GitHub, permitiendo una mejora continua y contribuciones de la comunidad.
- **Uso y modificación gratuitos:** La API de OpenSAT es accesible para todos, sin costo alguno.


## Base de datos pública en JSON

* Explora nuestra base de datos pública en JSON que contiene preguntas de práctica para el SAT
  👉 [pinesat.duckdns.org/api/questions](https://pinesat.duckdns.org/api/questions) 📚

### Ejemplo de objeto de pregunta

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

### Acceso a la API (Endpoint de preguntas)

#### GET `/api/questions`

Obtén preguntas de práctica para el SAT con filtros opcionales.

#### Parámetros de consulta

| Parámetro | Tipo    | Predeterminado | Descripción                                                    |
| --------- | ------- | ------- | -------------------------------------------------------------- |
| section   | string  | english | Sección de la pregunta (sin distinción de mayúsculas/minúsculas, ej. `english`, `ENGLISH`) |
| domain    | string  | any     | Nombre del dominio (sin distinción de mayúsculas/minúsculas)                                 |
| limit     | integer | null    | Número máximo de preguntas a devolver                          |

---

#### Ejemplos

**Filtrar por sección**

```
/api/questions?section=MATH
```

```
/api/questions?section=english
```

---

**Filtrar por sección y dominio**

```
/api/questions?section=English&domain=standard%20english%20conventions
```

---

**Usar todos los filtros juntos**

```
/api/questions?section=ENGLISH&domain=Standard%20English%20Conventions&limit=3
```

---

#### Comportamiento de la respuesta

* Las diferencias entre mayúsculas y minúsculas se ignoran para todos los parámetros de consulta.
* Si no se encuentra un dominio coincidente, se devuelven todas las preguntas de la sección seleccionada.
* Si hay un dominio coincidente, se devuelven las preguntas filtradas (hasta el límite especificado).
* Todos los parámetros de consulta son opcionales y se pueden combinar.


## Cómo contribuir:

Únete a nosotros para mejorar OpenSAT:

- **Mejorar el generador de preguntas:** Mejora nuestro sistema de generación de preguntas con IA para ofrecer mejores preguntas del SAT.
- **Reportar problemas con preguntas:** Ayúdanos a identificar y resolver problemas con preguntas específicas informándolos en GitHub bajo la etiqueta 'report question'.
- **Corregir errores y mejorar funcionalidades:** Comparte tus ideas para mejorar la plataforma o reporta cualquier error que encuentres en GitHub.

## Primeros pasos:

1. **Hacer un fork del repositorio:** Crea tu propia copia del repositorio de OpenSAT en GitHub haciendo un fork.
2. **Clonar tu fork:** Clona el repositorio bifurcado en tu máquina local usando Git.
3. **Contribuir:** Realiza cambios en el banco de preguntas o en la base de código según sea necesario.
4. **Enviar una Pull Request:** Una vez que estés satisfecho con tus cambios, envía una pull request al repositorio principal de OpenSAT para su revisión e posible inclusión.
> [!TIP]
>   Para cualquier consulta, envía un mensaje a `Anas099` en Discord.

**¡Colaboremos para construir una plataforma completa de práctica para el SAT accesible para todos!** 🌟
