#include "../advent_of_code.hpp"

int run(int problem, vector<string> &lines) {
  // TODO
}

int main() {
  aocInit();

  auto inputLines = getInputLines();

  run(1, inputLines) | debug("Star 1") | eq(/* TODO */);
  run(2, inputLines) | debug("Star 2") | eq(/* TODO */);

  return aocExit();
}
