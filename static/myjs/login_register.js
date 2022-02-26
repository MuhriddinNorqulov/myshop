let passwords = document.querySelectorAll('.password-form')

passwords[0].querySelector('input').placeholder = 'Password'
passwords[1].querySelector('input').placeholder = 'Confirm password'

for (let i = 0; i < passwords.length; i ++) {
    passwords[i].querySelector('input').classList.add('form-control')
}