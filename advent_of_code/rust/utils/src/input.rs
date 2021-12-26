use std::fs::File;
use std::io::prelude::*;

pub fn multiline_lines(value: &str) -> Vec<String> {
    let mut lines: Vec<String> = value
        .split("\n")
        .map(String::from)
        .collect();

    match lines.first() {
        Some(value) =>
            if value.is_empty() {
                lines.remove(0);
            },
        None => {},
    }
    match lines.last() {
        Some(value) =>
            if value.is_empty() {
                lines.pop();
            },
        None => {},
    }
    lines
}

pub fn get_input_lines(filepath: &str) -> Vec<String> {
    let input_filename = filepath.replace(".rs", "_input");

    let mut file = File::open(input_filename).unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).ok();

    multiline_lines(&contents)
}
