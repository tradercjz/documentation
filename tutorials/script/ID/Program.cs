using System;
using System.Collections.Generic;
using dolphindb;
using dolphindb.data;

namespace ConsoleApp6
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine(Utils.getAPIVersion());

            DBConnection conn = new DBConnection();
            conn.connect("192.198.1.38", 8200, "testUser2", "123456");

            BasicDate startDate = new BasicDate(new DateTime(2015, 1, 1));
            BasicDate endDate = new BasicDate(new DateTime(2024, 12, 31));
            BasicString cols = new BasicString("*");
            List<IEntity> funcArgs = new List<IEntity> { startDate, endDate, cols };
            BasicTable tb = (BasicTable)conn.run("query", funcArgs);

            Console.WriteLine(tb.toDataTable().Rows.Count);
        }
    }
}
