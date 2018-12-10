from pageTest.htmlSpider.htmlSpider import HtmlSpider
from pageTest.htmlSpider.htmlUtil import HtmlUtil


# strUrl = 'http://www.ip138.com/'
strUrl = 'http://2018.ip138.com/ic.asp'
# strUrl = 'http://www.baidu.com'

htmlSpiderObj = HtmlSpider()
htmlUtilObj = HtmlUtil()

dictProxyMsgObj = htmlSpiderObj.getBuildUpProxyMsgObj('high', '113.106.94.213', 80)

# bytePageContent = htmlSpiderObj.getHtmlMsg(strUrl)
# strPageContent = htmlSpiderObj.getHtmlStrMsg(strUrl)
strPageContent = htmlSpiderObj.getProxyHtmlStrMsg(strUrl, dictProxyMsgObj)
# strPageContent = bytePageContent.decode('gb2312', 'ignore')
# print(strPageContent)
# tagLabel = htmlUtilObj.getHtmlEncode(bytePageContent)
# print(tagLabel)


# strHtmlContent = htmlSpiderObj.getProxyHtmlStrMsg(strUrl, dictProxyMsgObj)
print(strPageContent)