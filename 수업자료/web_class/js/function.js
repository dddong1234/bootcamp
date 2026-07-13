function sayHello(){

    console.log("Hello");

}
let result = sayHello;
console.log(typeof result());

function run(fn){
    fn();
}

run(sayHello)