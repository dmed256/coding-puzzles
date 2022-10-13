#![allow(warnings, unused)]
use utils::*;

fn run(problem: i32, lines: &Vec<String>) -> i32 {
    let mut floor = 0;
    for (index, c) in lines[0].chars().enumerate() {
        floor += match c {
            ')' => -1,
            '(' => 1,
            _ => 0,
        };
        if problem == 2 && floor < 0 {
            return (index + 1) as i32;
        }
    }
    floor
}

fn main() {
    let input_lines = get_input_lines(file!());

    let example1 = multiline_lines("
(())
");

    run(1, &example1).should_be(0);
    run(1, &input_lines).debug("Star 1").should_be(138);

    let example2 = multiline_lines("
()())
");

    run(2, &example2).should_be(5);
    run(2, &input_lines).debug("Star 2").should_be(1771);

    aoc_exit();
}
