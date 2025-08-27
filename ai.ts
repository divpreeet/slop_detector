// Define the structure for a task
interface Task {
    id: number;
    text: string;
    completed: boolean;
}

// Get HTML elements
const taskInput = document.getElementById('taskInput') as HTMLInputElement;
const addButton = document.getElementById('addButton') as HTMLButtonElement;
const taskList = document.getElementById('taskList') as HTMLUListElement;

// Array to store tasks
let tasks: Task[] = [];
let nextId: number = 0;

// Function to render the tasks
function renderTasks(): void {
    taskList.innerHTML = '';
    tasks.forEach(task => {
        const li = document.createElement('li');
        li.textContent = task.text;
        li.className = task.completed ? 'completed' : '';
        li.addEventListener('click', () => toggleTask(task.id));
        taskList.appendChild(li);
    });
}

// Function to add a new task
function addTask(): void {
    const text = taskInput.value.trim();
    if (text) {
        const newTask: Task = {
            id: nextId++,
            text,
            completed: false,
        };
        tasks.push(newTask);
        taskInput.value = '';
        renderTasks();
    }
}

// Function to toggle a task's completion status
function toggleTask(id: number): void {
    const task = tasks.find(t => t.id === id);
    if (task) {
        task.completed = !task.completed;
        renderTasks();
    }
}

// Add event listener to the "Add" button
addButton.addEventListener('click', addTask);
taskInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        addTask();
    }
});

// Initial render
renderTasks();
