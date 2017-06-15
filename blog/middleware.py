"""
Blog 的中间件，包括访问统计中间件
"""

from django.utils.deprecation import MiddlewareMixin
from blog.models import VisitRecord


class VisitStatisticsMiddleWare(MiddlewareMixin):
    """
    站点访问量统计中间件
    """
    def __init__(self, get_response=None):
        """
        这段代码是抄袭自Django中间件
        :param get_response: 
        """
        self.get_response = get_response
        self.count = 0

    def process_request(self, request):

        remote_ip = request.META['REMOTE_ADDR']  # 访问者的ip
        # 如果访问者ip还存在session中，则表明还是同一次访问,不计入访问量
        if remote_ip not in request.session:
            request.session[remote_ip] = 1
            self.count = self.count + 1

        visit_record = VisitRecord()

        print(self.count)
        visit_record.http_host = request.META['HTTP_HOST']
        visit_record.http_user_agent = request.META['HTTP_USER_AGENT']
        visit_record.ip = request.META['REMOTE_ADDR']
        visit_record.server_name = request.META['SERVER_NAME']

        visit_record.save()  # 保存访问记录
        # print('HTTP_REFERER:', request.META['HTTP_REFERER'])

