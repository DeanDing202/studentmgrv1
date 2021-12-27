from django.shortcuts import render,HttpResponse,redirect
from django.conf import settings #导入模块取出settings中存储的数据库接口值
from utils.sqlhelper import MysqlConn #引入连接数据库模块
from utils import func
# Create your views here.
def index(request):
    '''返回静态页面'''
    # step 1: 获取连接数据库接口信息
    conn_info = settings.DATABASES['mysql']
    # step 2: 实例化数据库类MysqlConn
    obj_db_conn = MysqlConn(conn_info)
    # step 3: 准备sql语言
    sql = ""
    input_str = ""
    if request.method == 'GET': #GET 请求，展示所有数据   ------Dean
        sql = """SELECT SNo,SName,Gender,Birthday,Mobile,Email,Address FROM Student"""
    elif request.method == 'POST': #POST 请求，执行查询后结果的相应流程
        input_str = request.POST.get('txtquery') # 'txtquery'对于index.html文件中查询name
        if func.is_SpecChar(input_str):#是否有中文判断，解决Birthday为date字段sql语法的错误问题---Dean
            sql = """SELECT SNo,SName,Gender,Birthday,Mobile,Email,Address FROM Student 
                                WHERE SNo LIKE '%s' or SName LIKE '%s' or Gender LIKE '%s' or Mobile LIKE '%s' 
                                or Email LIKE '%s' or Address LIKE '%s' 
                                """ % ("%" + input_str + "%", "%" + input_str + "%", "%" + input_str + "%",
                                       "%" + input_str + "%","%" + input_str + "%", "%" + input_str + "%")
        else:
            sql = """SELECT SNo,SName,Gender,Birthday,Mobile,Email,Address FROM Student 
                        WHERE SNo LIKE '%s' or SName LIKE '%s' or Gender LIKE '%s' or Birthday LIKE '%s' 
                        or Mobile LIKE '%s' or Email LIKE '%s' or Address LIKE '%s' 
                        """%("%" + input_str + "%", "%"+input_str +"%", "%" + input_str + "%", "%" + input_str + "%",
                             "%" + input_str + "%", "%" + input_str + "%", "%" + input_str + "%")#模糊查询+"%" ------Dean
    # step 4: 执行取出数据
    obj_db_conn.get_db_data(sql)
    # step 5: 根据结果展示相关信息
    if obj_db_conn.flag == 1:
        # 成功的数据格式：[(),(),(),......],key = students在html模板里面对应并自动识别 ------Dean
        return render(request, 'index.html', context={'students': obj_db_conn.result, 'input_str':input_str})#'input_str':input_str，查询条件留在查询框中
    else:
        return render(request, 'error.html', context={'msg': obj_db_conn.msg})

def student_delete(request):
    '''删除学生信息'''
    #获取传递的sno学号（sno跟前端变量一直）
    sno = request.GET.get('sno')
    conn_info = settings.DATABASES['mysql']
    obj_db_conn = MysqlConn(conn_info)
    sql = """Delete from Student where sno = '%s'"""%(sno)
    obj_db_conn.update_db(sql)
    if obj_db_conn.flag == 1:
        # 如果数据成功删除，重新获取删除后数，redirect函数重新获取
        return redirect("/") #redirect: 没出错重新查询数据库,相当于重新执行index(request)函数
    else:
        return render(request, 'error.html', context={'msg': obj_db_conn.msg})

def conn_db(request):
    '''连接数据库'''
    #获取数据库连接信息
    conn_info = settings.DATABASES['mysql']
    #实例化一个数据库类
    obj_conn_db = MysqlConn(conn_info)
    #准备sql语句
    sql = """SELECT SNo,SName,Gender,Birthday,Mobile,Email,Address FROM Student"""
    #获取数据库数据
    obj_conn_db.get_db_data(sql)
    #判读异常
    if obj_conn_db.flag == 0:
        #展示错误信息: 错误值传进页面的msg变量------Dean
        return render(request, 'error.html', context={'msg':obj_conn_db.msg})
    else:
        #无异常，数据库获取的数据在页面展示
        return HttpResponse(str(obj_conn_db.result))