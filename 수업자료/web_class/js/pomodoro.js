const timeInput = document.querySelector('#time-input');
const startBtn = document.querySelector('#start-timer');
const stopBtn = document.querySelector('#stop-timer');
const display = document.querySelector('#timer-display');

let remainingSeconds = 0;
let timerId = null;

function updateDisplay(){
    const min = Math.floor(remainingSeconds / 60);
    const sec = remainingSeconds % 60;
    display.textContent = String(min).padStart(2, '0') + ':' + String(sec).padStart(2, '0');
}


startBtn.addEventListener('click', () => {
    const minutes = Number(timeInput.value)
    if (Number.isNaN(minutes) || minutes <= 0) {
        alert('Please enter a valid number of minutes');
        return;
    }
    remainingSeconds = minutes * 60;
    updateDisplay();
    
    
    timerId = setInterval(() => {
        remainingSeconds--;
        updateDisplay();
        if (remainingSeconds === 0) {
            alert('Time is up!');
            clearInterval(timerId);
        }
    }, 1000);
})

stopBtn.addEventListener('click', () => {
    clearInterval(timerId);
})
