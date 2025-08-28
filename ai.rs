use std::io;

#[derive(Debug)]
struct Todo {
    task: String,
    done: bool,
}

fn main() {
    let mut todos: Vec<Todo> = Vec::new();

    loop {
        println!("\nTODO List");
        println!("1. Add task");
        println!("2. List tasks");
        println!("3. Mark task as done");
        println!("4. Exit");
        println!("Enter your choice:");

        let mut choice = String::new();
        io::stdin().read_line(&mut choice).unwrap();

        match choice.trim() {
            "1" => {
                println!("Enter the task description:");
                let mut desc = String::new();
                io::stdin().read_line(&mut desc).unwrap();
                todos.push(Todo { task: desc.trim().to_string(), done: false });
                println!("Task added!");
            }
            "2" => {
                println!("\nTasks:");
                for (i, todo) in todos.iter().enumerate() {
                    let status = if todo.done { "[x]" } else { "[ ]" };
                    println!("{} {} {}", i + 1, status, todo.task);
                }
            }
            "3" => {
                println!("Enter the task number to mark as done:");
                let mut num = String::new();
                io::stdin().read_line(&mut num).unwrap();
                if let Ok(idx) = num.trim().parse::<usize>() {
                    if idx > 0 && idx <= todos.len() {
                        todos[idx - 1].done = true;
                        println!("Task marked as done!");
                    } else {
                        println!("Invalid task number.");
                    }
                } else {
                    println!("Please enter a valid number.");
                }
            }
            "4" => break,
            _ => println!("Invalid choice, please try again."),
        }
    }
    println!("Goodbye!");
}
