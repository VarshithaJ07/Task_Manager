const API = "";

// LOAD TASKS
function loadTasks() {
    const taskList = document.getElementById("taskList") || document.getElementById("list");
    if (!taskList) return; // prevent error on other pages

    const user = JSON.parse(localStorage.getItem('currentUser'));
    if (!user || !user.id) {
        console.error("User not logged in");
        return;
    }

    console.log("Loading tasks from API...");
    
    fetch(`${API}/api/tasks?user_id=${user.id}`)
        .then(res => {
            console.log("Response status:", res.status);
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            return res.json();
        })
        .then(data => {
            console.log("Tasks data received:", data);
            
            // Handle both array and object responses
            let tasks = Array.isArray(data) ? data : (data.tasks || []);
            
            taskList.innerHTML = "";

            const emptyState = document.getElementById("emptyState");
            
            if (!tasks || tasks.length === 0) {
                console.log("No tasks found");
                if (emptyState) emptyState.style.display = "block";
                return;
            }
            
            if (emptyState) emptyState.style.display = "none";

            console.log(`Rendering ${tasks.length} tasks...`);
            
            tasks.forEach(task => {
                const li = document.createElement("li");
                li.className = task.status === "completed" ? "task-item completed" : "task-item";

                const textDiv = document.createElement("div");
                textDiv.className = "task-text";
                textDiv.innerHTML = `
                    <div class="task-title">${task.title || "Untitled"}</div>
                    <div class="task-description">${task.description || "No description"}</div>
                    <div class="task-status"><span class="status-badge status-${task.status}">${task.status}</span></div>
                `;

                const actionsDiv = document.createElement("div");
                actionsDiv.className = "task-actions";

                // Complete button
                const completeBtn = document.createElement("button");
                completeBtn.type = "button";
                completeBtn.className = "btn-complete";
                completeBtn.innerText = task.status === "completed" ? "↩ Undo" : "✔ Complete";
                completeBtn.onclick = function(e) {
                    e.preventDefault();
                    completeTask(task.id);
                };

                // Delete button
                const deleteBtn = document.createElement("button");
                deleteBtn.type = "button";
                deleteBtn.className = "btn-delete";
                deleteBtn.innerText = "✖ Delete";
                deleteBtn.onclick = function(e) {
                    e.preventDefault();
                    deleteTask(task.id);
                };

                actionsDiv.appendChild(completeBtn);
                actionsDiv.appendChild(deleteBtn);

                li.appendChild(textDiv);
                li.appendChild(actionsDiv);

                taskList.appendChild(li);
            });
        })
        .catch(err => {
            console.error("Error loading tasks:", err);
            taskList.innerHTML = `<li style="color: red; padding: 20px;">Error loading tasks: ${err.message}</li>`;
        });
}

//ADD TASK
function addTask() {
    const title = document.getElementById("title")?.value.trim();
    const desc = document.getElementById("desc")?.value.trim();
    const user = JSON.parse(localStorage.getItem('currentUser'));

    if (!title) {
        alert("Title is required!");
        return;
    }

    if (!user || !user.id) {
        alert("Please log in first!");
        return;
    }

    fetch(`${API}/api/tasks`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: user.id,
            title: title,
            description: desc
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert("Task Added ✅");
            // Redirect to tasks page to see the new task
            window.location.href = "/tasks";
        } else {
            alert("Error adding task");
        }
    })
    .catch(err => {
        alert("Error: " + err);
    });
}

// COMPLETE 
function completeTask(id) {
    const user = JSON.parse(localStorage.getItem('currentUser'));
    if (!user || !user.id) {
        alert("Please log in first!");
        return;
    }

    fetch(`${API}/api/tasks/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: user.id
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message || data.status) {
            console.log("Task updated:", data);
            loadTasks();
        } else {
            alert("Error updating task");
        }
    })
    .catch(err => {
        console.error("Error completing task:", err);
        alert("Error: " + err);
    });
}

// DELETE
function deleteTask(id) {
    if (!confirm("Are you sure you want to delete this task?")) {
        return;
    }
    
    const user = JSON.parse(localStorage.getItem('currentUser'));
    if (!user || !user.id) {
        alert("Please log in first!");
        return;
    }
    
    fetch(`${API}/api/tasks/${id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: user.id
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            console.log("Task deleted:", data);
            loadTasks();
        } else {
            alert("Error deleting task");
        }
    })
    .catch(err => {
        console.error("Error deleting task:", err);
        alert("Error: " + err);
    });
}

// AUTO LOAD
window.onload = () => {
    loadTasks();
};