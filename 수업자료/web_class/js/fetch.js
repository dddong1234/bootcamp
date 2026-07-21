
// get 요청
// fetch('https://jsonplaceholder.typicode.com/posts')
//   .then(response => response.json())
//   .then(data => console.log(data))

// post 요청
fetch('https://jsonplaceholder.typicode.com/posts',
    {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({
            title: 'python',
            body: 'hello python',
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))