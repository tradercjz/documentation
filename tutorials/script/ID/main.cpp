#include "DolphinDB.h"
#include "Util.h"
#include <iostream>
#include <string>
using namespace dolphindb;
using namespace std;

int main(int argc, char* argv[]) {

    DBConnection conn;
    conn.connect("192.198.1.38", 8200, "testUser2", "123456");
    
    ConstantSP startDate = Util::createDate(2015, 1, 1);
    ConstantSP endDate = Util::createDate(2024, 12, 31);
    ConstantSP cols = Util::createString("*");
    vector<ConstantSP> funcArgs = {startDate, endDate, cols};
    auto tb = conn.run("query", funcArgs);
    
    cout << tb->getString() << endl;
    

    return 0;
}