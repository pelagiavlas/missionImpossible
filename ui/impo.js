const addUserBtn = document.getElementById('addUserBtn');
const nameInput = document.getElementById('name');
const userList = document.getElementById('userList');

// Base URL for the API (assumes that the backend runs on port 5000)
const apiUrl = 'http://localhost:5000/users';

// Function to fetch users and display them
const fetchUsers = async () => {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();

        userList.innerHTML = '';
        data.forEach(user => {
            const li = document.createElement('li');
            li.textContent = user.name;
            userList.appendChild(li);
        });
    } catch (error) {
        console.error('Error fetching users:', error);
    }
};

// Function to add a user
const addUser = async () => {
    const name = nameInput.value.trim();
    if (name === '') {
        alert('Please enter a name.');
        return;
    }

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name }),
        });

        if (response.ok) {
            nameInput.value = '';  // Clear the input field
            fetchUsers();  // Refresh the user list
        } else {
            alert('Failed to add user');
        }
    } catch (error) {
        console.error('Error adding user:', error);
    }
};

// Event listener for the "Add User" button
addUserBtn.addEventListener('click', addUser);

// Fetch users on page load
fetchUsers();
