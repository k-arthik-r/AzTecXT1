var contactNumberInput = document.getElementById("contact-number");

contactNumberInput.addEventListener("focus", function() {
    if (!contactNumberInput.value.startsWith("+91")) {
        contactNumberInput.value = "+91 " + contactNumberInput.value;
    }
});

function savedetails() {

    var name = document.getElementById("name").value;
    var usn = document.getElementById("usn").value;
    var DOB = document.getElementById("DOB").value;
    var bloodGroupDropdown = document.getElementById("blood-group");
    var selectedBloodGroup = bloodGroupDropdown.value;
    var address = document.getElementById("address").value
    var contact_number = document.getElementById("contact-number").value

    var data = {
        "name": name,
        'usn':usn,
        "DOB": DOB,
        "bloodgroup": selectedBloodGroup,
        "address": address,
        "contactnumber": contact_number
    };


    fetch('/savedetails', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', 
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json()) 
    .then(data => {
        alert(data.message);
        window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
  

    return false;
}