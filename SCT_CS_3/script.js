function checkPasswordStrength(password) {
    let strength = 0;
    const lengthCriteria = password.length >= 8;
    const uppercaseCriteria = /[A-Z]/.test(password);
    const lowercaseCriteria = /[a-z]/.test(password);
    const numberCriteria = /[0-9]/.test(password);
    const specialCharCriteria = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    if (lengthCriteria) strength++;
    if (uppercaseCriteria) strength++;
    if (lowercaseCriteria) strength++;
    if (numberCriteria) strength++;
    if (specialCharCriteria) strength++;

    switch (strength) {
        case 5:
            return "Very Strong";
        case 4:
            return "Strong";
        case 3:
            return "Moderate";
        case 2:
            return "Weak";
        case 1:
        case 0:
        default:
            return "Very Weak";
    }
}

document.getElementById('password').addEventListener('input', function() {
    const password = this.value;
    const strengthMessage = checkPasswordStrength(password);
    document.getElementById('strengthMessage').textContent = `Password strength: ${strengthMessage}`;
    document.getElementById('lengthMessage').textContent = `Password length: ${password.length}`;
});
