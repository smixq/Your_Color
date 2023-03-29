console.log(1)
const col = document.querySelectorAll('.col')
document.addEventListener('click', (evt)=>{
    evt.preventDefault()
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
})


// типо лямбда функция 
// слева в круглых скобках необходимые аргументы, а справа в фигурных тело функции
document.addEventListener('keydown', (evt)=>{
    evt.preventDefault()
    if(evt.code === 'Space'){
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


// настраиваем колонки 
function setRandomColors (){
    col.forEach((col)=>{
        const isLocked = col.querySelector('i').classList.contains('fa-lock')
        if (isLocked){
            return
        }
        const text = col.querySelector('h2')
        const color =  generateRandomColor()
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
setRandomColors()