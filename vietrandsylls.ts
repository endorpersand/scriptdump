function vietRS() {
    let initials = [
            '', 'b', 'ch', 'd', 'đ', 'gi', 'h', 'kh', 'l', 'm', 'n', 'nh', 'ph', 'r', 's', 't', 'th', 'tr', 'v', 'x',
            'c', 'g', 'ng'
        ],
        finals = ['', 'c', 'm', 'n', 'ng', 'p', 't'], // + ch, nh (for a, ê, i)
        monophs = [
            "a", "ă", "â", "e", "ê", "o", "ô", "ơ", "u", "ư", // normal monoph
            "i", "iê", "ươ", "uô", // [i, y], [iê, ia], [ươ, ưa], [uô, ua]
        ],
        tones = ['', '\u0300', '\u0301', '\u0303', '\u0309', '\u0323'];
        finals = finals.flatMap(x => [x, '']);
    let peek = <T>(iter: ArrayLike<T>): T => iter[iter.length - 1];
    let diphables = (char: string): string[] => {
        let canDiph = [];
        if (!['ư','ươ','o','ô','u','uô'].includes(char)) canDiph.push('w_');
        if (['e','i','a'].includes(char)) canDiph.push('w_w');
        if (['a','ă','â'].includes(char)) canDiph.push('w_j');
        if (!['e','ê','i','iê'].includes(char)) canDiph.push('_j');
        if (!['o','ô','u','uô'].includes(char)) canDiph.push('_w');
        canDiph = canDiph.flatMap(x => ['_', x]);
        return canDiph;
    }
    let choose = <T>(iter: ArrayLike<T>): T => iter[Math.floor(Math.random() * iter.length)]; // [min, max)
    
    let syllables = [];
    let sylcount = choose([1,1,1,2,2,3]);
    for (let i = 0; i < sylcount; i++) {
        let initial = choose(initials);
        let monoph = choose(monophs);
        let diphconfig = choose(diphables(monoph));
        let final = /_[jw]$/.test(diphconfig) ? '' : (['a', 'ê', 'i'].includes(peek(monoph)) ? choose([...finals, 'ch', 'nh']) : choose(finals));
        let tone = choose(tones);
        /*
        * <== ORTHOGRAPHICAL RULES ==>
        * ci, ce, cê => ki, ke, kê
        * cw_ => qu_
        * (n)gi, (n)ge, (n)gê => (n)ghi, (n)ghe, (n)ghê
        * iê$, ươ$, uô$ => ia, ưa, ua
        * <- I TO Y ->
        * ^iê => yê
        * wi => uy
        * <- SEMIVOWEL ORTH ->
        * ăj, âj => ăy, ây
        * _j => _i
        * aw, ew => ao, eo
        * ăw => au
        * _w => _u
        * we, wă => oe, oă // u(e|ă) occurs as qu(e|ă)
        * wa => oa or ua // por qué??
        * w_ => u_
        * <- TONE PLACEMENT ->
        * let w = semivowel, ◌́ = tone
        * w_w + ◌́ => w_́w
        * iê + ◌́ => iế // also applies to ươ, uô
        * ia + ◌́ => ía // also applies to ưa, ua
        * <- ->
        * gii => gi
        * ăy => ay
        */
        let syllable = initial + diphconfig.replace('_', monoph) + final;
        syllable = syllable.replace(/c(i|e|ê)/, 'k$1')
                           .replace(/cw/, 'qu')
        if (peek(initial) === 'g') syllable = syllable.replace(/g(i|e|ê)/, 'gh$1');
        syllable = syllable.replace(/iê$/, 'ia')
                           .replace(/ươ$/, 'ưa')
                           .replace(/uô$/, 'ua')
                           .replace(/^iê/, 'yê')
                           .replace(/(w|u)i/, 'uy')
                           .replace(/(ă|â)j/, '$1y')
                           .replace(/j/, 'i')
                           .replace(/(a|e)w/, '$1o')
                           .replace(/ăw/, 'au')
                           .replace(/w$/, 'u')
                           .replace(/w(e|ă)/, 'o$1')
                           .replace(/wa/, () => choose(['u', 'o']) + 'a')
                           .replace(/w/, 'u')
        if (tone !== '') {
            syllable = syllable.replace(/(iưu)a/, '$1' + tone + 'a')
                               .replace(monoph, monoph + tone)
        }
        syllable = syllable.replace(/gii/, 'gi')
                           .replace(/ăy/, 'ay')
    syllables.push(syllable);
    }
    return syllables.join(' ');
}