let kdtimer = null;
let keyDownTimers = [];
let kutimer = null;
let keyUpTimers = [];

const passwdInput1 = document.querySelector('#password');

const MICROSECOND_INTERVAL = 1; // Interval in microseconds

let firstKeyDownTime = null; // Variable to store the time of the first key down event

passwdInput1.addEventListener('keydown', function(event) {
    if (firstKeyDownTime === null) {
        firstKeyDownTime = performance.now(); // Set the time of the first keydown event
    }
    const elapsed = performance.now() - firstKeyDownTime; // Calculate elapsed time
    keyDownTimers.push({
        key: event.key,
        time: elapsed
    });
});

passwdInput1.addEventListener('keyup', function(event) {
    const elapsed = performance.now() - firstKeyDownTime; // Calculate elapsed time
    keyUpTimers.push({
        key: event.key,
        time: elapsed
    });
});



const registerContainer = document.querySelector('.register-container');
const keyUpValue = document.getElementById('keyup');
const keyDownValue = document.getElementById('keydown');

registerContainer.addEventListener('submit', function(event) {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const username = document.getElementById('username').value;
    
    keyUpValue.value = JSON.stringify(keyUpTimers);
    keyDownValue.value = JSON.stringify(keyDownTimers);

    const data = {
        email: email,
        password: password,
        username: username,
        keyUp: keyUpValue,
        keyDown: keyDownValue
    };

    fetch('register.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            // Data sent successfully, reset keyTimers array
            keyUpTimers = [];
            keyDownTimers = [];
            console.log('Data sent successfully!');
        } else {
            throw new Error('Failed to send data to server');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

});
