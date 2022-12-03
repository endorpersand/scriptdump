type Dedup<A extends unknown[]> = Deduplicator<[], A>;
type Is<A, B> = A extends B ? 
    (B extends A ? true : false) 
: false

type Contains<A extends unknown[], B> = A extends [infer A1, ...infer A2] ? 
    (Is<A1, B> extends true ? true : Contains<A2, B>)
: false

type Deduplicator<A extends unknown[], R extends unknown[]> =
    R extends [infer R1, ...infer R2] ? (
        Contains<A, R1> extends false ? Deduplicator<[...A, R1], R2> : Deduplicator<A, R2>
    )
: A


let a: Dedup<[1, 1, 2, 3, 4]>;