/*
 * creation: Nov 19, 2020?
 *
 * Dunno. I think I just went "what if primitive types were boxed in a way that could be accessible" 
 * and then it spiraled out of control.
 * Have a box and a bunch of random stuff under the box too.
 */


let ops = {
    "+": function (a, b) {return a.valueOf() + b.valueOf()},
    "-": function (a, b) {return a.valueOf() - b.valueOf()},
    "*": function (a, b) {return a.valueOf() * b.valueOf()},
    "/": function (a, b) {return a.valueOf() / b.valueOf()},
    "%": function (a, b) {return a.valueOf() % b.valueOf()},
    "**": function (a, b) {return a.valueOf() ** b.valueOf()},
    "<<": function (a, b) {return a.valueOf() << b.valueOf()},
    ">>": function (a, b) {return a.valueOf() >> b.valueOf()},
    ">>>": function (a, b) {return a.valueOf() >>> b.valueOf()},
}
class Box {
    #value;
    constructor(v) {
        this.#value = v.valueOf();
        this.#value = this.handle(this.#value);
        if (typeof this.#value === "object" || typeof this.#value === "undefined") throw TypeError("Object does not need to be boxed");
    };
    valueOf() {return this.#value}; 
    toString() {return this.#value.toString()};
    get type() {return typeof this.#value;}
    handle(self) {return self;}
}

class MutBox {
    #value;
    constructor(v) {
        this.set(v);
    };

    valueOf() {return this.#value}; 
    toString() {return this.#value.toString()};
    get type() {return typeof this.#value;}
    set(v) {
        this.#value = v.valueOf();
        this.#value = this.handle(this.#value);
        if (typeof this.#value === "object" || typeof this.#value === "undefined") throw TypeError("Object does not need to be boxed");
        return this;
    };
    handle(self) {return self;}
}

class Integer extends Box {
    handle(self) {
        return Math.trunc(+self);
    }
}

for (let [o, f] of Object.entries(ops)) {
    Box.prototype[o] = function (a) { return new this.constructor(f(this,a)) };
    MutBox.prototype[o] = function (a) { return this.set(f(this,a)) };
}

box = v => new Box(v);
mutbox = v => new MutBox(v);
int = v => new Integer(v);

/*
class Interface {
    static requiredMethod = Symbol("required method");
    static requiredField = Symbol("required field");
    implementProps = {};
    constructor(o) {
        Object.assign(this.implementProps, o);
    }
}

function Implementation(...interfaces) {
    let Impl = class { };
    let rferr = () => new ReferenceError("Field not yet implemented");
    let rmerr = () => new ReferenceError("Method not yet implemented");
    for (var i of interfaces) {
        if (!(i instanceof Interface)) throw new TypeError("Only interfaces can be implemented.")
        for (var p of Object.getOwnPropertyNames(i)) {
            if (i[p] === Interface.requiredField) Impl.prototype[p] = rferr;
            else if (i[p] === Interface.requiredMethod) Impl.prototype[p] = rmerr;
            else Impl.prototype[p] = i[p];
        }

        Impl.constructor = function () {
            for (var p of Object.getOwnPropertyNames(this)) {
                if (p === rferr) p();
                else if (p === rmerr) p();
            }
        };
    }
    return Impl;
}
*/

class Stream {
    #iterable;
    constructor(iterable) {
        this.#iterable = iterable[Symbol.iterator]();
    }

    *#nulliter() {
        return;
    }

    static #concatiters(a, b) {
        function* iter() {
            for (let x of a) yield x;
            for (let x of b) yield x;
        }
        return iter();
    }

    static range(start, stop) {
        return new Stream(function* () {
            for (let i = start; i < stop; i++) {
                yield i;
            }
        });
    }

    map(callback = x=>x) {
        function* iter() {
            for (let e of this.#iterable) {
                yield callback(e);
            }
        }
        return new Stream(iter.bind(this)());
    }

    filter(callback = _=>true) {
        function* iter() {
            for (let e of this.#iterable) {
                if (callback(e)) {
                    yield e;
                }
            }
        }
        return new Stream(iter.bind(this)());
    }

    exist() {
        function* iter() {
            for (let e of this.#iterable) {
                if (typeof e !== "undefined") yield e;
            }
        }

        return new Stream(iter.bind(this)());
    }

    next() {
        let v = this.#iterable.next().value;
        return v;
    }

    reduce(callback = (_, cv) => cv, df) {
        let acc = df ?? this.#iterable.next().value;
        for (let e of this.#iterable) {
            acc = callback(acc, e);
        }
        return acc;
    }

    unique() {
        function* iter() {
            let values = [];
            for (let e of this.#iterable) {
                if (!values.includes(e)) {
                    values.push(e);
                    yield e;
                }
            }
        }

        return new Stream(iter.bind(this)());
    }

    consume(callback = _ => {}) {
        for (let e of this.#iterable) {
            callback(e);
        }
    }

    zip(stream) {
        function* iter(a,b) {
            let av = a.next(), bv = b.next();
            while (!av.done && !bv.done) {
                yield [av.value, bv.value];
                av = a.next(), bv = b.next();
            }
        }
        return new Stream(iter(this.#iterable, stream.#iterable));
    }


    [Symbol.iterator]() {
        return this.#iterable;
    }
}