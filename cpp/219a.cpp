#include <iostream>
#include <map>
using namespace std;

int main(int argc, char** argv) {
  int num;
  cin >> num;
  
  string str;
  cin >> str;
  
  map<char, int> T;
  
  for (int i = 0; i < str.size(); i++) {
    if (T.find(str[i]) == T.end()) // what is T.end()
      T[str[i]] = 0;
    T[str[i]]++;  
  }
  
  string result = "";
  for (map<char, int>::iterator it = T.begin(); it != T.end(); it++) {
    //it->first = key
    //it->second = value
    char letter = it->first;
    int repeats = it->second;
    
    if (repeats % num != 0) {
      cout << "-1" << endl;
      return 0;
    } else {
      T[letter] /= num;
      for (int i = T[letter]; i > 0; i--) {
    result += letter;
      }
    }
  }
  
  for (int i = 0; i < k; i++)
    cout << result;
  cout << endl;
  
  return 0;
}
