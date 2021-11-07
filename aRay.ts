type IndexFn<T> = (i: number) => T;
type Mapper<T, R> = (n: T, i: number) => R;

class FunctionList<T> {
    mapper: IndexFn<T>;
    length?: number;
    
    constructor(mapper: IndexFn<T>, length?: number) {
        this.mapper = mapper;
        this.length = length;
    }

    get(i: number) {
        if (i < 0) return undefined;
        if (typeof this.length == "number" && i >= this.length) return undefined;
        return this.mapper(i);
    }

    *[Symbol.iterator]() {
        let i = 0;
        while (true) {
            yield this.get(i++) as T;
            if (typeof this.length == "number" && i >= this.length) return;
        }
    }

    map<U>(map: Mapper<T, U>) {
        let mapper = this.mapper;
        return new FunctionList(function(i: number) {
            return map(mapper(i), i);
        }, this.length);
    }

    entries() {
        return this.map((n, i) => [i, n])[Symbol.iterator]();
    }

    any(pred: Mapper<T, boolean>) {
        return this.some(pred);
    }

    all(pred: Mapper<T, boolean>) {
        return this.every(pred);
    }

    some(pred: Mapper<T, boolean>) {
        if (typeof this.length === "undefined") throw TypeError("Cannot check infinite list");
        let i = 0;
        for (let x of this[Symbol.iterator]()) {
            if (pred(x, i++)) return true;
        }
        return false;
    }

    every(pred: Mapper<T, boolean>) {
        if (typeof this.length === "undefined") throw TypeError("Cannot check infinite list");
        let i = 0;
        for (let x of this[Symbol.iterator]()) {
            if (!pred(x, i++)) return false;
        }
        return true;
    }

    static fromArray<T>(array: T[]) {
        return new FunctionList(i => array[i], array.length)
    }

    toArray() {
        return [...this];
    }
}