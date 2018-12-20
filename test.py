from proxyPool.pageTest.htmlSpider.htmlSpider import HtmlSpider
from proxyPool.pageTest.htmlSpider.htmlUtil import HtmlUtil


# strUrl = 'http://www.ip138.com/'
strUrl = 'http://2018.ip138.com/ic.asp'
# strUrl = 'http://www.dangdang.com/'

# proxyStrurl = 'http://www.89ip.cn/'

strProxyIp, strProxyPort, strProxyType = '27.24.215.49', '57248', 'https'
# strProxyIp, strProxyPort, strProxyType = '112.16.172.107', '48399', 'http'
# strProxyHost = strProxyIp + ':' + strProxyPort

htmlSpiderObj = HtmlSpider()
htmlUtilObj = HtmlUtil()

# dictProxyMsgObj = htmlSpiderObj.getBuildUpProxyMsgObj('HTTPS', 'https://218.59.228.18', 61976)

# bytePageContent = htmlSpiderObj.getHtmlMsg(strUrl)
# strPageContent = htmlSpiderObj.getHtmlStrMsgNew(strUrl)
strPageContent = htmlSpiderObj.getProxyHtmlStrMsgNew(strUrl, strProxyIp + ':' + strProxyPort, strProxyType)
# strPageContent = bytePageContent.decode('gb2312', 'ignore')
# print(strPageContent)
# tagLabel = htmlUtilObj.getHtmlEncode(bytePageContent)
# print(tagLabel)


# strHtmlContent = htmlSpiderObj.getProxyHtmlStrMsg(strUrl, dictProxyMsgObj)
print(strPageContent)