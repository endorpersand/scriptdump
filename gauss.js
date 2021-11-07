class Matrix {
    constructor(arr) {
        this.value = arr;
        this.rows = arr.length;
        this.cols = arr[0].length;
        this.display()
    }

    display() {
        let pad = Math.max.apply(null, this.value.flat().map(x => x.toString().length));
        console.log(pad)
        console.log('|' + this.value.map(x => x.map(y => y.toString().padStart(pad, ' ')).join(' ')).join('|\n|') + '|')
        return this.value;
    }
    get(row, col) {
        return this.value[row][col];
    }
    rowSet(row, setval) {
        this.value[row] = setval;
    }
    rowScale(row, scalar) {
        this.value[row] = this.value[row].map(x => x * scalar);
    }
    rowAdd(row1, row2) {
        return this.value[row1].map((x, i) => x + this.value[row2][i])
    }
    rowSubtract(row1, row2, scalar = 1) {
        return this.value[row1].map((x, i) => x - this.value[row2][i] * scalar)
    }
    rowDivide(row, scalar) {
        return this.value[row].map(x => x / scalar)
    }
}

function solve(arr) {
    let matrix = new Matrix(arr);
    if (matrix.rows !== matrix.cols - 1) throw new Error();
    for (var j = 0; j < matrix.cols - 1; j++) {
        matrix.rowScale(j, 1 / matrix.get(j, j));
        for (var i = 0; i < matrix.rows; i++) {
            if (i === j) continue;
            matrix.rowSet(i, matrix.rowSubtract(i, j, matrix.get(i, j)))
        }
    }
    let result = matrix.value.map(x => x[x.length - 1])
    return result;

}