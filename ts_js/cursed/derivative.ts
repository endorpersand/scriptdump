type Concat<T extends unknown[], U extends unknown[]> = [...T, ...U];
type Join<T extends string[], S extends string = "", B extends string = ""> =
    T extends [...infer U extends string[], infer V extends string] ? 
        B extends "" ? Join<U, S, V> : Join<U, S, `${V}${S}${B}`> 
    : B;
type Split<S extends string, P extends string = "", B extends string[] = []> = 
    S extends "" ? B : 
        S extends `${infer Q}${P}${infer R}` ? 
            Split<R, P, [...B, Q]>
        : [...B, S];

type Pow<S extends `${string}^${number}`> = S extends `${infer X}^${infer E}` ? {[_ in X]: E} : never;

type Poly<S extends string> = 
    Split<S, " + "> extends infer L extends string[] ? 
        {[T in keyof L]: 
            L[T] extends `${infer C}x^${infer E}` ?
                C extends "" ? ["1", E] : [C, E] 
            : never} 
    : never;

type DecrementS = {
    "0": 0,
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "10": 9,
    "11": 10,
    "12": 11,
    "13": 12,
    "14": 13,
    "15": 14,
    "16": 15,
    "17": 16,
    "18": 17,
    "19": 18,
    "20": 19,
    "21": 20,
    "22": 21,
    "23": 22,
    "24": 23,
    "25": 24,
    "26": 25,
    "27": 26,
    "28": 27,
    "29": 28,
    "30": 29,
    "31": 30,
    "32": 31
}

type MulS = {
    "0": {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
        "10": 0,
        "11": 0,
        "12": 0
    },
    "1": {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "11": 11,
        "12": 12
    },
    "2": {
        "0": 0,
        "1": 2,
        "2": 4,
        "3": 6,
        "4": 8,
        "5": 10,
        "6": 12,
        "7": 14,
        "8": 16,
        "9": 18,
        "10": 20,
        "11": 22,
        "12": 24
    },
    "3": {
        "0": 0,
        "1": 3,
        "2": 6,
        "3": 9,
        "4": 12,
        "5": 15,
        "6": 18,
        "7": 21,
        "8": 24,
        "9": 27,
        "10": 30,
        "11": 33,
        "12": 36
    },
    "4": {
        "0": 0,
        "1": 4,
        "2": 8,
        "3": 12,
        "4": 16,
        "5": 20,
        "6": 24,
        "7": 28,
        "8": 32,
        "9": 36,
        "10": 40,
        "11": 44,
        "12": 48
    },
    "5": {
        "0": 0,
        "1": 5,
        "2": 10,
        "3": 15,
        "4": 20,
        "5": 25,
        "6": 30,
        "7": 35,
        "8": 40,
        "9": 45,
        "10": 50,
        "11": 55,
        "12": 60
    },
    "6": {
        "0": 0,
        "1": 6,
        "2": 12,
        "3": 18,
        "4": 24,
        "5": 30,
        "6": 36,
        "7": 42,
        "8": 48,
        "9": 54,
        "10": 60,
        "11": 66,
        "12": 72
    },
    "7": {
        "0": 0,
        "1": 7,
        "2": 14,
        "3": 21,
        "4": 28,
        "5": 35,
        "6": 42,
        "7": 49,
        "8": 56,
        "9": 63,
        "10": 70,
        "11": 77,
        "12": 84
    },
    "8": {
        "0": 0,
        "1": 8,
        "2": 16,
        "3": 24,
        "4": 32,
        "5": 40,
        "6": 48,
        "7": 56,
        "8": 64,
        "9": 72,
        "10": 80,
        "11": 88,
        "12": 96
    },
    "9": {
        "0": 0,
        "1": 9,
        "2": 18,
        "3": 27,
        "4": 36,
        "5": 45,
        "6": 54,
        "7": 63,
        "8": 72,
        "9": 81,
        "10": 90,
        "11": 99,
        "12": 108
    },
    "10": {
        "0": 0,
        "1": 10,
        "2": 20,
        "3": 30,
        "4": 40,
        "5": 50,
        "6": 60,
        "7": 70,
        "8": 80,
        "9": 90,
        "10": 100,
        "11": 110,
        "12": 120
    },
    "11": {
        "0": 0,
        "1": 11,
        "2": 22,
        "3": 33,
        "4": 44,
        "5": 55,
        "6": 66,
        "7": 77,
        "8": 88,
        "9": 99,
        "10": 110,
        "11": 121,
        "12": 132
    },
    "12": {
        "0": 0,
        "1": 12,
        "2": 24,
        "3": 36,
        "4": 48,
        "5": 60,
        "6": 72,
        "7": 84,
        "8": 96,
        "9": 108,
        "10": 120,
        "11": 132,
        "12": 144
    }
};

type _Derivative<S extends string> = 
    Poly<S> extends infer L extends [string, string][] ? 
        {[T in keyof L]:
            L[T] extends [infer A extends keyof MulS, infer B extends keyof DecrementS] ?
                B extends keyof MulS[A] ? [MulS[A][B], DecrementS[B]] : never
            : never
        } 
    : never;
    
type Stringable = string | number | bigint | boolean | null | undefined;

type PolyString<S extends unknown[]> = Join<{
        [T in keyof S]: S[T] extends [infer C extends Stringable, infer E extends Stringable] ? 
            `${C}x^${E}` 
        : ""
    }, " + ">;

type Derivative<S extends string> = PolyString<_Derivative<S>>;

let v: Derivative<"12x^3 + x^2"> = "36x^2 + 2x^1";

export {};