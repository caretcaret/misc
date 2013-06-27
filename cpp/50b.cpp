#include <iostream>
#include <map>

using namespace std;

int main(int argc, char** argv) {
  map<char, long long> M;
  string s;
  cin >> s;
  for (int i = 0; i < s.size(); i++) {
    if (M.find(s[i]) == M.end()) {
      M[s[i]] = 1;
    } else {
      M[s[i]]++;
    }
  }
  long long sum = 0;
  for (map<char, long long>::iterator it = M.begin(); it != M.end(); it++) {
    sum += (it->second) * (it->second);
  }
  cout << sum << endl;
  return 0;
}