#include <iostream>
#include <string>
#include <sstream>
#include <cstdio>

int main() {
    std::string command = "python2.7 nao_listner.py";
    FILE* pipe = popen(command.c_str(), "r");
    if (!pipe) {
        std::cerr << "Failed to run command: " << command << std::endl;
        return 1;
    }

    char buffer[128];
    while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
        std::string line(buffer);
        line = line.substr(0, line.size() - 1); 
        
        std::cout << line << std::endl;
    }

    pclose(pipe);
    return 0;
}
