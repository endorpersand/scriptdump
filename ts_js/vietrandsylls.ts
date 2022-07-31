/*
 * creation: unknown
 *
 * Creates random syllables that look Vietnamese
 * yeah
 */

/**
 * Orthographical units that make up a syllable
 */
namespace Unit {
    /** The possible initial consonants */
    export const Initials = [
        '', 'b', 'c', 'ch', 'd', 'đ', 'g', 'gi', 'h', 'kh', 'l', 'm', 
        'n', 'ng', 'nh', 'ph', 'r', 's', 't', 'th', 'tr', 'v', 'x'
    ] as const;
    export type Initial = typeof Initials[number];

    /** The possible final consonants */
    export const Finals = [
        '', 'c', 'ch', 'm', 'n', 'ng', 'nh', 'p', 't'
    ] as const;
    export type Final = typeof Finals[number];

    /** The possible vowels */
    export const Vowels = [
        "a", "ă", "â", "e", "ê", "o", "ô", "ơ", "u", "ư", // normal monoph
        "i", "iê", "ươ", "uô", // [i, y], [iê, ia], [ươ, ưa], [uô, ua]
    ] as const;
    export type Vowel = typeof Vowels[number];

    /** The possible combination of on-glides and off-glides */
    export const Glides = [
        "_", "w_", "w_w", "w_j", "_j", "_w"
    ] as const;
    export type Glide = typeof Glides[number];

    /** The possible tones */
    export const Tones = [
        '', '\u0300', '\u0301', '\u0303', '\u0309', '\u0323'
    ] as const;
    export type Tone = typeof Tones[number];
}

/**
 * Utility namespace to manipulate probability weights
 */
namespace Weights {

    /**
     * A weight, either an integer (which represents a weight) or a probability
     */
    export type Weight =
        | number
        | RelWeight;

    /**
     * Weight dependent on the total weight of the set of weights
     */
    interface RelWeight {
        /**
         * The probability that this item occurs.
         * This should be a number between [0, 1] 
         * and the total fraction of relative weights should be no greater than 1.
         */
        fr: number
    };

    /**
     * Create a uniform distribution of weights from a list.
     */
    function uniform<T extends string>(t: readonly T[]): Record<T, number> {
        return fromEntries(t.map(e => [e, 1] as const));
    }

    /**
     * Convert a record of weights (which may include relative weights) into purely absolute weights
     * @param weights record of weights
     * @returns record of absolute weights
     */
    export function absWeights<T extends PropertyKey>(weights: Record<T, Weight>): Record<T, number> {
        const r = { ...weights };

        const absolutes: number[] = [];
        const relatives: RelWeight[] = [];

        for (let w of Object.values<Weight>(weights)) {
            if (typeof w === "number") absolutes.push(w);
            else relatives.push(w);
        }

        let total: number;
        if (absolutes.length !== 0) {
            const absSum = absolutes.reduce((acc, cv) => acc + cv, 0);
            const absPerc = 1 - relatives.reduce((acc, {fr}) => acc + fr, 0);
    
            total = absSum / absPerc;
        } else {
            total = 1 / relatives.reduce((acc, cv) => acc * cv.fr, 1);
        }

        for (let [k, w] of Object.entries<Weight>(r)) {
            if (typeof w !== "number") r[k as T] = Math.round(w.fr * total);
        }
        return r as any;
    }

    /**
     * Weights of final consonants
     */
    export const wFinals: Record<Unit.Final, Weight> = {
        ...uniform(Unit.Finals),
        "": { fr: 1/2 }
    };

    /**
     * Weights of glides
     */
    export const wGlides: Record<Unit.Glide, Weight> = {
        ...uniform(Unit.Glides),
        "_": { fr: 1/2 }
    };
}

/**
 * Choose uniformly from an array
 * @param arr array
 * @returns an element
 */
function choose<T>(arr: ArrayLike<T>) {
    const i = Math.floor(Math.random() * arr.length);
    return arr[i];
}

/**
 * Choose from a record of weights
 * @param weights record of weights
 * @returns an element
 */
function chooseWeighted<T extends PropertyKey>(weights: Record<T, Weights.Weight>) {
    const entries = Object.entries<number>(Weights.absWeights(weights)) as [T, number][];
    
    const sum = entries.map(([_, w]) => w)
        .reduce((acc, cv) => acc + cv, 0);
    
    let i = Math.floor(Math.random() * sum);
    for (let [k, w] of entries) {
        i -= w;
        if (i < 0) return k;
    }

    return entries[entries.length - 1][0];
}

/**
 * Make a copy of an object with some keys omitted
 * @param o Object
 * @param omit Keys to omit
 * @returns new object
 */
function omit<T extends PropertyKey, U extends T, V>(o: Record<T, V>, omit: U[]): Omit<typeof o, U> {
    const result = { ...o };
    for (let u of omit) delete result[u];
    return result;
}

/**
 * Object.fromEntries that types into a Record
 */
function fromEntries<T extends PropertyKey, V>(entries: readonly (readonly [T, V])[]): Record<T, V> {
    return Object.fromEntries<V>(entries) as Record<T, V>;
}

/**
 * Split a glide into an on-glide and an off-glide
 */
function splitGlide<G extends Unit.Glide>(g: G): G extends `${infer S1}_${infer S2}` ? [S1, S2] : never {
    return g.split("_") as any;
};

/**
 * Randomly choose a glide
 */
function chooseGlide(v: Unit.Vowel): Unit.Glide {
    const glides: Unit.Glide[] = ["_"];
    if (!'ưươoôuuô'.includes(v)) glides.push('w_');
    if ('eia'.includes(v)) glides.push('w_w');
    if ('aăâ'.includes(v)) glides.push('w_j');
    if (!'eêiiê'.includes(v)) glides.push('_j');
    if (!'oôuuô'.includes(v)) glides.push('_w');
    
    const weights = fromEntries(
        glides.map(g => [g, Weights.wGlides[g]])
    );
    return chooseWeighted(weights);
}

/**
 * Randomly choose a final consonant
 */
function chooseFinal(v: Unit.Vowel, g: Unit.Glide): Unit.Final {
    if (!g.endsWith("_")) return "";

    const finals = "aêi".includes(v) ?
    Weights.wFinals
    : omit(Weights.wFinals, ["ch", "nh"]);

    return chooseWeighted(finals);
}

function chooseSylConfig(): 
    [Unit.Initial, Unit.Vowel, Unit.Glide, Unit.Final, Unit.Tone] {
    const initial = choose(Unit.Initials);
    const vowel   = choose(Unit.Vowels);
    const glide   = chooseGlide(vowel);
    const final   = chooseFinal(vowel, glide);
    const tone    = choose(Unit.Tones);

    return [initial, vowel, glide, final, tone];
}

export function generateSyllable() {
    const [initial, vowel, glide, final, tone] = chooseSylConfig();

    let [onGlide, offGlide] = splitGlide(glide);

    // apply off-glide

    // ăj => ay
    // âj => ây
    // _j => _i

    // aw => ao
    // ew => eo
    // ăw => au
    // _w => _u

    let syllable = `${vowel}${tone}${offGlide}`
        .replace("j", () => "ăâ".includes(vowel) ? "y" : "i")
        .replace("w", () => "ae".includes(vowel) ? "o" : "u")
        .replace(/ă(\p{M}?)y/u, "a$1y")
        .replace(/ă(\p{M}?)w/u, "a$1w");
    
        
    // apply on-glide

    // cw_ => qu_
    // wa => oa
    // wă => oă
    // we => oe
    // wi => uy
    // w_ => u_

    let dInitial: string = initial;
    if (onGlide === "w") {
        if (dInitial === "c") {
            dInitial = "q";
            syllable = `u${syllable}`;
        } else {
            syllable = `${onGlide}${syllable}`
                .replace("w", () => "aăe".includes(vowel) ? "o" : "u")
        }
    }
    syllable.replace("ui", "uy");
    // apply initial
    // ci, ce, cê => ki, ke, kê
    // (n)gi, (n)ge, (n)gê => (n)ghi, (n)ghe, (n)ghê

    // ^iê => yê
    // gi + i => gi
    syllable = `${dInitial}${syllable}`
        .replace(/c([eêi])/, "k$1")
        .replace(/gii/, "gi")
        .replace(/g([eêi])/, "gh$1")
        .replace(/^iê/, "yê");
    
    // apply final
    // iê$, ươ$, uô$ => ia, ưa, ua

    // for tones, ia, ưa, ua => [i]a, [ư]a, [u]a
    syllable = `${syllable}${final}`
        .replace(/iê(\p{M}?)$/u, "i$1a")
        .replace(/ươ(\p{M}?)$/u, "ư$1a")
        .replace(/uô(\p{M}?)$/u, "u$1a");

    return syllable.normalize("NFC");
}

export function generateWord() {
    const length = choose([1,1,1,2,2,3]);
    return Array.from({length}, () => generateSyllable()).join(" ");
}