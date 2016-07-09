#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

// get the known class

vector<string> getKnownClass(const char* fileName) {
    vector<string> knownClass;
    ifstream configFile(fileName,ios::in);
    string line; 
    int case_num = 0, ct = 1;
    while (getline(configFile, line)) {
        knownClass.push_back(line);
    }
    configFile.close();
    return knownClass;
}

int main() {
    const char* fileName = "../config/known-class.config";
    vector<string> knownClass = getKnownClass(fileName);
    for(int i = 0; i < knownClass.size(); i++) {
        cout << knownClass[i] << endl;
    }
    return 0;
}