requestAnimationFrame(UpdateAge);
function UpdateAge(timestamp) {
    var Years = (Date.now() - 1094252399999) / 31536000000
    Numbers = Years.toString() + "000000000"
    document.getElementById("Age").innerHTML = Numbers.slice(0, 12)
    requestAnimationFrame(UpdateAge)
}
function ShowUnity(){
    document.getElementById("unity-container").style.opacity = 1;
}