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
type DAToString<A extends number[]> =
    A extends [0, ...infer A2 extends number[]] ?
        A2 extends [] ? "0" : DAToString<A2>
    : Concat<A>

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
// Add two digits (optionally with carry), ranges from 0-19
type _Add1<A extends number, B extends number, C extends boolean = false> = 
    [...Digits[A], ...Digits[B], ...(C extends true ? [0] : [])]["length"] extends (infer R extends number) ?
        R
    : never;
// Add an array of digits (optionally with a carry value)
type _AddZ<A extends number[], B extends number[], C extends boolean = false> =
    A extends [...infer A1 extends number[], infer A2 extends number] ?
        B extends [...infer B1 extends number[], infer B2 extends number] ?
            SplitN<_Add1<A2, B2, C>> extends [...infer N1 extends number[], infer N2 extends number] ?
                [..._AddZ<A1, B1, N1 extends [] ? false : true>, N2]
            : never
        : C extends true ? _AddZ<A, [1]> : A
    : C extends true ? _AddZ<B, [1]> : B;

// Actual addition types
type AddN<A extends number, B extends number> = ParseInt<DAToString<_AddZ<SplitN<A>, SplitN<B>>>>;
type AddB<A extends bigint, B extends bigint> = ParseBigInt<DAToString<_AddZ<SplitN<A>, SplitN<B>>>>;
type Add<A extends number | bigint, B extends number | bigint> =
    [A, B] extends [infer A extends number, infer B extends number] ?
        AddN<A, B>
    : [A, B] extends [infer A extends bigint, infer B extends bigint] ?
        AddB<A, B>
    : never;
// Doubling type
type Double<A extends number | bigint> = Add<A, A>;

type IsEven<N extends Stringable> = `${N}` extends `${string}${0 | 2 | 4 | 6 | 8}` ? true : false;
type IsOdd<N extends Stringable> = IsEven<N> extends false ? true : false;

type _HalfDS<D extends string, C extends boolean> =
    C extends true ?
        D extends `${8 | 9}` ? 9 :
        D extends `${6 | 7}` ? 8 :
        D extends `${4 | 5}` ? 7 :
        D extends `${2 | 3}` ? 6 :
        D extends `${0 | 1}` ? 5 :
        never
    :
        D extends `${8 | 9}` ? 4 :
        D extends `${6 | 7}` ? 3 :
        D extends `${4 | 5}` ? 2 :
        D extends `${2 | 3}` ? 1 :
        D extends `${0 | 1}` ? 0 :
        never;
type _HalfS<A extends string, C extends boolean = false> =
A extends `${infer D}${infer R}` ? 
    [
        _HalfDS<D, C>,
        ..._HalfS<R, IsOdd<D>>
    ]
: [];
type HalfN<A extends number> = ParseInt<DAToString<_HalfS<`${A}`>>>;
type HalfB<A extends bigint> = ParseBigInt<DAToString<_HalfS<`${A}`>>>;
type Half<A extends number | bigint> =
    A extends number ?
        HalfN<A>
    : A extends bigint ?
        HalfB<A>
    : never;

type Mul<A extends number | bigint, B extends number | bigint> =
    B extends (0 | 0n) ? 
        B
    : B extends (1 | 1n) ? 
        A 
    : A extends (0 | 0n) ? 
        A
    : A extends (1 | 1n) ? 
        B 
    : IsEven<B> extends true ?
        Mul<Double<A>, Half<B>>
    : Add<Mul<Double<A>, Half<B>>, A>;

namespace Compare {
    export type Le<A extends number | bigint, B extends number | bigint> =
        never

    export type Ge<A extends number | bigint, B extends number | bigint> =
        never

    export type Eq<A extends number | bigint, B extends number | bigint> = 
        A extends B ?
            B extends A ? true : false 
        : false;

    export type Lt<A extends number | bigint, B extends number | bigint> =
        [Le<A, B>, Eq<A, B>] extends [true, false] ?
            true
        : false;

    export type Gt<A extends number | bigint, B extends number | bigint> =
        [Ge<A, B>, Eq<A, B>] extends [true, false] ?
            true
        : false;
}

let q: Compare.Eq<Mul<293842234029374238n, 1028312038120131n>, 302161506560518335958659800585178n>;