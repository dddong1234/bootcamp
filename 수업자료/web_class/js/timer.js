// setTimeout(
//     ()=> console.log("3초 경과"),
//     3000 //ms
// )

let cout = 0;

const timerId = setInterval(
    ()=> {
        if(cout === 5) {
            clearInterval(timerId)
            return;
        }
        console.log("2초마다 반복")
        cout++
    },
    2000
)


