let kdtimer = null;
let keyDownTimers = [];
let kutimer = null;
let keyUpTimers = [];

const passwdInput1 = document.querySelector('#password');
const usernameInput = document.getElementById('username');
const registerInfo = document.querySelector('.registration-info');
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

usernameInput.addEventListener('blur', function(event) {
    const username = event.target.value;
    getRegistryCount(username);
});

const registerContainer = document.querySelector('.register-container');
const keyUpValue = document.getElementById('keyup');
const keyDownValue = document.getElementById('keydown');

registerContainer.addEventListener('submit', function(event) {

    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const username = document.getElementById('username').value;
    const registrationMessage = document.getElementById('registrationMessage');
    const knownIssueMessage = document.getElementById('known-issues-msg');
    
    keyUpValue.value = JSON.stringify(keyUpTimers);
    keyDownValue.value = JSON.stringify(keyDownTimers);

    const data = {
        "email": email,
        "Password": password,
        "Username": username,
        "keyup": keyUpValue.value,
        "keydown": keyDownValue.value
    };

    registrationMessage.textContent = "Loading..."

    if (password === "keyboardist"){
        fetch('register.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                // Data sent successfully, reset keyTimers array and send info to user               
                if (9 > keyUpTimers.length){
                console.log('Insufficient data!');
                registerInfo.style.backgroundColor = 'red';
                registrationMessage.style.color = "black";
                knownIssueMessage.style.color = 'black'
                registrationMessage.textContent = "Failed to capture relevant key data. Make sure not to copy and paste the password!"
                }
                else{
                console.log('Data sent successfully!');
                registerInfo.style.backgroundColor = 'lightgreen';
                registrationMessage.style.color = "black";
                knownIssueMessage.style.color = 'black'
                registrationMessage.textContent = "Succesful data submit! The page will reload shortly!"
                }          
                keyUpTimers = [];
                keyDownTimers = [];
                //setTimeout(function() {
                //    location.reload();
                //}, 3000);
            } else {
                throw new Error('Failed to send data to server');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        registerInfo.style.backgroundColor = 'orange';
        registrationMessage.style.color = "black";
        knownIssueMessage.style.color = 'black'
        registrationMessage.textContent = "Wrong password, registration unsuccesful! The page will reload shortly!"
        setTimeout(function() {
            location.reload();
        }, 5000);
    }

});

function getRegistryCount(username) {
    const registrationMessage = document.getElementById('registrationMessage');
    const knownIssueMessage = document.getElementById('known-issues-msg');
    const pswdLabel = document.getElementById('pswd-label-ID');
    registrationMessage.textContent = `Loading...`;
    fetch('resources/registry.json')
        .then(response => response.json())
        .then(data => {
            if (data.hasOwnProperty(username)) {
                const registryCount = data[username];
                if (registryCount > 9){
                    registerInfo.style.backgroundColor = 'lightgreen';
                    registrationMessage.textContent = `Number of registrations for ${username}: ${registryCount}. Thank you, you can login now!`;
                    knownIssueMessage.textContent = "";
                }
                else{
                    pswdLabel.textContent = `The ${registryCount + 1}. Password`;
                    registerInfo.style.backgroundColor = 'lightblue';
                    console.log(`Number of registries for ${username}: ${registryCount}`);
                    registrationMessage.style.color = 'black'
                    knownIssueMessage.style.color = 'black'
                    registrationMessage.textContent = `Number of registrations for user ${username}: ${registryCount}.`;
                }
            } else {
                registrationMessage.textContent = `No registries found for ${username}`;
                console.log(`No registries found for ${username}`);
            }
        })
        .catch(error => console.error('Error:', error));
}
