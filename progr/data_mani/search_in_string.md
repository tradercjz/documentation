# 搜索字符串

在DolphinDB中，有三种搜索字符串的方式：

1. 使用 [like](../../funcs/l/like.md) 函数和 [ilike](../../funcs/i/ilike.md) 函数。*like* 函数和 *ilike*
   函数的区别在于是否区分大小写。

   ```
   a=`IBM`ibm`MSFT`Goog`YHOO`ORCL;
   a ilike "%OO%";
   // output
   [0,0,0,1,1,0]

   a like "%oo%"
   // output
   [0,0,0,1,0,0]
   ```
2. [strpos](../../funcs/s/strpos.md) 函数能够检查字符串中是否包含子字符串，如果是，则返回子字符串在原字符串中的起始位置。

   ```
   strpos("abcdefg","cd");
   // output
   2

   strpos("abcdefg","d");
   // output
   3

   strpos("abcdefg","ah");
   // output
   -1
   ```
3. [regexFind](../../funcs/r/regexFind.md) 函数能够检查字符串中是否包含正则表达式表示的子字符串，如果是，则返回子字符串在原字符串中的起始位置。它与
   *strpos* 函数的区别是，*regexFind*
   函数可以使用正则表达式，并且能够指定开始搜索的位置。如果我们不需要指定开始搜索的位置，应该使用 *strpos* 函数，因为
   *strpos* 函数的效率比 *regexFind* 函数高。

   ```
   regexFind("FB IBM FB IBM AMZN", `IBM, 7);
   // output
   10

   regexFind("this subject has a submarine as subsequence", "\\b(sub)([^ ]*)");
   // output
   5

   regexFind("this subject has a submarine as subsequence", "\\b(sub)([^ ]*)", 10);
   // output
   19
   ```

Copyright

**©2025 浙江智臾科技有限公司 浙ICP备18048711号-3**
