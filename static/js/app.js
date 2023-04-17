let like = document.querySelector('.like')
const col = document.querySelectorAll('.col')


like.addEventListener('click', (event) => {
    let el = event.target
    el.classList.toggle("fa-solid")
    el.classList.toggle('fa-regular')
    let xhr = new XMLHttpRequest();
    let id = el.dataset.id
    id = 1
    console.log(id)
    let user_id = document.querySelectorAll('.nav_action_item')[1].dataset.type
    console.log(user_id)
    xhr.open("POST", '/add-like')
    xhr.withCredentials = true
    xhr.setRequestHeader('Content-Type', 'application/json')
    let colors = []
    col.forEach((col, index)=>{
    let text = col.querySelector('h2')
    colors.push(text.textContent)
    })
    console.log(colors)
//    console.log(xhr.getResponseHeader('Content-Type'))
    xhr.send(JSON.stringify({"user_id": user_id, 'colors':colors}))
//    console.log(xhr.getResponseHeader('Content-Type'))
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
//    if (isInital){
//        colors = getColorsFromHash()
//    }
//    else{
//        colors = []
//    }
    let color
//    console.log(colors)
    col.forEach((col, index)=>{
        const isLocked = col.querySelector('i').classList.contains('fa-lock')
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
//        if (!isInital){
//            colors.push(color)
//        }
        
        col.style.background = color
        text.textContent = color
        setTextColor(text, color)
        setTextColor(btn, color)
    })

//    updateColorsHash(colors)
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

//function updateColorsHash(colors = []){
//    document.location.hash = colors.map((col) => {
//        return col.toString().substring(1)
//    }).join('-')
//}

//function getColorsFromHash(){
//    if (document.location.hash.length > 1){
//        return document.location.hash.substring(1).split('-').map((color) => '#' + color)
//    }
//    return []
//}
setRandomColors(true)