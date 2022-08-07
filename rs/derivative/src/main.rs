// Very simple derivative calculator

use std::fmt::Display;

#[derive(PartialEq, Eq, Clone)]
enum Term {
    Const(usize),
    Symbol(Symbol)
}

#[derive(PartialEq, Eq, Clone)]
struct Symbol(String);

#[derive(PartialEq, Eq, Clone)]
enum Expr {
    Add(Vec<Expr>),
    Mul(Vec<Expr>),
    Pow(Box<Expr>, u32),
    Term(Term)
}

impl Term {
    fn new_const(n: usize) -> Expr {
        Expr::Term(Self::Const(n))
    }
    fn new_sym(sym: &str) -> Expr {
        Expr::Term(Self::Symbol(Symbol::new(sym)))
    }
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
                Expr::Term(Term::Const(c)) => constant += c,
                other => final_exprs.push(other)
            }
        }

        if constant != 0 { final_exprs.insert(0, Term::new_const(constant)) };
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
                zero @ Expr::Term(Term::Const(0)) => return zero,
                Expr::Term(Term::Const(c)) => coeff *= c,
                other => final_exprs.push(other)
            }
        }

        if coeff != 1 { final_exprs.insert(0, Term::new_const(coeff)) };
        Self::Mul(final_exprs)
    }

    fn new_pow(expr: Expr, n: u32) -> Self {
        if let Expr::Term(Term::Const(b)) = expr {
            return Term::new_const(b.pow(n));
        }

        Self::Pow(Box::new(expr), n)
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

impl Derivable for Term {
    fn derive(self, wrt: &Symbol) -> Expr {
        match self {
            Term::Const(_) => Term::new_const(0),
            Term::Symbol(s) => s.derive(wrt)
        }
    }
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
                Term::new_const(c as usize), 
                Expr::new_pow(*e.clone(), c - 1),
                e.derive(wrt)
            ]),
            Expr::Term(t) => t.derive(wrt),
        }
    }
}

impl Derivable for Symbol {
    fn derive(self, wrt: &Symbol) -> Expr {
        Term::new_const((&self == wrt) as usize)
    }
}

impl Display for Term {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Term::Const(c) => write!(f, "{}", c),
            Term::Symbol(s) => write!(f, "{}", s.0),
        }
    }
}

impl Display for Expr {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let s: String = match self {
            Expr::Add(exprs) => {
                exprs.iter()
                     .map(|e| e.to_string())
                     .collect::<Vec<_>>()
                     .join(" + ")
            },
            Expr::Mul(exprs) => {
                exprs.iter()
                     .map(|e| e.to_string())
                     .collect::<Vec<_>>()
                     .join(" * ")
            },
            Expr::Pow(e, p) => format!("{}^{}", e, p),
            Expr::Term(t) => format!("{}", t),
        };

        write!(f, "{}", s)
    }
}

fn main() {
    let x = Symbol::new("x");

    let e = Expr::new_add(vec![
        Expr::new_mul(vec![
            Expr::new_pow(Term::new_const(4), 7),
            Expr::new_pow(Term::new_sym("x"), 7)
        ]), 
        Expr::new_mul(vec![
            Expr::new_pow(Term::new_const(4), 7),
            Expr::new_pow(Term::new_sym("y"), 7)
        ]),
        Expr::new_mul(vec![
            Term::new_sym("x"),
            Term::new_sym("y"),
            Term::new_sym("z")
        ]),
    ]);

    println!("{}", e);

    let de = e.derive(&x);
    println!("{}", de);
}
