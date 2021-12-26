#include "../advent_of_code.hpp"

int run(int problem, vector<string> &lines) {
  const string &line = lines[0];

  int floor = 0;
  for (int i = 0; i < sz(line); ++i) {
    const char c = line[i];

    if (c == ')') {
      --floor;
    } else if (c == '(') {
      ++floor;
    }

    if (problem == 2 && floor < 0) {
      return i + 1;
    }
  }

  return floor;
}

int main() {
  aocInit();

  auto inputLines = getInputLines();

  run(1, inputLines) | debug("Star 1") | eq(138);
  run(2, inputLines) | debug("Star 2") | eq(1771);

  return aocExit();
}
