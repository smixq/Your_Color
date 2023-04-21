let buttons = document.querySelectorAll('.delete_favourite_button')
let likes = document.querySelectorAll('.like')
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
        block.removeChild(palette)
    })
})
console.log(likes)
likes.forEach((like) => {
    like.addEventListener('click', (event) => {
        let el = event.target
        const id_palette = event.target.dataset.id
        let user_id = document.querySelectorAll('.nav_action_item')[1].dataset.type
        let xhr = new XMLHttpRequest();
        xhr.open("POST", '/liked_palettes')
        xhr.withCredentials = true
        xhr.setRequestHeader('Content-Type', 'application/json')
        let isDel
        if (el.classList.contains('fa-solid')) {
            isDel = true
        }
        else {
            isDel = false
        }
        el.classList.toggle("fa-solid")
        el.classList.toggle('fa-regular')
        xhr.send(JSON.stringify({"user_id": user_id, 'id_palette':id_palette , 'is_del': isDel}))
    })
})
