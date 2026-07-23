const display = document.querySelector("#display");
const buttons = document.querySelectorAll(".buttons button");
const powerButton = document.querySelector(".on-off");

let isPowerOn = false;
let currentExpression = "";

function updateDisplay(value) {
	display.value = value;
}

function setPowerState(nextState) {
	isPowerOn = nextState;
	powerButton.classList.toggle("on", isPowerOn);
	updateDisplay(isPowerOn ? currentExpression || "0" : "OFF");
}

function togglePower() {
	if (isPowerOn) {
		currentExpression = "";
		setPowerState(false);
		return;
	}

	currentExpression = "";
	setPowerState(true);
}

function clearDisplay() {
	if (!isPowerOn) {
		return;
	}

	currentExpression = "";
	updateDisplay("0");
}

function appendNumber(number) {
	if (!isPowerOn) {
		return;
	}

	if (number === ".") {
		const parts = currentExpression.split(/[\+\-\*\/]/);
		const lastPart = parts[parts.length - 1];

		if (lastPart.includes(".")) {
			return;
		}

		if (currentExpression === "" || /[\+\-\*\/]$/.test(currentExpression)) {
			currentExpression += "0";
		}
	}

	if (currentExpression === "0" && number !== ".") {
		currentExpression = number;
	} else {
		currentExpression += number;
	}

	updateDisplay(currentExpression);
}

function appendOperator(operator) {
	if (!isPowerOn) {
		return;
	}

	if (currentExpression === "") {
		if (operator === "-") {
			currentExpression = "-";
			updateDisplay(currentExpression);
		}
		return;
	}

	if (/[\+\-\*\/]$/.test(currentExpression)) {
		currentExpression = currentExpression.slice(0, -1) + operator;
	} else {
		currentExpression += operator;
	}

	updateDisplay(currentExpression);
}

function tokenize(expression) {
	const tokens = [];
	let number = "";

	for (let index = 0; index < expression.length; index += 1) {
		const char = expression[index];
		const lastToken = tokens[tokens.length - 1];
		const isUnaryMinus =
			char === "-" && (index === 0 || ["+", "-", "*", "/"].includes(lastToken));

		if (/\d|\./.test(char) || isUnaryMinus) {
			number += char;
			continue;
		}

		if (number === "") {
			throw new Error("잘못된 계산식입니다.");
		}

		tokens.push(number, char);
		number = "";
	}

	if (number === "") {
		throw new Error("수식이 연산자로 끝날 수 없습니다.");
	}

	tokens.push(number);
	return tokens;
}

function calculate(tokens, operators) {
	const values = [];
	const ops = [];

	function getPriority(operator) {
		if (operator === "+" || operator === "-") {
			return 1;
		}

		if (operator === "*" || operator === "/") {
			return 2;
		}

		return 0;
	}

	function applyOperator() {
		const right = values.pop();
		const left = values.pop();
		const operator = ops.pop();

		if (operator === "+") {
			values.push(left + right);
			return;
		}

		if (operator === "-") {
			values.push(left - right);
			return;
		}

		if (operator === "*") {
			values.push(left * right);
			return;
		}

		if (right === 0) {
			throw new Error("0으로 나눌 수 없습니다.");
		}

		values.push(left / right);
	}

	for (const token of tokens) {
		if (!operators.includes(token)) {
			values.push(Number(token));
			continue;
		}

		while (ops.length > 0 && getPriority(ops[ops.length - 1]) >= getPriority(token)) {
			applyOperator();
		}

		ops.push(token);
	}

	while (ops.length > 0) {
		applyOperator();
	}

	return values[0];
}

function performCalculate() {
	if (!isPowerOn || currentExpression === "") {
		return;
	}

	try {
		const tokens = tokenize(currentExpression);
		const result = calculate(tokens, ["+", "-", "*", "/"]);
		currentExpression = String(result);
		updateDisplay(currentExpression);
	} catch (error) {
		updateDisplay("Error");
		currentExpression = "";
	}
}

function bindEvents() {
	buttons.forEach((button) => {
		button.removeAttribute("onclick");

		button.addEventListener("click", () => {
			if (button.classList.contains("on-off")) {
				togglePower();
				return;
			}

			if (button.classList.contains("clear")) {
				clearDisplay();
				return;
			}

			if (button.classList.contains("enter")) {
				performCalculate();
				return;
			}

			if (button.classList.contains("operator")) {
				appendOperator(button.textContent.trim());
				return;
			}

			appendNumber(button.textContent.trim());
		});
	});
}

bindEvents();
setPowerState(false);
