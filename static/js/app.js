let like = document.querySelector('.fa-save')
const col = document.querySelectorAll('.col')


like.addEventListener('click', (event) => {
    let el = event.target
    let xhr = new XMLHttpRequest();
    let user_id = document.querySelectorAll('.nav_action_item')[1].dataset.type
    xhr.open("POST", '/save-palette')
    xhr.withCredentials = true
    xhr.setRequestHeader('Content-Type', 'application/json')
    let colors = []
    col.forEach((col, index)=>{
    let text = col.querySelector('h2')
    colors.push(text.textContent)
    })
    let isDel
    if (el.classList.contains('fas')) {
        isDel = true

    }
    else {

        isDel = false
    }
    el.classList.toggle("fas")
    el.classList.toggle('far')
    xhr.send(JSON.stringify({"user_id": user_id, 'colors': colors, 'is_del': isDel}))

})



document.addEventListener('click', (evt)=>{
    //evt.preventDefault()
    const type = evt.target.dataset.type
    if (type === 'lock'){
        if (evt.target.tagName.toLowerCase() === 'i'){
            var node = evt.target
        }
        else{
            var node = evt.target.children[0]
        }
        
        node.classList.toggle('fa-lock-open')
        node.classList.toggle('fa-lock')
    }
    else if (type ==='copy'){
        copyToClick(evt.target.textContent)
    }
})


// типо лямбда функция 
// слева в круглых скобках необходимые аргументы, а справа в фигурных тело функции
document.addEventListener('keydown', (evt)=>{

    if(evt.code === 'Space'){
        evt.preventDefault()
    if (like.classList.contains('fas')) {
        like.classList.toggle('fas')
        like.classList.toggle('far')
    }
        setRandomColors()
    }
})

// гениратор рандомного хекса
function generateRandomColor(){
    const hexCodes = '0123456789ABCDEF'
    let color = ''
    for (let i = 0; i < 6; i++){
        // Math.random выбирает рандомную дробь от 0 до 1
        color += hexCodes[Math.floor(Math.random() * hexCodes.length)]
    }
    return '#' + color
}

function copyToClick(text){
    return navigator.clipboard.writeText(text)
}


// настраиваем колонки 
function setRandomColors (isInital){
    let colors = []
    let color
    col.forEach((col, index)=>{
        let i_el = col.querySelectorAll('i')
        let isLocked
        if (i_el[0].classList.contains('fa-save')){
            isLocked = i_el[1].classList.contains('fa-lock')
        }
        else{
            isLocked = i_el[0].classList.contains('fa-lock')
        }
        const text = col.querySelector('h2')
        if (isLocked){
            colors.push(text.textContent)
            return
        }
        
        if (isInital){
            if (colors[index]){
                color = colors[index]
            }
            else{
                color =  chroma.random()
            }
        }
    
        else{
            color =  chroma.random()
        }
        
        const btn = col.querySelector('button')
        
        col.style.background = color
        text.textContent = color
        setTextColor(text, color)
        setTextColor(btn, color)
    })

}

// функция подбора цвета для текста 
function setTextColor(text, color){
    // chroma импортируеться в index
    // luminance определяет светлость оттенка который преходит в переменной color
    // luminance принемает значение от 0 до 1
    const luminance = chroma(color).luminance()
    if (luminance < 0.5){
        text.style.color = '#FFFFFF'
    }
    else{
        text.style.color = '#000000'
    }
}

setRandomColors(true)