function tokenize(expression) {
	const cleaned = expression.replace(/\s+/g, "");
	const tokens = [];
	let currentNumber = "";

	for (let i = 0; i < cleaned.length; i += 1) {
		const char = cleaned[i];
		const prevToken = tokens[tokens.length - 1];
		const isUnaryMinus = char === "-" && (i === 0 || ["+", "-", "*", "/"].includes(prevToken));

		if (/\d|\./.test(char) || isUnaryMinus) {
			currentNumber += char;
			continue;
		}

		if (!["+", "-", "*", "/"].includes(char)) {
			throw new Error(`지원하지 않는 문자: ${char}`);
		}

		if (currentNumber === "") {
			throw new Error("잘못된 수식입니다.");
		}

		tokens.push(currentNumber, char);
		currentNumber = "";
	}

	if (currentNumber === "") {
		throw new Error("수식이 연산자로 끝날 수 없습니다.");
	}

	tokens.push(currentNumber);
	return tokens;
}

function precedence(operator) {
	if (operator === "+" || operator === "-") {
		return 1;
	}

	if (operator === "*" || operator === "/") {
		return 2;
	}

	return 0;
}

function applyOperator(numbers, operator) {
	if (numbers.length < 2) {
		throw new Error("잘못된 수식입니다.");
	}

	const right = numbers.pop();
	const left = numbers.pop();

	if (operator === "+") {
		numbers.push(left + right);
		return;
	}

	if (operator === "-") {
		numbers.push(left - right);
		return;
	}

	if (operator === "*") {
		numbers.push(left * right);
		return;
	}

	if (operator === "/") {
		if (right === 0) {
			throw new Error("0으로 나눌 수 없습니다.");
		}

		numbers.push(left / right);
	}
}

function calculateExpression(expression) {
	const tokens = tokenize(expression);
	const numbers = [];
	const operators = [];

	for (const token of tokens) {
		if (!Number.isNaN(Number(token))) {
			numbers.push(Number(token));
			continue;
		}

		while (
			operators.length > 0 &&
			precedence(operators[operators.length - 1]) >= precedence(token)
		) {
			applyOperator(numbers, operators.pop());
		}

		operators.push(token);
	}

	while (operators.length > 0) {
		applyOperator(numbers, operators.pop());
	}

	if (numbers.length !== 1) {
		throw new Error("계산에 실패했습니다.");
	}

	return numbers[0];
}

function start() {
	alert("계산기를 시작합니다. 예: 12+3*4-6/2");

	while (true) {
		const expression = prompt("계산식을 입력하세요. 종료하려면 취소를 누르세요.");

		if (expression === null) {
			console.log("계산기를 종료합니다.");
			break;
		}

		if (expression.trim() === "") {
			alert("빈 수식은 계산할 수 없습니다.");
			continue;
		}

		try {
			const result = calculateExpression(expression);
			console.log(`${expression} = ${result}`);
			alert(`${expression} = ${result}`);
		} catch (error) {
			alert(error.message);
			console.error(error.message);
		}
	}
}
