use utils::*;

fn main() {
    let x: i32 = 3;

    x.should_be(&3);
    x.should_be(&4);

    x.debug("Star 1").should_be(&3);
}
