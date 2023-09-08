//Checks if  password and confirm password are same or not
function validate_password() {
    var pass = document.getElementById('password').value;
    var confirm_pass = document.getElementById('cnfmpass').value;
    var createButton = document.getElementById('45');

    if (pass !== confirm_pass) {
        document.getElementById('checkpass').style.color = 'red';
        document.getElementById('checkpass').innerHTML = 'Password and Confirm Password are different';
        createButton.disabled = true;
        createButton.style.opacity = 0.4;
    } else {
        document.getElementById('checkpass').style.color = 'green';
        document.getElementById('checkpass').innerHTML = 'Password Matched';
        createButton.disabled = false;
        createButton.style.opacity = 1;
    }
}

// to check password minimum lenght
function checkpass() {
    var createButton = document.getElementById('45');
    var pass = document.getElementById('password').value;
    if (pass.length < 6) {
        document.getElementById('1').style.color = 'red';
        document.getElementById("1").innerHTML = "*Password length must be atleast 6 characters";
        createButton.disabled = true;
        createButton.style.opacity = 0.4;
    }
    else {
        document.getElementById("1").innerHTML = "";
        createButton.disabled = false;
        createButton.style.opacity = 1;
    }

}

// to check address length
function checkaddress() {
    var minlength = 15
    var createButton = document.getElementById('45');
    var adres = document.getElementById('address').value;
    var count_address = adres.length

    if (count_address < minlength) {
        document.getElementById('3').style.color = 'red';
        document.getElementById('3').innerHTML = "*Address shoud be minimum lenght of 15 words";
        createButton.disabled = true;
        createButton.style.opacity = 0.4;

    }
    else {
        document.getElementById('3').innerHTML = "";
        createButton.disabled = false;
        createButton.style.opacity = 1;
    }


}

// to check gender must be selected
function checkgender() {
    var gender = document.getElementById('gender').value;
    if (gender == '') {
        document.getElementById('2').style.color = 'red';
        document.getElementById('2').innerHTML = "*Please select your gender";
    }
}

// to check aleast one hobby selected

function check_ticks() {
    var form_data = new
        FormData(document.querySelector('form'));
    if (!form_data.has('hobbies')) {

        document.getElementById('4').style.color = 'red';
        document.getElementById('4').innerHTML = "*Please select at least one option.";
        return false;
    }
    else {
        document.getElementById('4').innerHTML = "";
        return true;
    }
}
