const API_BASE_URL = 'http://127.0.0.1:5000/tasks';

// DOM Elements
const taskForm = document.getElementById('task-form');
const tasksContainer = document.getElementById('tasks-container');
const statusMessage = document.getElementById('status-message');
const statusFilter = document.getElementById('status-filter');
const sortBy = document.getElementById('sort-by');
const toggleSortOrder = document.getElementById('toggle-sort-order');

const editModal = document.getElementById('edit-modal');
const editForm = document.getElementById('edit-form');
let sortOrder = 'ASC'; // Initial sort order

// --- Utility Functions ---

function displayMessage(message, type = 'success') {
    statusMessage.textContent = message;
    statusMessage.className = `message ${type}`;
    setTimeout(() => {
        statusMessage.textContent = '';
        statusMessage.className = 'message';
    }, 3000);
}

// --- API FETCH FUNCTIONS ---

// READ (GET) - Fetches and Renders all tasks
async function fetchTasks() {
    // 1. Get query parameters for filtering/sorting
    const status = statusFilter.value;
    const sortField = sortBy.value;
    
    let url = API_BASE_URL;
    const params = new URLSearchParams();

    if (status) {
        params.append('status', status);
    }
    if (sortField) {
        params.append('sort_by', sortField);
        params.append('sort_order', sortOrder);
    }
    
    if (params.toString()) {
        url += '?' + params.toString();
    }

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch tasks');
        
        const tasks = await response.json();
        renderTasks(tasks);
    } catch (error) {
        displayMessage(`Error loading tasks: ${error.message}`, 'error');
        renderTasks([]); // Clear the list on error
    }
}

// CREATE (POST) - Handles form submission
taskForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const dueDate = document.getElementById('due_date').value;

    const taskData = {
        title: title,
        description: description,
        due_date: dueDate
    };

    try {
        const response = await fetch(API_BASE_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskData)
        });

        const result = await response.json();

        if (response.ok) {
            displayMessage(`Task added successfully! ID: ${result.task_id}`);
            taskForm.reset();
            fetchTasks(); // Refresh the list
        } else {
            displayMessage(`POST Failed: ${result.error || result.message}`, 'error');
        }
    } catch (error) {
        displayMessage(`Network Error: ${error.message}`, 'error');
    }
});

// UPDATE (PATCH) - Handles editing via modal
editForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const id = document.getElementById('edit-id').value;
    const title = document.getElementById('edit-title').value;
    const description = document.getElementById('edit-description').value;
    const dueDate = document.getElementById('edit-due-date').value;

    const updateData = {
        title: title,
        description: description,
        due_date: dueDate
    };

    try {
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updateData)
        });

        const result = await response.json();

        if (response.ok) {
            displayMessage(`Task ID ${id} updated successfully!`);
            editModal.style.display = 'none';
            fetchTasks(); 
        } else {
            displayMessage(`PATCH Failed: ${result.error || result.message}`, 'error');
        }
    } catch (error) {
        displayMessage(`Network Error: ${error.message}`, 'error');
    }
});

// DELETE - Removes a task
async function deleteTask(id) {
    if (!confirm(`Are you sure you want to delete Task ID ${id}?`)) return;

    try {
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (response.ok) {
            displayMessage(result.message);
            fetchTasks();
        } else {
            displayMessage(`DELETE Failed: ${result.error || result.message}`, 'error');
        }
    } catch (error) {
        displayMessage(`Network Error: ${error.message}`, 'error');
    }
}

// UPDATE (PUT) - Toggles status (simplified PUT)
async function toggleStatus(id, currentStatus) {
    const newStatus = currentStatus.toLowerCase() === 'pending' ? 'Completed' : 'Pending';

    try {
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        
        const result = await response.json();

        if (response.ok) {
            displayMessage(`Task ID ${id} status updated to ${newStatus}!`);
            fetchTasks();
        } else {
            displayMessage(`Status Update Failed: ${result.error || result.message}`, 'error');
        }
    } catch (error) {
        displayMessage(`Network Error: ${error.message}`, 'error');
    }
}

// --- RENDER & EVENT HANDLERS ---

function renderTasks(tasks) {
    tasksContainer.innerHTML = ''; // Clear previous tasks

    if (tasks.length === 0) {
        tasksContainer.innerHTML = '<p class="message">No tasks found based on current filters.</p>';
        return;
    }

    tasks.forEach(task => {
        const taskItem = document.createElement('div');
        taskItem.className = `task-item ${task.status.toLowerCase()}`;
        taskItem.dataset.id = task.id; // Store ID for actions

        const formattedDueDate = new Date(task.due_date).toLocaleDateString('en-US');

        taskItem.innerHTML = `
            <div class="task-info">
                <h3>${task.title} (ID: ${task.id})</h3>
                <p>${task.description}</p>
                <p><strong>Due:</strong> ${formattedDueDate} | <strong>Status:</strong> ${task.status}</p>
            </div>
            <div class="task-actions">
                <button class="btn-complete" onclick="toggleStatus(${task.id}, '${task.status}')">
                    ${task.status.toLowerCase() === 'pending' ? 'Mark Done' : 'Mark Pending'}
                </button>
                <button class="btn-edit" onclick="openEditModal(${task.id}, '${task.title}', '${task.description}', '${task.due_date}')">Edit</button>
                <button class="btn-delete" onclick="deleteTask(${task.id})">Delete</button>
            </div>
        `;
        tasksContainer.appendChild(taskItem);
    });
}

// --- MODAL LOGIC ---

function openEditModal(id, title, description, dueDate) {
    // Format the date for the HTML input (YYYY-MM-DD)
    // Note: The date format might need adjustment based on how your API returns it
    const cleanDate = dueDate.split('T')[0]; 

    document.getElementById('edit-id').value = id;
    document.getElementById('edit-title').value = title;
    document.getElementById('edit-description').value = description;
    document.getElementById('edit-due-date').value = cleanDate;
    editModal.style.display = 'block';
}

// Close modal when close button (x) or outside the modal is clicked
document.querySelector('.close-btn').onclick = () => {
    editModal.style.display = 'none';
};
window.onclick = (event) => {
    if (event.target == editModal) {
        editModal.style.display = 'none';
    }
};

// --- FILTERING/SORTING EVENT LISTENERS ---

// Re-fetch tasks whenever the filter or sort field changes
statusFilter.addEventListener('change', fetchTasks);
sortBy.addEventListener('change', fetchTasks);

toggleSortOrder.addEventListener('click', () => {
    if (sortOrder === 'ASC') {
        sortOrder = 'DESC';
        toggleSortOrder.textContent = 'Sort: DESC';
    } else {
        sortOrder = 'ASC';
        toggleSortOrder.textContent = 'Sort: ASC';
    }
    fetchTasks(); // Re-fetch tasks with the new order
});


// Initial load
fetchTasks();