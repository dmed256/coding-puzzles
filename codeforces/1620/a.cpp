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
int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  i32 N;
  cin >> N;

  for (int n = 0; n < N; ++n) {
    string word;
    cin >> word;

    i32 e_chars = 0;
    i32 n_chars = 0;
    for (int i = 0; i < sz(word); ++i) {
      e_chars += (word[i] == 'E');
      n_chars += (word[i] == 'N');
    }

    if (n_chars == 1) {
      cout << "NO\n";
    } else {
      cout << "YES\n";
    }
  }

  return 0;
}
