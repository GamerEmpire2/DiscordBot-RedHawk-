function checkUserId() {
    var userId = document.getElementById("userIdInput").value;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "./PHP/check_user.php?userId=" + userId, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById("userIdResult").innerHTML = xhr.responseText;
        }
    };
    xhr.send();
}