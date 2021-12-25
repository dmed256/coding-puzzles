use colored::*;

// TODO:
// - submit
// - clipboard

fn run_should_be<T: Eq>(value: &T, ans: &T)
where
    T: std::fmt::Display,
{
    if value == ans {
        println!("\n{}: [{}]", "PASS".green(), ans.to_string().green());
    } else {
        println!(
            "\n{}:
- OUTPUT  : [{}]
- EXPECTED: [{}]",
            "FAIL".red(),
            value.to_string().red(),
            ans.to_string().green(),
        );
    }
}

fn run_debug<T>(value: T, header: &str)
where
    T: std::fmt::Display,
{
    println!(
        "\n{}
-> [{}]",
        header.blue(),
        value.to_string().blue(),
    )
}

pub trait Answer {
    fn should_be(&self, ans: &Self) -> &Self;

    fn debug(&self, header: &str) -> &Self;
}

impl Answer for i32 {
    fn should_be(&self, ans: &i32) -> &i32 {
        run_should_be(&self, &ans);
        self
    }

    fn debug(&self, header: &str) -> &i32 {
        run_debug(&self, &header);
        self
    }
}

impl Answer for i64 {
    fn should_be(&self, ans: &i64) -> &i64 {
        run_should_be(&self, &ans);
        self
    }

    fn debug(&self, header: &str) -> &i64 {
        run_debug(&self, &header);
        self
    }
}

impl Answer for str {
    fn should_be(&self, ans: &str) -> &str {
        run_should_be(&self, &ans);
        self
    }

    fn debug(&self, header: &str) -> &str {
        run_debug(&self, &header);
        self
    }
}
