"""
Blog 的中间件，包括访问统计中间件
"""
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from blog.models import VisitRecord, VisitStatistics, BlackList
from django.utils import timezone

DENY_VISIT_COUNT_THRESHOLD = 3000  # 同一次访问限制次数


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
            visit_record.ip = str(request.META.get('REMOTE_ADDR'))
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


class BlackListMiddleWare(MiddlewareMixin):
    """
    黑名单中间件
    """

    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_request(self, request):

        remote_ip = request.META['REMOTE_ADDR']  # 访问者的ip

        black_list = BlackList.objects.filter(is_disable=True).values_list('ip', flat=True)
        if remote_ip in black_list:
            return HttpResponseForbidden()

        # 如果访问者ip还存在session中，则表明还是同一次访问,不计入访问量
        if remote_ip not in request.session:
            request.session[remote_ip] = 1
        else:
            request.session[remote_ip] = int(request.session[remote_ip]) + 1
            if int(request.session[remote_ip]) > DENY_VISIT_COUNT_THRESHOLD:

                request_path = request.path_info  # 请求路径

                deny_reason = '1'  # 默认爬虫 deny_reason 1爬虫，2破解密码，3不友好用户

                # 如果访问记录是管理员后台,可考虑破解密码
                if 'xadmin' in request_path:
                    deny_reason = '2'

                try:
                    # 如果记录存在则更新
                    visit = BlackList.objects.get(ip=remote_ip)
                    visit.deny_reason = deny_reason
                    visit.modified_time = timezone.now()
                    visit.is_disable = True
                    visit.save()
                except ObjectDoesNotExist:
                    # 如果该记录不存在则新建
                    visit = BlackList()
                    visit.deny_reason = deny_reason
                    visit.ip = remote_ip
                    visit.created_time = timezone.now()
                    visit.is_disable = True
                    visit.save()
                # 禁止访问
                return HttpResponseForbidden()


class RealIpMiddleware(MiddlewareMixin):
    """
    如果存在代理，则从代理获取真实IP
    """
    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR']

