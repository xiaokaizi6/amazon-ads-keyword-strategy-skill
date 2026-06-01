# cpc广告的一些技术要点：5个campaign法、AD group设置、BUDGET预算50%倍增法、Bid设置50%倍增法、广告时间段的精细化管理、关键词设定/布局方法、提高CR的方法……

- 文章链接: https://www.wearesellers.com/question/12878
- 发布人名称: 环球万象
- 发布时间: 2019-09-03
- 站内元信息: 回复 62 / 关注 629 / 浏览 31309
- 圈子/标签: Amazon, Amazon PPC
- 爬取到的公开回复数: 0
- 爬取到的评论数: 6

## 发布人正文

广告组结构：5个campaign法

（1） AUTO-broad
检测一下出来的词和产品相关性大不大，不大的话说明亚马逊对你的产品定位不准
一定要坚持跑下去（至少3个月），跑到再也没有新词出来为止
Auto里面出现的asin，主要是有人在送评，用户看到你的广告点击了

（2）用suggested的关键词单独建一个targetcampaign-phrase
一定要全部用上，（1）和（2）是亚马逊数据生成的最精确的数据，相对来说比较长尾了。
如果数量太少，说明listing的质量差，亚马逊对它的识别度不高

（3）Keyword research得到的词 collectingKeyword-broad
第3方关键词的精准性远低于亚马逊的suggested

（4） 跑半个月到一个月（预算越高需要的时间越短），从(1)（2）(3)的search term筛选出winningKeyword-phrase。The more data you have in the beginning, the better!!!!!!
初期高预算积累大量数据，为以后发展提供大量数据，后期预算反而会少
选出来的词一点要在原来的campaign中negative掉

（5）从前面4个campaign中筛选winningKeyword-exact
5个组同时运行
Keyword升级后要在之前组里Negative掉，把表现不好的词放回原来的组。
不断调整，最终实现ACOS、CR和CTR在BROAD-PHRASE-EXACT上不断优化的层级结构。当AUTO组没有新的词产生，才可以关闭，至少运行3个月
 转化率 CR （Conversion Rate）= orders÷clcks
 点击率CTR （Click through rate）= clicks÷impressions
 广告成本AcoS（Advertising cost of sales）= total ad spend ÷ total sales from advertising

Winning Keyword 门槛标准

大概的参考值，可以设置自己的门槛

（1）broadcampaign升级到Phrasecampaign的门槛
ACOS不用特别纠结值的高低，只要是大于销售利润率15-20%以内，都是可以考虑的。20%作为临界点是因为相当于把S单的钱拿来做广告。
CTR不小于3（亚马逊PPC的CTR平均值2-3）
conversion rate最重要指标 > 8 percent 

（2）phrasecampaign升级到EXACTcampaign的门槛
conversion rate > 20 percent
做决定的周期建议为一个月，周期越长数据越准确，升级后原来组里的词不删用negative。

5个 campaign，要有耐心。先看一下Business report下产品自然转化率的CR（亚马逊平均值为4，旺季8），比如10%，那么给PPC下每个SEARCH TERM10 个CLIIKS的机会，十个clicks有1个order就达到了10%的平均水平可以保留，如果超过10个点击没有转化就可以negative。如果还没达到10个clicks再等待一下看看。

AD group设置
 
需要进一步细化关键词层级时，可以在Campaign下设置AD group，按照bidding 分BID+ 组， BID ++ 组，对每一个层级设置threshold门槛。刚开始不建议尝试。

BUDGET预算50%倍增法
原则：为越精准的campaign付越多的钱
保守的做法：
PHRASE= BORAD X 1.5
EXACT = PHRASE X 1.5
激进的做法: EXACT = PHRASE X 2

Bid设置50%倍增法
Broad campaign bidding: default bid: winning cost-per-click bidsby category (后台可以下)如果想要快一点， x 1.5
Phrase campaign bidding: est page one bid x 1.5 or 2 forspecific Keyword
Exact campaign bidding: est page one bid x 2 or 2.5 for specific Keyword

Bid+的作用
当Keyword在第二页时，允许把bid加价50%上首页。
raises bids in this campaign by up to 50P more than your defaultwhen you are eligible in the top of search results.
可以下载adplacement report 看看效果
Bid+ 可以用在phrase和 exactcampaign 上面使用。
50%在亚马逊是一个很好的竞价策略。

广告时间段的精细化管理
 
高峰期WEEKDAYS:9AM – 5PM ( is almost double than therest of the hours)，把预算调成平常的1.5倍

Monday/Tuesday： highly converted days 把预算调成平常的1.5倍，其中9AM – 5PM调成2倍

低迷期Weekendsand holidays 转化比较低，预算调低

关键词设定

1、选定root Keyword，一般1到3个
用后面的工具找长尾词的时候，可能也会对rootKeyword有所补充

2、按照工具的精准度开始生成短尾、长尾词

1）Amazonsearch box + google search box
亚马逊搜索框rootKeyword+26字母/数字。
老外买东西之前喜欢通过谷歌搜索，通过链接进入亚马逊。谷歌的搜索框、相关搜索的词都可以用，搜出来在首页的网站进去看看他们还用了什么关键词

2） Google adwords (generating ) GKP 
信息类的词都不要，筛选购买意图高的词，精准流量精准转化，50以上的搜索量就可以考虑

3）merchantwords
不精准且更新慢，搜索量虚高，关键词老旧。只看500搜索量以上就行

4）ubersuggets
按shopping来搜索，但它有很多非电商词汇

5）keywordsinspector
用反查PPC的功能，它是在前台去搜索得到的词，你不知道对手的设置是broadphrase exact 要对出来的结果反推对手设置的词

Keyword时间跨度短，可能是被对手negative掉了，时间跨度越长的词越可靠

非英文语境下的关键词设定
同理用上面的124步骤
用 Googlesearch bar. http://www.google.com/ncr = google.com
http://www.google.co.uk/ncr = google.co.uk
国家名字后缀加 /ncr

关键词在title和search term中的布局方法

客户搜索时，亚马逊内部搜索引擎是按照单个exact的词抓取的，而不是phrase，亚马逊会自动组合title 和search中的词。移除重复的关键词，Title和search term中的词只最好出现一次。
不用把searchterm词都填满，相关性差的只会带来垃圾流量

同序的词权重大于乱序的，做searchterm的时候，词序按照最有逻辑的方式来排列
Search term会自动忽略标点符号，单复数只要放一个，有无ing的也只要一个
As you see below, Amazon can handle “basic” stemming. I have notfound a definition of “basic” but my interpretation is plurals and common otherendings such as “ing.” Anything beyond that I would consider adding as anothersearch term.
据说每行填一个词可以提高该词的权重

PPC报表的用处
 
（1）Performance over time
可以按照DAYS， MONTHS YEARS 来显示，日期上面最为精确。可以通过这个表格大致分析出来哪一天点击的人多，周末和工作日的区别，可以细化去分析每一天的 total spend 和点击 大幅下降和增加的原因。
在表现好的某一天加大预算，因为budget会偏向表现好的Keyword，吃掉其他词的机会。

（2）Performance BY SKU
用于针对变体下的各个SKU 进行测试，有助于选择最好的，避免竞争, 而且监测打造爆款的SKU发展。
类似的产品最好做成一个变体，打一样的广告，跑半个月，从其中选出最好的一个SKU。最后把所有变体广告的预算放在它上面。
经验：一开始不做变体，作为单独的SKU养，做到比较好了再合并。

（3）Performance by placement
衡量广告的效果，bid+效果好的说明产品效果不错，可以直接手工加价。如果bid+没有什么效果，说明listing和广告有待提高。

（4）Estimated page 1 report
是bid的基准点，按1.5 2 2.5的倍数往上走

（5）other asin report
很重要！客户点击广告但是跳转到你的其他产品上并购买。
1说明该产品值得做广告
2通过跳转到其他便宜的产品上来S单，销售额会算到totalsales，去冲击Acos

（6）Campaign performance report
要用数据透视表。

（7）search term report
找到消费者的真实搜索Keyword，是winning Keyword的来源。

提高转化率CR的方法
本质是CONTENT MAREKTING
（1）内页优化和SEO : search term, product description, image, bullet points
（2）review 数量和质量以及点YES NO 自己写个软差评，点no点成most critical 一个review很差的产品不想它死掉，可以找一个好的跟它合并，把好评点到前面去，等差评多的产品评论解决好再拆分
（3）questions 和 vote 老外很爱看QA，功能性产品一定要有
（4）add to wish and give away wishlist要点进榜才有意义
（5）S单 model 关键要掌握节奏，稳住排名

广告曝光特别低的原因和解决方法
 
1 Adding more Keywords
2 Target only a few Keywords
3 Ad 5 SKUs to each Ad group
4 Raise bids
5 Change Title and Description Product Page to include allKeywords
6 Up the Daily Budget
7 Wait a few Days
8 Improving ad relevance especially for title 
Amazon doesn’t advertise your products for certain keywords unless they think your product listingis relevant enough.
Try to talk with amazonand tell them what you are 
The automatic campaign can be used as a verification tool that tells you if Amazon understandsexactly what product you are selling. If they do, great. If they don’t, tweakyour listing until they do.
Traffic validation 防止恶意点击机制

亚马逊有筛选和移除PPC非法点击机制。

广告被暴力点击钱不会真的扣，过几天系统会确认非法点击。只是当天的budget会被点爆。
Clicks may be invalidated for the following reasons: 
1 Unusual click patterns
2 Clicks identified asbeing machine generated
3 Duplicated clicks
万一被人恶意点击，以click fraud为主题向亚马逊申诉，理由是以上3个之一

## 评论区

### 评论 1
- 评论人名称: 米兔
- 评论时间: 2019-09-07 17:35
- 点赞数量: 未显示

不明觉厉
mark
感冒了，脑子发懵的时候看到
等清醒的时候再看看能不能看懂一点点
谢谢楼主

### 评论 2
- 评论人名称: ponyboy
- 评论时间: 2019-11-05 12:05
- 点赞数量: 未显示

click fraud 是怎么判断出来的啊？

### 评论 3
- 评论人名称: kylelee
- 评论时间: 2020-01-09 09:58
- 点赞数量: 未显示

这中英混合的真的好ga

### 评论 4
- 评论人名称: 霉霉500
- 评论时间: 2021-10-29 10:54
- 点赞数量: 未显示

写得挺用心的，但是看得一脸蒙

### 评论 5
- 评论人名称: 定当技惊四方
- 评论时间: 2021-10-30 17:07
- 点赞数量: 未显示

@kylelee:看的的 有点费劲

### 评论 6
- 评论人名称: 常青藤
- 评论时间: 2022-06-17 11:54
- 点赞数量: 未显示

2年前认真研究过了，其实根据自己的产品来调整的话，当时还是很有用处的；现在忘得差不多，重新再来研究下
