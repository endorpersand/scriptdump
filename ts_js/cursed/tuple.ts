type Split<S extends string> =
S extends `${infer C}${infer R}` ?
    [`${C}`, ...Split<R>]
: [];

// Binary parsing:
{
    type BitTuple<S extends string[]> =
        S extends [...infer S1 extends string[], infer S2 extends "0" | "1"] ?
            [...BitTuple<S1>, ...BitTuple<S1>, ...S2 extends "1" ? [1] : []]
        : [];
    
    type Decimal<S extends string> = BitTuple<Split<S>>["length"];
    let z: Decimal<"10011100001111"> = 9999;
}

type DigitTuple<S extends string[]> =
    S extends [...infer S1 extends string[], infer S2 extends string] ?
        [
            ...DigitTuple<S1>,
            ...DigitTuple<S1>,
            ...DigitTuple<S1>,
            ...DigitTuple<S1>,
            ...DigitTuple<S1>,
            ...DigitTuple<S1>,
            ...DigitTuple<S1>,
            ...DigitTuple<S1>,
            ...DigitTuple<S1>,
            ...DigitTuple<S1>,
            ...(
                S2 extends "9" ? [1, 1, 1, 1, 1, 1, 1, 1, 1] :
                S2 extends "8" ? [1, 1, 1, 1, 1, 1, 1, 1] :
                S2 extends "7" ? [1, 1, 1, 1, 1, 1, 1] :
                S2 extends "6" ? [1, 1, 1, 1, 1, 1] :
                S2 extends "5" ? [1, 1, 1, 1, 1] :
                S2 extends "4" ? [1, 1, 1, 1] :
                S2 extends "3" ? [1, 1, 1] :
                S2 extends "2" ? [1, 1] :
                S2 extends "1" ? [1] :
                []
            )
        ]
    : [];
type Tupled<N extends number> = DigitTuple<Split<`${N}`>>;

namespace Compare {
    export type Le<A extends number, B extends number> =
        Tupled<B> extends [...Tupled<A>, ...unknown[]] ? true : false;

    export type Ge<A extends number, B extends number> =
        Tupled<A> extends [...Tupled<B>, ...unknown[]] ? true : false;

    export type Eq<A extends number, B extends number> = 
        A extends B ? true : false;
    
    export type Lt<A extends number, B extends number> =
        Le<A, B> extends true ?
            Eq<A, B> extends false ?
                true
            : false
        : false;

    export type Gt<A extends number, B extends number> =
        Ge<A, B> extends true ?
            Eq<A, B> extends false ?
                true
            : false
        : false;
    
}

type Add<A extends number, B extends number> =
    B extends 0 ? 
        A 
    : A extends 0 ? 
        B 
    : [...Tupled<A>, ...Tupled<B>]["length"];

type Sub<A extends number, B extends number> =
    B extends 0 ? 
        A 
    : Tupled<A> extends [...Tupled<B>, ...infer D] ? D["length"] : 0;

type Decr<A extends number> = Sub<A, 1>;
type Incr<A extends number> = Add<A, 1>;

type Digit = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;
type Concat<
    A extends number,
    B extends Digit
> = [
    ...Tupled<A>,
    ...Tupled<A>,
    ...Tupled<A>,
    ...Tupled<A>,
    ...Tupled<A>,
    ...Tupled<A>,
    ...Tupled<A>,
    ...Tupled<A>,
    ...Tupled<A>,
    ...Tupled<A>,
    ...Tupled<B>
]["length"];

type EvenS<A extends string> = A extends `${string}${0 | 2 | 4 | 6 | 8}` ? true : false;
type Even<A extends number> = EvenS<`${A}`>;

type Half1<A extends string, NoCarry extends boolean = true> =
    A extends `${infer C}${infer R}` ? 
        [
            NoCarry extends false ?
                C extends `${8 | 9}` ? 9 :
                C extends `${6 | 7}` ? 8 :
                C extends `${4 | 5}` ? 7 :
                C extends `${2 | 3}` ? 6 :
                5
            :
                C extends `${8 | 9}` ? 4 :
                C extends `${6 | 7}` ? 3 :
                C extends `${4 | 5}` ? 2 :
                C extends `${2 | 3}` ? 1 :
                0, 
            ...Half1<R, EvenS<C>>
        ]
    : [];
type Half2<A extends number[]> =
    A extends [...infer R extends number[], infer D extends Digit] ? 
        Concat<Half2<R>, D>
    : 0;

type Half<A extends number> = Half2<Half1<`${A}`>>;
type Double<A extends number> = [...Tupled<A>, ...Tupled<A>]["length"] & number;

type Mul<A extends number, B extends number> =
    B extends 0 ? 
        0 
    : B extends 1 ? 
        A 
    : A extends 0 ? 
        0 
    : A extends 1 ? 
        B 
    : Even<B> extends false ?
        Add<Mul<Double<A>, Half<B>>, A>
    : Mul<Double<A>, Half<B>>;

type DivMod<A extends number, B extends number> =
    B extends 0 ? 
        never 
    : B extends 1 ?
        A
    : Compare.Lt<A, B> extends true ? 
        [0, A] 
    : Compare.Gt<B, 4999> extends true ? // fallback because you can't Double values greater than 4999
        [1, Sub<A, B>]
    : DivMod<A, Double<B>> extends [infer D1 extends number, infer M1 extends number] ?
        Compare.Ge<M1, B> extends true ?
            [Add<Double<D1>, 1>, Sub<M1, B>]
        : [Double<D1>, M1]
    : never;

let y: DivMod<9999, 2>;
export {};