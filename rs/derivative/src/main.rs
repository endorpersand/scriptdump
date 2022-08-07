// Very simple derivative calculator

use std::fmt::Display;

#[derive(PartialEq, Eq, Clone)]
struct Symbol(String);

#[derive(PartialEq, Eq, Clone)]
enum Expr {
    Add(Vec<Expr>),
    Mul(Vec<Expr>),
    Pow(Box<Expr>, u32),

    Constant(usize),
    Symbol(Symbol)
}

impl Expr {
    fn new_add(exprs: Vec<Expr>) -> Self {
        let mut final_exprs = vec![];
        let mut constant = 0;

        let exprs = exprs
            .into_iter()
            .flat_map(|e| match e {
                Expr::Add(exprs) => exprs,
                other => vec![other]
            });
        for e in exprs {
            match e {
                Expr::Constant(c) => constant += c,
                other => final_exprs.push(other)
            }
        }

        if constant != 0 { final_exprs.insert(0, Expr::new_const(constant)) };
        Self::Add(final_exprs)
    }

    fn new_mul(exprs: Vec<Expr>) -> Self {
        let mut final_exprs = vec![];
        let mut coeff = 1;

        let exprs = exprs
            .into_iter()
            .flat_map(|e| match e {
                Expr::Mul(exprs) => exprs,
                other => vec![other]
            });
        for e in exprs {
            match e {
                zero @ Expr::Constant(0) => return zero,
                Expr::Constant(c) => coeff *= c,
                other => final_exprs.push(other)
            }
        }

        if coeff != 1 { final_exprs.insert(0, Expr::new_const(coeff)) };
        Self::Mul(final_exprs)
    }

    fn new_pow(expr: Expr, n: u32) -> Self {
        if let Expr::Constant(b) = expr {
            return Expr::new_const(b.pow(n));
        }

        Self::Pow(Box::new(expr), n)
    }

    fn new_const(n: usize) -> Self {
        Self::Constant(n)
    }

    fn new_sym(sym: &str) -> Self {
        Self::Symbol(Symbol::new(sym))
    }
}

impl Symbol {
    fn new(s: &str) -> Self {
        Self(s.to_string())
    }
}

trait Derivable {
    fn derive(self, wrt: &Symbol) -> Expr;
}

impl Derivable for Expr {
    fn derive(self, wrt: &Symbol) -> Expr {
        match self {
            Expr::Add(exprs) => Expr::new_add(
                exprs.into_iter()
                     .map(|e| e.derive(wrt))
                     .collect()
            ),
            Expr::Mul(exprs) => {
                let terms = (0..exprs.len())
                    .map(|i| {
                        let mut res = vec![];
                        let mut it = exprs.iter();

                        res.extend(it.by_ref().take(i).cloned());
                        if let Some(e) = it.next() {
                            res.push(e.clone().derive(wrt));
                        }
                        res.extend(it.cloned());

                        res
                    })
                    .map(Expr::new_mul)
                    .collect();
                
                Expr::new_add(terms)
            },
            Expr::Pow(e, c) => Expr::new_mul(vec![
                Expr::new_const(c as usize), 
                Expr::new_pow(*e.clone(), c - 1),
                e.derive(wrt)
            ]),
            Expr::Constant(_) => Expr::new_const(0),
            Expr::Symbol(s) => s.derive(wrt)
        }
    }
}

impl Derivable for Symbol {
    fn derive(self, wrt: &Symbol) -> Expr {
        Expr::new_const((&self == wrt) as usize)
    }
}

impl Display for Expr {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Expr::Add(exprs) => {
                let s = exprs.iter()
                     .map(|e| e.to_string())
                     .collect::<Vec<_>>()
                     .join(" + ");
                
                write!(f, "{}", s)
            },
            Expr::Mul(exprs) => {
                let s = exprs.iter()
                     .map(|e| e.to_string())
                     .collect::<Vec<_>>()
                     .join(" * ");
                
                write!(f, "{}", s)
            },
            Expr::Pow(e, p) => write!(f, "{}^{}", e, p),
            Expr::Constant(c) => write!(f, "{}", c),
            Expr::Symbol(s) => write!(f, "{}", s.0),
        }
    }
}

fn main() {
    let x = Symbol::new("x");

    let e = Expr::new_add(vec![
        Expr::new_mul(vec![
            Expr::new_pow(Expr::new_const(4), 7),
            Expr::new_pow(Expr::new_sym("x"), 7)
        ]), 
        Expr::new_mul(vec![
            Expr::new_pow(Expr::new_const(4), 7),
            Expr::new_pow(Expr::new_sym("y"), 7)
        ]),
        Expr::new_mul(vec![
            Expr::new_sym("x"),
            Expr::new_sym("y"),
            Expr::new_sym("z")
        ]),
    ]);

    println!("{}", e);

    let de = e.derive(&x);
    println!("{}", de);
}
