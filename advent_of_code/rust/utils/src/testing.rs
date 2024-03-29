//! Testing utility methods
//!
//! value.should_be(&ans)
//! value.debug("Star 1")
//! value.clipboard()
//!
//! TODO:
//!   value.submit(1)
//!
use colored::*;
use std::io::Write;
use std::process::{Command, Stdio};

static mut TESTS_FAILED: i32 = 0;

pub trait Answer {
    fn should_be(self, ans: Self) -> Self;
    fn debug<H: Into<String>>(self, header: H) -> Self;
    fn clipboard(self) -> Self;
}

impl Answer for i32 {
    fn should_be(self, ans: i32) -> i32 {
        run_should_be(self, ans);
        self
    }

    fn debug<H: Into<String>>(self, header: H) -> i32 {
        run_debug(self, header);
        self
    }

    fn clipboard(self) -> i32 {
        run_clipboard(self);
        self
    }
}

impl Answer for i64 {
    fn should_be(self, ans: i64) -> i64 {
        run_should_be(self, ans);
        self
    }

    fn debug<H: Into<String>>(self, header: H) -> i64 {
        run_debug(self, header);
        self
    }

    fn clipboard(self) -> i64 {
        run_clipboard(self);
        self
    }
}

impl Answer for String {
    fn should_be(self, ans: String) -> String {
        run_should_be(self.clone(), ans);
        self
    }

    fn debug<H: Into<String>>(self, header: H) -> String {
        run_debug(self.clone(), header);
        self
    }

    fn clipboard(self) -> String {
        run_clipboard(self.clone());
        self
    }
}

/// assert_eq without the panic and helper print
fn run_should_be<T: Eq>(value: T, ans: T)
where
    T: std::fmt::Display,
{
    if value == ans {
        println!(
            "\n{}: [{}]",
            "PASS".green(),
            ans.to_string().green(),
        );
    } else {
        unsafe {
            TESTS_FAILED += 1;
        }
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

/// Print out value with header
fn run_debug<T, H: Into<String>>(value: T, header: H)
where
    T: std::fmt::Display,
{
    println!(
        "\n{}
-> [{}]",
        header.into().blue(),
        value.to_string().blue(),
    )
}

/// Copy `value` to the clipboard
fn run_clipboard<T>(value: T)
where
    T: std::fmt::Display,
{
    Command::new("pbcopy")
        .arg("w")
        .stdin(Stdio::piped())
        .spawn()
        .map(|process| process
             .stdin
             .unwrap()
             .write_all(value.to_string().as_bytes())
        ).ok();
}

/// Check if any tests failed
pub fn aoc_exit() {
    unsafe {
        if 0 < TESTS_FAILED {
            std::process::exit(1);
        }
    }
}
