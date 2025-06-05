function updateClock() {
    const now = new Date();

    const seconds = now.getSeconds();
    const minutes = now.getMinutes();
    const hours = now.getHours();

    const secAngle = seconds * 6;
    const minAngle = minutes * 6 + seconds * 0.1;
    const hourAngle = (hours % 12) * 30 + minutes * 0.5;

    document.getElementById("secs").style.transform = `rotate(${secAngle}deg)`;
    document.getElementById("mins").style.transform = `rotate(${minAngle}deg)`;
    document.getElementById("hours").style.transform = `rotate(${hourAngle}deg)`;

    const timeString = now.toLocaleTimeString('en-US', { hour12: false });
    document.getElementById("digital-time").textContent = timeString;

    const date = String(now.getDate()).padStart(2, '0');
    const month = String(now.getMonth() + 1).padStart(2, '0'); 
    const year = now.getFullYear();
    document.getElementById("date-display").textContent = `${date}-${month}-${year}`;
}

setInterval(updateClock, 1000);
updateClock();
