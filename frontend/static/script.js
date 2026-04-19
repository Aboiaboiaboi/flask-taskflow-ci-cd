// State
let allTasks = [];
let currentFilter = 'all';

// DOM Elements
const taskInput = document.getElementById('taskInput');
const addBtn = document.getElementById('addBtn');
const tasksList = document.getElementById('tasksList');
const errorMsg = document.getElementById('errorMsg');
const filterBtns = document.querySelectorAll('.filter-btn');
const totalCount = document.getElementById('totalCount');
const completedCount = document.getElementById('completedCount');
const pendingCount = document.getElementById('pendingCount');

// Event Listeners
addBtn.addEventListener('click', addTask);
taskInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTask();
});

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        renderTasks();
    });
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
});

// Load all tasks
async function loadTasks() {
    try {
        const response = await fetch('/tasks');
        allTasks = await response.json();
        renderTasks();
        updateStats();
    } catch (error) {
        console.error('Error loading tasks:', error);
        showError('Failed to load tasks');
    }
}

// Add new task
async function addTask() {
    const taskText = taskInput.value.trim();

    if (!taskText) {
        showError('Please enter a task');
        return;
    }

    try {
        const response = await fetch('/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task: taskText })
        });

        if (response.ok) {
            const newTask = await response.json();
            allTasks.push(newTask);
            taskInput.value = '';
            errorMsg.textContent = '';
            renderTasks();
            updateStats();
        } else {
            showError('Failed to add task');
        }
    } catch (error) {
        console.error('Error adding task:', error);
        showError('Error adding task');
    }
}

// Delete task
async function deleteTask(id) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    try {
        const response = await fetch(`/tasks/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            allTasks = allTasks.filter(task => task.id !== id);
            renderTasks();
            updateStats();
        } else {
            showError('Failed to delete task');
        }
    } catch (error) {
        console.error('Error deleting task:', error);
        showError('Error deleting task');
    }
}

// Update task status
async function toggleTaskStatus(id) {
    const task = allTasks.find(t => t.id === id);
    if (!task) return;

    const newStatus = task.status === 'pending' ? 'completed' : 'pending';

    try {
        const response = await fetch(`/tasks/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });

        if (response.ok) {
            task.status = newStatus;
            renderTasks();
            updateStats();
        } else {
            showError('Failed to update task');
        }
    } catch (error) {
        console.error('Error updating task:', error);
        showError('Error updating task');
    }
}

// Render tasks based on filter
function renderTasks() {
    const filteredTasks = allTasks.filter(task => {
        if (currentFilter === 'all') return true;
        return task.status === currentFilter;
    });

    if (filteredTasks.length === 0) {
        tasksList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <p>No tasks found</p>
            </div>
        `;
        return;
    }

    tasksList.innerHTML = filteredTasks.map(task => `
        <div class="task-item ${task.status === 'completed' ? 'completed' : ''}">
            <input 
                type="checkbox" 
                class="task-checkbox" 
                ${task.status === 'completed' ? 'checked' : ''}
                onchange="toggleTaskStatus(${task.id})"
            >
            <div class="task-content">
                <div class="task-text">${escapeHtml(task.task)}</div>
                <div class="task-meta">Status: ${task.status}</div>
            </div>
            <div class="task-actions">
                <button 
                    class="btn btn-danger btn-small" 
                    onclick="deleteTask(${task.id})"
                >
                    🗑️ Delete
                </button>
            </div>
        </div>
    `).join('');
}

// Update statistics
function updateStats() {
    const total = allTasks.length;
    const completed = allTasks.filter(t => t.status === 'completed').length;
    const pending = allTasks.filter(t => t.status === 'pending').length;

    totalCount.textContent = total;
    completedCount.textContent = completed;
    pendingCount.textContent = pending;
}

// Show error message
function showError(message) {
    errorMsg.textContent = message;
    setTimeout(() => {
        errorMsg.textContent = '';
    }, 5000);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
