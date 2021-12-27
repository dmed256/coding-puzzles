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
stringstream cin_line() {
  string line;
  getline(cin, line);
  return stringstream(line);
}

template <class T>
vector<T>& makeUnique(vector<T> &vec) {
  sort(all(vec));
  vec.resize(unique(all(vec)) - vec.begin());
}

//---[ Main ]------------------------------------
struct point {
  i64 x;
  i64 y;
};

i64 triangle_area_doubled(point p1, point p2, point p3) {
  return abs(
    (p1.x * (p2.y - p3.y))
    + (p2.x * (p3.y - p1.y))
    + (p3.x * (p1.y - p2.y))
  );
}

void solve_test() {
  i64 w, h;
  cin >> w >> h;

  vector<vector<point>> sides;
  i64 side_points;
  i64 x, y;
  i64 max_area = 0;

  {
    vector<point> points;
    cin >> side_points;
    for (int i = 0; i < side_points; ++i){
      cin >> x;
      points.push_back({x, 0});
    }
    sides.push_back(points);
  }

  {
    vector<point> points;
    cin >> side_points;
    for (int i = 0; i < side_points; ++i){
      cin >> x;
      points.push_back({x, h});
    }
    sides.push_back(points);
  }

  {
    vector<point> points;
    cin >> side_points;
    for (int i = 0; i < side_points; ++i){
      cin >> y;
      points.push_back({0, y});
    }
    sides.push_back(points);
  }

  {
    vector<point> points;
    cin >> side_points;
    for (int i = 0; i < side_points; ++i){
      cin >> y;
      points.push_back({w, y});
    }
    sides.push_back(points);
  }

  for (int s1 = 0; s1 < 4; ++s1) {
    vector<point> &points1 = sides[s1];
    for (int s2 = 0; s2 < 4; ++s2) {
      if (s1 == s2) {
        continue;
      }
      vector<point> &points2 = sides[s2];

      // Max area should include the first and last side points
      const point &p1 = points1[0];
      const point &p2 = points1[sz(points1) - 1];

      // Check both ends
      const point &p31 = points2[0];
      const point &p32 = points2[sz(points2) - 1];

      max_area = max(
        max_area,
        triangle_area_doubled(p1, p2, p31)
      );
      max_area = max(
        max_area,
        triangle_area_doubled(p1, p2, p32)
      );
    }
  }

  cout << max_area << '\n';
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
