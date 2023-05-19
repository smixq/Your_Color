let buttons = document.querySelectorAll('.delete_favourite_button')
let likes = document.querySelectorAll('.like')
let palette_col = document.querySelectorAll('.palette_col')
let toast = document.querySelector('.toast')
let toast__close = document.querySelector('.toast__close')

buttons.forEach((button) => {
    button.addEventListener('click', (event) => {
        let block = document.getElementById('favourite_content')
        const id_palettes = event.target.dataset.id
        let palette = document.getElementById(id_palettes);
        let xhr = new XMLHttpRequest();
        xhr.open("POST", '/delete-palettes')
        xhr.withCredentials = true
        xhr.setRequestHeader('Content-Type', 'application/json')
        xhr.send(JSON.stringify({'id_palettes': id_palettes}))
        palette.remove()
    })
})
likes.forEach((like) => {
    like.addEventListener('click', (event) => {
        let el = event.target
        let text = el.textContent
        const id_palette = event.target.dataset.id
        let user_id = document.querySelectorAll('.nav_action_item')[1].dataset.type
        let xhr = new XMLHttpRequest();
        xhr.open("POST", '/liked_palettes')
        xhr.withCredentials = true
        xhr.setRequestHeader('Content-Type', 'application/json')
        let isDel = false
        if (el.classList.contains('fa-solid')) {
            text = parseInt(text)
            isDel = true
            if (text == 1){
                el.textContent = ''
            }
            else{
                el.textContent = text - 1

            }
        }

        else {
            isDel = false
            if (text){
                text = parseInt(text)
                el.textContent = text + 1
            }
            else{
                el.textContent = 1
            }
        }
        el.classList.toggle("fa-solid")
        el.classList.toggle('fa-regular')
        xhr.send(JSON.stringify({"user_id": user_id, 'id_palette':id_palette , 'is_del': isDel}))
    })
})


palette_col.forEach((col) =>{
    col.addEventListener('click', (evt) => {
        let el = evt.target
        let text = el.dataset.id
        navigator.clipboard.writeText("#" + text)
        let classes = toast.classList
        classes.remove('toast_hide')
        toast.classList.remove('animation_hiding')
        console.log(classes)
        setTimeout(delete_window, 2000);
        // toast.classList.toggle('toast_hide')
    })
})



let delete_window = function() {
    toast.classList.add('animation_hiding')
}


