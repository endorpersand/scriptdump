/*
 * creation: February 13-15, 2021
 *
 * Implementation of Stream (from Java) in TS
 * Not too interesting but I like the type stuff here
 */

type GeneratorFn<T> = (() => Generator<T>);
type Streamable<T> = IterableIterator<T> | Iterable<T> | GeneratorFn<T> | Stream<T>;

class Stream<T> implements IterableIterator<T> {
    private iterator: IterableIterator<T>;

    private constructor(iter?: IterableIterator<T>) {
        if (typeof iter === "undefined") {
            this.iterator = [].values();
        } else {
            this.iterator = iter;
        }
    }

    static of<T>(iter: Streamable<T>): Stream<T> {
        if (iter instanceof Stream) {
            return iter;
        }
        if (iter instanceof Function) {
            return new Stream(iter());
        }

        if ("next" in iter) {
            return new Stream(iter);
        }

        return new Stream(
            Object.assign(
                iter[Symbol.iterator](), {
                    [Symbol.iterator]() {
                        return this;
                    }
                }
            )
        );
    }

    static element<T>(item?: T): Stream<T> {
        if (typeof item === "undefined") return Stream.ofElements();
        return Stream.ofElements(item);
    }

    static ofElements<T>(...items: T[]) {
        return Stream.of(items);
    }

    private pop() {
        let iter = this.iterator;
        this.iterator = function* () {
            while (true) throw new TypeError("Cannot use consumed stream");
        }();
        return iter;
    }

    private moveStream<U>(map: (iter: IterableIterator<T>) => IterableIterator<U>) {
        return Stream.of(map(this.pop()));
    }

    next() {
        return this.iterator.next();
    }

    [Symbol.iterator]() {
        return this;
    }

    // lazy intermediate
    map<U>(callback: (item: T) => U): Stream<U> {
        function* iterator(iter: IterableIterator<T>) {
            for (let item of iter) {
                yield callback(item);
            }
        }

        return this.moveStream(iterator);
    }

    // lazy intermediate
    flatMap<U>(callback: (item: T) => (U | Stream<U>)): Stream<U> {
        function* iterator(iter: IterableIterator<T>) {
            for (let item of iter) {
                let cb = callback(item);
                if (cb instanceof Stream) {
                    for (let cbi of cb) {
                        yield cbi;
                    }
                } else {
                    yield cb;
                }
            }
        }

        return this.moveStream(iterator);
    }

    // lazy intermediate
    filter(callback: (item: T) => boolean): Stream<T> {
        function* iterator(iter: IterableIterator<T>) {
            for (let item of iter) {
                if (callback(item)) {
                    yield item;
                }
            }
        }

        return this.moveStream(iterator);
    }

    // lazy generator
    static concat<U>(...streams: (U|Stream<U>)[]): Stream<U> {
        function* iterator() {
            for (let u of streams) {
                if (u instanceof Stream) {
                    for (let item of u.pop()) yield item;
                } else {
                    yield u;
                }
            }
        }

        return Stream.of(iterator);
    }

    // lazy generator
    append<U>(...values: (U | Stream<U>)[]): Stream<T|U> {
        return Stream.concat<T|U>(this, ...values);
    }

    //lazy generator
    prepend<U>(...values: (U|Stream<U>)[]): Stream<T|U> {
       return Stream.concat<T|U>(...values, this);
    }

    // eager terminal
    collect() {
        return [...this.pop()];
    }

    // lazy intermediate
    accumulate<U>(callback: (acc: U, cv: T) => U, defaultValue: U): Stream<U> {
        function* iterator(iter: IterableIterator<T>) {
            let acc = defaultValue;

            yield acc;
            for (let cv of iter) {
                yield acc = callback(acc, cv);
            }
        }

        return this.moveStream(iterator);
    }

    // eager terminal
    reduce<U>(callback: (acc: U, cv: T) => U, defaultValue: U): U {
        let acc = defaultValue;

        for (let cv of this.pop()) {
            acc = callback(acc, cv);
        }

        return acc;
    }

    // lazy terminal/intermediate
    tee(n: number = 2): Stream<T>[] {
        let lists = Array.from(Array(n), () => [] as T[]);
        let iter = this.pop();
        function* iterator(deque: T[]) {
            while (true) {
                if (deque.length == 0) {
                    let nv = iter.next();
                    if (nv.done) return;
                    for (let list of lists) list.push(nv.value);
                }
                yield deque.shift() as T;
            }
        }

        return lists.map(l => Stream.of(iterator(l)));
    }

    // eager terminal
    count() {
        return this.map(_ => 1).reduce((acc, cv) => acc + cv, 0);
    }

    // lazy intermediate
    enumerate() {
        function* iterator(iter: IterableIterator<T>): Generator<[number, T]> {
            let i = 0;
            for (let item of iter) {
                yield [i++, item];
            }
        }

        return this.moveStream(iterator);
    }

    // lazy intermediate
    drop(size: number) {
        function* iterator(iter: IterableIterator<T>) {
            for (let i = 0; i < size; i++) {
                iter.next();
            }
            for (let item of iter) yield item;
        }

        return this.moveStream(iterator);
    }

    // lazy intermediate
    take(size: number) {
        function* iterator(iter: IterableIterator<T>) {
            let i = 0;
            for (let item of iter) {
                yield item;
                if (++i >= size) return;
            }
        }

        return this.moveStream(iterator);
    }

    // lazy intermediate
    dropWhile(callback: (v: T) => boolean) {
        function* iterator(iter: IterableIterator<T>) {
            let read = false;
            for (let item of iter) {
                if (!callback(item)) read = true;
                if (read) yield item;
            }
        }

        return this.moveStream(iterator);
    }

    // lazy intermediate
    takeWhile(callback: (v: T) => boolean) {
        function* iterator(iter: IterableIterator<T>) {
            for (let item of iter) {
                if (!callback(item)) return;
                yield item;
            }
        }

        return this.moveStream(iterator);
    }

    // lazy terminal
    all(callback: (v: T) => boolean) {
        return this.every(callback);
    }

    // lazy terminal
    every(callback: (v: T) => boolean) {
        for (let item of this) {
            if (!callback(item)) return false;
        }
        return true;
    }

    // lazy terminal
    any(callback: (v: T) => boolean) {
        return this.some(callback);
    }

    // lazy terminal
    some(callback: (v: T) => boolean) {
        for (let item of this) {
            if (callback(item)) return true;
        }
        return false;
    }

    // lazy intermediate
    unique() {
        function* iterator(iter: IterableIterator<T>) {
            let itemSet: Set<T> = new Set();

            for (let item of iter) {
                if (itemSet.has(item)) continue;
                itemSet.add(item);
                yield item;
            }
        }
       
        return this.moveStream(iterator);
    }

    // eager terminal
    forEach(callback: (item: T) => void) {
        for (let item of this.pop()) callback(item);
    }
    
    // lazy generator
    // T: [A, B, C, D, ...], streamables: [Streamable<A>, Streamable<B>, Streamable<C>, Streamable<D>, ...]
    static zip<T extends unknown[]>(...streamables: {[I in keyof T]: Stream<T[I]>}): Stream<T> {
        let streams = streamables.map(s => Stream.of(s)) // streams: [Stream<A>, Stream<B>, Stream<C>, Stream<D>, ...]
        let iters = streams.map(s => s.pop()) // iters: [IterableIterator<A>, IterableIterator<B>, IterableIterator<C>, IterableIterator<D>, ...]
        function* iterator() {
            let nv = iters.map(s => s.next()); // nv: [IteratorResult<A>, IteratorResult<B>, IteratorResult<C>, IteratorResult<D>, ...]
            
            while (!nv.some(r => r.done)) {
                yield nv.map(r => (r as IteratorYieldResult<T>).value) as T; // .value: [A, B, C, D, ...]
                nv = iters.map(s => s.next());
            }
        }

        return Stream.of(iterator);
    }
    
    // lazy intermediate
    peek(callback: (item: T) => void) {
        function* iterator(iter: IterableIterator<T>) {
            for (let item of iter) {
                callback(item);
                yield item;
            }
        }
        return this.moveStream(iterator);
    }

    // lazy generator
    static range(start: number, stop?: number, step: number=1) {
        let b: number, e: number;
        if (typeof stop === "undefined") {
            b = 0;
            e = start;
        } else {
            b = start;
            e = stop;
        }

        return Stream.of(function*() {
            let i = b;
            while (true) {
                yield i;
                i += step;
            }
        })
        .takeWhile(i => i * Math.sign(step) < e * Math.sign(step));
    }

    // lazy intermediate
    repeat(n: number = Infinity) {
        function* iterator(iter: IterableIterator<T>) {
            if (n < 1) return;
            let seq: T[] = [];

            for (let item of iter) {
                seq.push(item);
                yield item;
            }

            for (let _ = 1; _ < n; _++) {
                for (let item of seq) {
                    yield item;
                }
            }
        }

        return this.moveStream(iterator);
    }

    compress(iter: Streamable<number>) {
        return Stream.zip(this, Stream.of(iter))
            .flatMap(([t, i]) => 
                Stream.element(t)
                    .repeat(i)
            );
    }
}