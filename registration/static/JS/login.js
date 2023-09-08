// To check email formate
function check_email() {
    var user_email = document.getElementById('login_email').value;
    var regex = /^[a-z0-9]+@[a-z]+\.[a-z]{2,3}$/;
    var result = regex.test(user_email);

    if (!result) {
        document.getElementById('login-email').style.color = 'red';
        document.getElementById('login-email').innerHTML = '*invalid email address!';
    }
    else {
        document.getElementById('login-email').style.color = 'green';
        document.getElementById('login-email').innerHTML = '';
    }
}

