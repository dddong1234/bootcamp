// 할일을 입력하고 추가버튼을 누르면
// 할일 목록에 할 일이 추가되어야 함

const todoInput = document.querySelector('#todo-input');
const addBtn = document.querySelector('#add-btn');
const todoList = document.querySelector('#todo-list');
let todos = []
const savedTodos =JSON.parse(localStorage.getItem('todos'))

//전체 todo를 화면에 그리는 함수
function renderTodos(){
    for (const [index,todo] of todos.entries()) {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.textContent = todo
    
        const btn = document.createElement('button');
        btn.className = 'btn btn-danger btn-sm'
        btn.textContent = '삭제'
            
        btn.addEventListener('click', () => {
            
        })
        li.appendChild(btn)
        todoList.appendChild(li)
    }
}

function saveTodos(){
    localStorage.setItem('todos',JSON.stringify(todos))
}

function deleteTodo(index){
    todos.splice(index,1)
    renderTodos()
    saveTodos()
}



if(savedTodos){
    todos = savedTodos
    renderTodos()
}

// 할일 추가
addBtn.addEventListener('click', () => {
    const todo = todoInput.value.trim();
    if (todo === '') {
        alert('할 일을 입력해주세요.')
        return
    }
    
    todos.push(todo)
    renderTodos()
    localStorage.setItem('todos',JSON.stringify(todos))
    
    todoInput.value = '';
})