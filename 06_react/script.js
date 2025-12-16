function sendRequest(endpoint) {
    
    var a = document.getElementById('valA').value;
    var b = document.getElementById('valB').value;
    var outputSpan = document.getElementById('output');

    var url = "http://localhost:8081/" + endpoint + "?a=" + a + "&b=" + b;

    var request = null;

    try {
        request = new XMLHttpRequest();
    } catch (e) {
        console.error("error");
    }

    if (request) {
        request.open('GET', url, true);

        request.onreadystatechange = function () {
            if (request.readyState == 4) {
                outputSpan.innerText = request.responseText;
                
                if(request.status !== 200) {
                     outputSpan.style.color = "red";
                } else {
                     outputSpan.style.color = "green";
                }
            }
        };

        request.send(null);
    }
}