#include <iostream>

// basically write a test case such that the alg sorts correctly
// even though the sort is wrong
//
// 2
// 2 1
//
// 3
// 3 1 2
// wait let's basically write a recursive function that does the opposite
// of their alg
//o k
// it's like ctrl+z r
// what's the opposite of that function?
// if x = n exit
// swap(x+1, x), call f(x+1)?
// hmm.
// YEAH

void swap(int [] arr, int index1, int index2) {
    int copy = arr[index1];
    arr[index1] = arr[index2];
    arr[index2] = copy;
}

void reverse_sort(int[] arr, n, x) {
    if (x == n) return;
    // i'll just do some tests
    // 3 1 2 (x=0) -> 1 3 2 (x=1) -> 1 2 3 (i hope that's right)
    // wait that just moves the 3 to the 0th index
    //hmm
    swap(arr, x+1, x);
    reverse_sort(arr, n, x+1);
}

void other_reverse(int n) {
  cout << n;
  for (int i = 1; i < n; i++) {
    cout << " " << i;
  }
  cout << endl;
} // hmm. k. also check if other_reverse works.
// wait let's try finishing this one

int main(int argc, char *argv[]) {
    int n;
    cin >> n;

    int values[n];
    for (int i = 0; i < n; i++)
        values[i] = i+1;

    reverse_sort(values, n, 0);
    for (int i = 0; i < n; i++)
        cout << values[i] << " "; // <- should we not have a trailing space
}