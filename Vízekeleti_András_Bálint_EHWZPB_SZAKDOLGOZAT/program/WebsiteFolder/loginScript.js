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

const loginContainer = document.querySelector('.login-container');
const keyUpValue = document.getElementById('keyup');
const keyDownValue = document.getElementById('keydown');

loginContainer.addEventListener('submit', async function(event) {
    event.preventDefault();

    const password = document.getElementById('password').value;
    const username = document.getElementById('username').value;
    
    keyUpValue.value = JSON.stringify(keyUpTimers);
    keyDownValue.value = JSON.stringify(keyDownTimers);

    const data = {
        "Password": password,
        "Username": username,
        "keyup": keyUpValue.value,
        "keydown": keyDownValue.value
    };

    if (password === "keyboardist"){
        const register_link = document.querySelector('.register-link');
        const help_text =  document.getElementById('help-text');
        const qst_msg = document.getElementById('question-msg');
        help_text.textContent = `Loading...`;
        const response = await fetch('login.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            if (response.ok) {
                // Data sent successfully, reset keyTimers array
                keyUpTimers = [];
                keyDownTimers = [];
                console.log('Data sent successfully!');

                const result = await response.json();
                //help_text.textContent = `result: ${result.success}`
                if (result.success){
                    window.location.href = 'http://jscr.inf.elte.hu/szakdoga/statistics.html';
                }else {
                    help_text.style.color = "black";
                    qst_msg.style.color = "black";
                    register_link.style.backgroundColor = "orange";
                    help_text.textContent = "Your typing pattern did not match the expected user pattern. Please try again!";
                    firstKeyDownTime = null;
                    setTimeout(function() {
                        location.reload();
                    }, 5000);
                }
            } else {
                throw new Error('Failed to send data to server');
            }

    } else{
        const register_link = document.querySelector('.register-link');
        register_link.style.backgroundColor = "orange";
        help_text.style.color = "black";
        qst_msg.style.color = "black";
        help_text.textContent = "Incorrect password, the password is 'keyboardist'. Please try again. The page will refresh shortly.";
        firstKeyDownTime = null;
        setTimeout(function() {
            location.reload();
        }, 5000);
    }

});
