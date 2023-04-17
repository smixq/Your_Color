let likes = document.querySelectorAll('span')

likes.forEach((like)=>{
    like.addEventListener('click', (event) => {
        let el = event.target
        let i = parseInt(el.textContent)
        el.textContent = i += 1
        let xhr = new XMLHttpRequest();
        let id = el.dataset.id
        xhr.open("POST", `sute.ru/add-like`)
        xhr.withCredentials = true
        xhr.send({id: id, user_id: user_id})
    })
})