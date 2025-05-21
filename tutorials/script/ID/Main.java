package org.example;

import com.xxdb.DBConnection;
import com.xxdb.data.*;

import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;

public class Main {

    public static void main(String[] args) throws Exception {
        // 建立会话并登陆账号
        DBConnection conn= new DBConnection();
        conn.connect("192.198.1.38", 8200, "testUser2", "123456");

        // 访问全表数据
        BasicDate startDate = new BasicDate(LocalDate.of(2015,1,1));
        BasicDate endDate = new BasicDate(LocalDate.of(2024,12,31));
        BasicString cols = new BasicString("*");
        List<Entity> funcArgs = Arrays.asList(startDate, endDate, cols);
        BasicTable tb = (BasicTable)conn.run("query", funcArgs);
        System.out.println(tb.getString());
    }
}



