#include <bits/stdc++.h>

using namespace std;

#ifdef RUNNING_LOCALLY
#  define _GLIBCXX_DEBUG
#endif

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
// Get the next value from cin and cast it to type T
template <class T>
T readNext() {
  T value;
  cin >> value;
  return value;
}

template <class T>
vector<T>& makeUnique(vector<T> &vec) {
  sort(all(vec));
  vec.resize(unique(all(vec)) - vec.begin());
}

//---[ Inputs ]-----------------------------------
#define getInputLines() _getInputLines(__FILE__)

vector<string> _getInputLines(const string &filename) {
  const string inputFilename = (
    regex_replace(filename, regex(".cpp"), "_input")
  );

  fstream file;
  file.open(inputFilename, ios::in);
  if (!file) {
    cout << "[" << inputFilename << "] does not exist!\n";
    cout.flush();
    throw 1;
  }

  string line;
  vector<string> inputLines;
  while (getline(file, line)) {
    inputLines.push_back(line);
  }

  file.close();

  return inputLines;
}

//---[ Colors ]-----------------------------------
string to_string(const char *c) {
  return c;
}

string to_string(const string &s) {
  return s;
}

template <class T>
string blue(const T &value) {
  return "\033[34m" + to_string(value) + "\033[0m";
}

template <class T>
string green(const T &value) {
  return "\033[32m" + to_string(value) + "\033[0m";
}

template <class T>
string red(const T &value) {
  return "\033[31m" + to_string(value) + "\033[0m";
}

//---[ Testing ]----------------------------------
int testsFailed = 0;

template <class T>
class Eq {
public:
  T expectedValue;

  Eq(const T &_expectedValue) :
    expectedValue(_expectedValue) {}

  void test(const T &value) const {
    if (value == expectedValue) {
      cout << '\n'
           << green("PASS") << ": "
           << "[" << green(value) << "]\n";
    } else {
      testsFailed += 1;
      cout << '\n'
           << red("FAIL") << '\n'
           << "- OUTPUT  : [" << red(value) << "]\n"
           << "- EXPECTED: [" << green(expectedValue) << "]\n";
    }
  }
};

class Debug {
public:
  const string &header;

  Debug(const string &_header) :
    header(_header) {}

  template <class T>
  void test(const T &value) const {
    cout << '\n'
         << blue(header) << '\n'
         << "-> [" << blue(value) << "]\n";
  }
};

Debug debug(const string &header) {
  return Debug(header);
}

template <class T>
Eq<T> eq(const T &expectedValue) {
  return Eq(expectedValue);
}

template <class T>
T operator | (const T &value, const Eq<T> &eq) {
  eq.test(value);
  return value;
}

template <class T>
T operator | (const T &value, const Debug &debug) {
  debug.test(value);
  return value;
}

void aocInit() {
  testsFailed = 0;

  ios_base::sync_with_stdio(false);
  cin.tie(0);
}

int aocExit() {
  return testsFailed ? 1 : 0;
}
