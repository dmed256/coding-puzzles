#include <iostream>
#include <tuple>
#include <unordered_map>
#include <vector>

class input_t {
public:
  const int a;
  const int b;
  const int c;

  input_t(int a_, int b_, int c_) :
    a(a_),
    b(b_),
    c(c_) {}
};

int64_t solve(
  const std::vector<input_t> &inputs,
  const int input_index,
  const int64_t init_z,
  const int64_t model_number,
  const bool get_max_value,
  std::unordered_map<int64_t, int> &cache
) {
  const int64_t key = (
    (abs(init_z) * 100)
    + (init_z < 0) * 10
    + input_index
  );
  if (cache.contains(key)) {
    return -1;
  }
  cache[key] = 1;

  if (inputs.size() <= input_index) {
    return init_z ? -1 : model_number;
  }

  const input_t &input = inputs[input_index];
  const int a = input.a;
  const int b = input.b;
  const int c = input.c;

  const int start = get_max_value ? 9 : 1;
  const int end = get_max_value ? 0 : 10;
  const int inc = get_max_value ? -1 : 1;

  for (int w = start; w != end; w += inc) {
    int64_t z = init_z;

    const bool x = w != ((z % 26) + b);
    z /= a;

    z *= (25 * x) + 1;
    z += (w + c) * x;

    const int64_t solution = solve(
      inputs,
      input_index + 1,
      z,
      (model_number * 10L) + w,
      get_max_value,
      cache
    );
    if (0 <= solution) {
      return solution;
    }
  }

  return -1;
}

int main() {
  const std::vector<input_t> inputs = {
    {1, 11, 6},
    {1, 13, 14},
    {1, 15, 14},
    {26, -8, 10},
    {1, 13, 9},
    {1, 15, 12},
    {26, -11, 8},
    {26, -4, 13},
    {26, -15, 12},
    {1, 14, 6},
    {1, 14, 9},
    {26, -1, 15},
    {26, -8, 4},
    {26, -14, 1},
  };

  std::unordered_map<int64_t, int> cache1;
  std::cout << "max value: " << solve(inputs, 0, 0, 0, true, cache1) << '\n';

  std::unordered_map<int64_t, int> cache2;
  std::cout << "min value: " << solve(inputs, 0, 0, 0, false, cache2) << '\n';

  return 0;
}
