#include <bits/stdc++.h>

using namespace std;

//---[ Types ]------------------------------------

#define i32 int32_t
#define i64 int64_t
#define i128 __int128

//---[ Macros ]-----------------------------------
// Easier to use iterator methods:
// sort(v) -> sort(v.begin(), v.end())
//
// Add beginning offset:
// sort(1 + v) -> sort(1 + v.begin(), v.end())
//
// Add ending offset:
// sort(v - 1) -> sort(v.begin(), v.end() - 1)
#define all(x) (x).begin(), (x).end()

#define sz(x) ((int) (x).size())

//---[ Utils ]------------------------------------
template <class T>
vector<T>& makeUnique(vector<T> &vec) {
  sort(all(vec));
  vec.resize(unique(all(vec)) - vec.begin());
}

//---[ Main ]-------------------------------------
void solve_test() {
  i64 a, b, c;
  cin >> a >> b >> c;

  if ((a + b == c) ||
      (a + c == b) ||
      (b + c == a) ||
      (a == b && !(c % 2)) ||
      (a == c && !(b % 2)) ||
      (b == c && !(a % 2))) {
    cout << "YES\n";
  } else {
    cout << "NO\n";
  }
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(0);

  i32 T;
  cin >> T;

  for (int t = 0; t < T; ++t) {
    solve_test();
  }

  return 0;
}
