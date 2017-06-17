"""
Blog 的中间件，包括访问统计中间件
"""
from django.core.exceptions import ObjectDoesNotExist
from django.utils.deprecation import MiddlewareMixin
from blog.models import VisitRecord, VisitStatistics
from django.utils import timezone


class VisitRecordMiddleWare(MiddlewareMixin):
    """
    游客访问记录中间件 
    将非管理员操作记录到数据库中
    """

    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_request(self, request):
        request_path = request.path_info  # 请求路径

        #  访问管理后台不记录
        if 'xadmin' not in request_path:
            visit_record = VisitRecord()

            visit_record.http_host = request.META.get('HTTP_HOST')
            visit_record.http_user_agent = request.META.get('HTTP_USER_AGENT')
            visit_record.ip = request.META.get('REMOTE_ADDR')
            visit_record.server_name = request.META.get('SERVER_NAME')
            visit_record.http_path = request.path_info

            visit_record.save()  # 保存访问记录


class VisitStatisticsMiddleWare(MiddlewareMixin):
    """
    站点访问量统计中间件
    统计站点每天运行中的访问量，包括总共访问量，单日访问量，总共积累IP，当日IP
    """

    def __init__(self, get_response=None):
        """
        __init__抄袭自Django中间件
        :param get_response: 
        """
        self.get_response = get_response
        self.count = 0

    def process_request(self, request):

        remote_ip = request.META['REMOTE_ADDR']  # 访问者的ip
        # 如果访问者ip还存在session中，则表明还是同一次访问,不计入访问量
        if remote_ip not in request.session:
            request.session[remote_ip] = 1
            try:
                # 如果记录存在则更新
                visit = VisitStatistics.objects.get(created_date=timezone.now())
                visit.today_visit += 1
                visit.save()
            except ObjectDoesNotExist:
                # 如果该记录不存在则新建
                visit = VisitStatistics(created_date=timezone.now())
                visit.today_visit += 1
                visit.save()


class AntiSpiderMiddleWare(MiddlewareMixin):
    """
    反爬虫中间件
    """
    pass
    # TODO 反爬虫中间件 2017年6月16日11:39:35
