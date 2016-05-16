### Ticket 

> 抢票脚本

* [微票](http://www.wepiao.com/)

可根据演出的 `onlineId` 直接下单，适用于不用选座位的演出，对要选座位的方案还不是很完备。

![screenshot](https://github.com/chxj1992/crawlers/blob/master/ticket/wepiao/screenshot.png)

API:

```
  http://crawlers.chxj.name/wepiao/without-seats?online_id=73c60ea249f746a78d3299902ade5e08
  
  其他参数：
  cookie=xxxxxxxxxx
  phone=15500000000
  address=天府软件园xxxxx
  name=陈晓敬
  ticket_number=2
```

另有[命令行工具](https://github.com/chxj1992/crawlers/blob/master/ticket/wepiao/run.py)，开多个并发抢 
