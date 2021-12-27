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
  int n;
  vector<i64> p;
  string s;

  cin >> n;

  for (int i = 0; i < n; ++i) {
    i64 pi;
    cin >> pi;
    p.emplace_back(pi);
  }

  cin >> s;

  vector<i64> liked;
  vector<i64> disliked;
  for (int i = 0; i < n; ++i) {
    if (s[i] == '1') {
      liked.emplace_back(p[i]);
    } else {
      disliked.emplace_back(p[i]);
    }
  }
  sort(all(liked));
  sort(all(disliked));

  for (int i = 0; i < n; ++i) {
    i64 pi = p[i];

    if (s[i] == '1') {
      i64 liked_idx = 1 + distance(liked.begin(), lower_bound(all(liked), pi));
      i64 qi = n - sz(liked) + liked_idx;
      cout << qi;
    } else {
      i64 disliked_idx = 1 + distance(disliked.begin(), lower_bound(all(disliked), pi));
      i64 qi = disliked_idx;
      cout << qi;
    }
    if (i < (n - 1)) {
      cout << ' ';
    }
  }
  cout << '\n';
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
