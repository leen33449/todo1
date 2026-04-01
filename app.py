# from flask import Flask, render_template, request, redirect
# import psycopg2

# app = Flask(__name__)

# # tasks = []


# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         task = request.form.get("task")
#         if task:
#             tasks.append({"text": task, "done": False})
#         return redirect("/")
    
#     return render_template("index.html", tasks=tasks)

# @app.route("/delete/<int:index>")
# def delete(index):
#     if 0 <= index < len(tasks):
#         tasks.pop(index)
#     return redirect("/")

# @app.route("/complete/<int:index>")
# def complete(index):
#     if 0 <= index < len(tasks):
#         tasks[index]["done"] = not tasks[index]["done"]
#     return redirect("/")

# # @app.route("/edit/<int:index>", methods=["POST"])
# # def edit(index):
# #     if 0 <= index < len(tasks):
# #         new_text = request.form.get("task")
# #         if new_text:
# #             tasks[index]["text"] = new_text
# #     return redirect("/")

# @app.route("/edit/<int:index>", methods=["PUT"])
# def edit(index):
#     if 0 <= index < len(tasks):
#         data = request.get_json()
#         new_text = data.get("task")

#         if new_text:
#             tasks[index]["text"] = new_text

#     return "", 204

# @app.route("/clear")
# def clear():
#     tasks.clear()
#     return redirect("/")


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# 🔌 Database connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="mydb",
        user="postgres",
        password="123456"
    )

# 🏠 Home + Add task
@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        task = request.form.get("task")
        if task:
            cur.execute(
                "INSERT INTO tasks (text, done) VALUES (%s, %s)",
                (task, False)
            )
            conn.commit()
        cur.close()
        conn.close()
        return redirect("/")

    cur.execute("SELECT * FROM tasks ORDER BY id;")
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", tasks=tasks)

# 🗑️ Delete
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")

# ✅ Toggle complete
@app.route("/complete/<int:id>")
def complete(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE tasks SET done = NOT done WHERE id = %s",
        (id,)
    )
    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")

# ✏️ Edit
@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    new_text = request.form.get("task")

    if new_text:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE tasks SET text = %s WHERE id = %s",
            (new_text, id)
        )
        conn.commit()

        cur.close()
        conn.close()

    return redirect("/")

# 🧹 Clear all
@app.route("/clear")
def clear():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks;")
    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)