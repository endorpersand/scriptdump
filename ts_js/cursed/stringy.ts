export {}

type ParseInt<S extends string> = S extends `${infer N extends number}` ? N : never;
type ParseBigInt<S extends string> = S extends `${infer N extends bigint}` ? N : never;
type IntToBigInt<N extends number> = ParseBigInt<`${N}`>;

type Stringable = string | number | bigint | boolean | null | undefined;
type Concat<S extends Stringable[]> =
    S extends [infer S1 extends Stringable, ...infer S2 extends Stringable[]] ?
        `${S1}${Concat<S2>}`
    : "";
type SplitS<S extends string> =
    S extends `${infer C}${infer R}` ?
        [`${C}`, ...SplitS<R>]
    : [];
type ToDigitArray<S extends string[]> =
    S extends [infer S1 extends string, ...infer S2 extends string[]] ?
        [ParseInt<S1>, ...ToDigitArray<S2>]
    : [];
type SplitN<N extends number | bigint> = ToDigitArray<SplitS<`${N}`>>
let b: SplitN<1347823044992342342347239472397n>;
type Digits = [
    [],
    [0],
    [0, 0],
    [0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
];
// Add two digits
type _Add1<A extends number, B extends number> = 
    [...Digits[A], ...Digits[B]]["length"] extends number ?
        [...Digits[A], ...Digits[B]]["length"]
    : never;
// Add an array of digits (optionally with a carry value)
type _AddZ<A extends number[], B extends number[], C extends boolean = false> =
    A extends [...infer A1 extends number[], infer A2 extends number] ?
        B extends [...infer B1 extends number[], infer B2 extends number] ?
            // Adding with carry
            SplitN<_Add1<A2, B2>> extends [...infer N1 extends number[], infer N2 extends number] ?
                [..._AddZ<A1, B1, N1 extends [] ? false : true>, C extends true ? _Add1<N2, 1> : N2]
            : never
        : C extends true ? _AddZ<A, [1]> : A
    : C extends true ? _AddZ<B, [1]> : B;

// Actual addition types
type Add<A extends number, B extends number> = ParseInt<Concat<_AddZ<SplitN<A>, SplitN<B>>>>;
type AddB<A extends bigint, B extends bigint> = ParseBigInt<Concat<_AddZ<SplitN<A>, SplitN<B>>>>;
// Doubling type
type Double<A extends number> = Add<A, A>;
type DoubleB<A extends bigint> = AddB<A, A>;

let a: AddB<1234234230482n, 9992342342342399n>;