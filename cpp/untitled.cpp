#include <iostream>
#include <vector>

using namespace std;

vector<int> build_failure_function(string &pattern) {
  vector<int> F;
  int m = pattern.length();
  F.push_back(0);
  F.push_back(0);
  for (int i = 2; i <= m; i++) {
    int j = F[i-1];
    while (true) {
      if (pattern[j] == pattern[i - 1]) {
        F.push_back(j + 1);
        break;
      }
      else if (j == 0) {
        F.push_back(0);
        break;
      }
      else {
        j = F[j];
      }
    }
  }
  return F;
}

int knuth_morris_pratt(string pattern, string text) {
  vector<int> F = build_failure_function(pattern);
  int m = pattern.length();
  int n = text.length();
  int i = 0; // the index of text read
  int j = 0; // the index matched so far in pattern
  while (true) {
    if (i == n) return -1;
    else if (text[i] == pattern[j]) {
      i++;
      j++;
      if (j == m) return i - m;
    }
    else if (j > 0) {
      j = F[j];
    }
    else {
      i++;
    }
  }
}

int main (int argc, char** argv) {
  string text;
  string pattern;
  cout << "Please enter a text string:" << endl;
  cin >> text;
  cout << "Please enter a pattern string:" << endl;
  cin >> pattern;
  cout << "Result: " << knuth_morris_pratt(pattern, text) << endl;
  return 0;
}