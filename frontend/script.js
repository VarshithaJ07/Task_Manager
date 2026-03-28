const API_URL = "http://127.0.0.1:5000/tasks";

// 🔹 Load all tasks
function loadTasks() {
    fetch(API_URL)
        .then(res => res.json())
        .then(tasks => {
            const taskList = document.getElementById("taskList");
            taskList.innerHTML = "";

            tasks.forEach(task => {
                const li = document.createElement("li");

                const textDiv = document.createElement("div");
                textDiv.className = "task-text";

                textDiv.innerHTML = `
                    <strong>${task.title}</strong><br>
                    <small>${task.description || ""}</small><br>
                    <small>Status: ${task.status}</small>
                `;

                if (task.status === "completed") {
                    textDiv.classList.add("completed");
                }

                const actionsDiv = document.createElement("div");
                actionsDiv.className = "actions";

                // ✅ Complete button
                const completeBtn = document.createElement("button");
                completeBtn.innerText = "✔";
                completeBtn.onclick = () => completeTask(task.id);

                // ❌ Delete button
                const deleteBtn = document.createElement("button");
                deleteBtn.innerText = "✖";
                deleteBtn.classList.add("delete");
                deleteBtn.onclick = () => deleteTask(task.id);

                actionsDiv.appendChild(completeBtn);
                actionsDiv.appendChild(deleteBtn);

                li.appendChild(textDiv);
                li.appendChild(actionsDiv);

                taskList.appendChild(li);
            });
        });
}

// 🔹 Add task
function addTask() {
    const title = document.getElementById("title").value.trim();
    const desc = document.getElementById("desc").value.trim();

    if (!title) {
        alert("Title is required!");
        return;
    }

    fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title,
            description: desc
        })
    })
    .then(() => {
        document.getElementById("title").value = "";
        document.getElementById("desc").value = "";
        loadTasks();
    });
}

// 🔹 Mark task as completed
function completeTask(id) {
    fetch(`${API_URL}/${id}`, {
        method: "PUT"
    }).then(() => loadTasks());
}

// 🔹 Delete task
function deleteTask(id) {
    fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    }).then(() => loadTasks());
}

// Initial load
loadTasks();