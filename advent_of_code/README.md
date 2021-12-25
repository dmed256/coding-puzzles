# Advent of Code

I've loved the fun and challenging puzzles found in [Advent of Code](https://adventofcode.com/), so here are the somewhat cleaned up solutions

I use Python for trying to "compete" for the leaderboard, although I haven't been too successful yet 😅, but getting there!

I'll be adding other languages to pick them up, currently thinking of:
1. Rust
2. Go
3. C++

## Scripts

### Extended global leaderboard

Since I couldn't make the top 100 leaderboard, I was curious which position I was at. I made a script that will sleep, fetch, and cache daily leaderboards. 
This way I could aggregate and find what position I was in

```sh
./get-global-loaderboard YEAR [--user USER]
```

**Example**
```sh
./get-global-leaderboard 2021 dmed256
```

### Downloading puzzle input

⚠️ This expects a `advent_of_code/.session` file to exist with your session key ⚠️

I built a simple bash script to download the daily puzzle input to avoid accidental copy-paste issues.
The script looks at the directory to figure out the day

```sh
../../get-input DAY
```

**Example**
```sh
../../get-input 2
../../get-input 10
```

## Tests

I wanted to make sure I didn't break previous solutions while refactoring the `repo_utils.py` module, and then started using it to track slow solutions to optimize later

```sh
./run-tests LANGUAGE
```

**Example**

```sh
./run-tests python
```

Currently only `python` is supported, but `rust` coming soon I hope!

# Leaderboard

## 2021

2021 was my first year "competing", and I ended up with `467` points at ranking `128` (so close!)

I managed to finish most problems the night/dawn of the problem except for `23`, that one stumped me that night 😞

<img src="https://user-images.githubusercontent.com/1812355/147386886-cf457537-ef14-4415-9d19-5fb530c6298f.png" width="400px"></img>

