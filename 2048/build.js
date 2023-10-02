const array = [];
let start = false;
let array_record = [[4, 4, 4, 4], [4, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
const step = document.getElementById('step');

for (let i = 0; i < 4; i++) {
    array[i] = [];
    for (let j = 0; j < 4; j++) array[i][j] = document.getElementById(`${i}${j}`);
}

const getRandomInt = (max) => {
    return Math.floor(Math.random() * Math.ceil(max));
}

const createRandomPosition = () => {
    while (true) {
        const x = getRandomInt(4);
        const y = getRandomInt(4);
        if (array_record[x][y] === 0) {
            const n = getRandomInt(2) === 0 ? 2 : 4;
            array_record[x][y] = n;
            array[x][y].textContent = n;
            break;
        }
    }
}

const empty = () => {
    array.forEach(arr => arr.forEach(element => element.textContent = ''));
    array_record = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
    step.textContent = '0';
}

document.getElementById('start').addEventListener('click', e => {
    // e.preventDefault();
    // empty();
    // start = true;
    // createRandomPosition();
    // createRandomPosition();
})

document.getElementById('reset').addEventListener('click', e => {
    e.preventDefault();
    empty();
})


document.addEventListener('keydown', e => {
    // if (!start) return;

    let move = false;
    let empty = false;


    switch (e.key) {
        case 'w': case 'ArrowUp':
            for (let i = 3; i >= 0; i--) {
                for (let j = 1; j < 4; j++) {
                    if (array_record[j][i] !== 0) {
                        let check = true;
                        for (let k = 0; k < j; k++) {
                            if (array_record[k][i] === 0) {
                                if (k > 0 && array_record[j][i] === array_record[k - 1][i]) array_record[k - 1][i] *= 2;
                                else array_record[k][i] = array_record[j][i];
                                array_record[j][i] = 0;
                                check = false;
                                break
                            }
                        }

                        if (check && j > 0 && array_record[j][i] === array_record[j - 1][i]) {
                            array_record[j - 1][i] *= 2;
                            array_record[j][i] = 0;
                        }
                    }
                }
            }
            break;
        case 's': case 'ArrowDown':
            for (let i = 0; i < 4; i++) {
                for (let j = 2; j >= 0; j--) {
                    if (array_record[j][i] !== 0) {
                        let check = true;
                        for (let k = 3; k > j; k--) {
                            if (array_record[k][i] === 0) {
                                if (k < 3 && array_record[j][i] === array_record[k + 1][i]) array_record[k + 1][i] *= 2;
                                else array_record[k][i] = array_record[j][i];
                                array_record[j][i] = 0;
                                check = false;
                                break
                            }
                        }

                        if (check && j < 3 && array_record[j][i] === array_record[j + 1][i]) {
                            array_record[j + 1][i] *= 2;
                            array_record[j][i] = 0;
                        }
                    }
                }
            }
            break;
        case 'a': case 'ArrowLeft':
            for (let i = 3; i >= 0; i--) {
                for (let j = 1; j < 4; j++) {
                    if (array_record[i][j] !== 0) {
                        let check = true;
                        for (let k = 0; k < j; k++) {
                            if (array_record[i][k] === 0) {
                                if (k > 0 && array_record[i][j] === array_record[i][k - 1]) array_record[i][k - 1] *= 2;
                                else array_record[i][k] = array_record[i][j];
                                array_record[i][j] = 0;
                                check = false;
                                break
                            }
                        }

                        if (check && j > 0 && array_record[i][j] === array_record[i][j - 1]) {
                            array_record[i][j - 1] *= 2;
                            array_record[i][j] = 0;
                        }
                    }
                }
            }
            break;
        case 'd': case 'ArrowRight':
            for (let i = 0; i < 4; i++) {
                for (let j = 2; j >= 0; j--) {
                    if (array_record[i][j] !== 0) {
                        let check = true;
                        for (let k = 3; k > j; k--) {
                            if (array_record[i][k] === 0) {
                                if (k < 3 && array_record[i][j] === array_record[i][k + 1]) array_record[i][k + 1] *= 2;
                                else array_record[i][k] = array_record[i][j];
                                array_record[i][j] = 0;
                                check = false;
                                break
                            }
                        }

                        if (check && j < 3 && array_record[i][j] === array_record[i][j + 1]) {
                            array_record[i][j + 1] *= 2;
                            array_record[i][j] = 0;
                        }
                    }
                }
            }
            break;
    }
    for (let i = 0; i < 4; i++) {
        console.log(array_record[i]);
    }

    // jiancha
    // createRandomPosition();
})