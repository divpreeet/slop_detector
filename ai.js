// Get the input field and the list
const taskInput = document.getElementById('taskInput');
const taskList = document.getElementById('taskList');

function addTask() {
    // Get the task text from the input field and remove whitespace
    const taskText = taskInput.value.trim();

    // Only add a task if the input is not empty
    if (taskText !== '') {
        // Create a new list item (<li>)
        const listItem = document.createElement('li');
        listItem.textContent = taskText;

        // Create a button to remove the task
        const removeButton = document.createElement('button');
        removeButton.textContent = 'Remove';
        removeButton.onclick = function() {
            // Remove the parent list item when the button is clicked
            listItem.remove();
        };

        // Add the remove button to the list item
        listItem.appendChild(removeButton);

        // Add the new list item to the to-do list
        taskList.appendChild(listItem);

        // Clear the input field for the next task
        taskInput.value = '';
    }
}