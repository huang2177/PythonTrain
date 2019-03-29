from django.shortcuts import *
from mysql import connector
from mysql.connector.cursor_cext import CMySQLCursorDict


# ====================班级操作=========================
# 获取班级列表
def clazz(request):
    data = execute_sql('select * from class order by c_id', True)
    return render(request, 'clazz.html', {'data': data})


# 添加班级
def add_clazz(request):
    if request.method == 'GET':
        return render(request, 'add_clazz.html')
    else:
        c_id = request.POST.get('c_id')
        c_name = request.POST.get('c_name')
        execute_sql(('insert into class (c_id,c_name) values ("%s","%s")' % (c_id, c_name)), False)

        return redirect('/clazz/')


# 编辑指定班级
def edit_clazz(request):
    c_id = request.GET.get('c_id')
    print(c_id)
    if request.method == "GET":
        c_id = request.GET.get('c_id')
        result = execute_sql(('select * from class where c_id="%s"' % c_id), True)
        return render(request, 'edit_clazz.html', {'data': result[0]})
    else:
        c_id = request.POST.get('c_id')
        c_name = request.POST.get('c_name')
        execute_sql(('update class set c_name="%s" where c_id ="%s"' % (c_name, c_id)), False)

        return redirect('/clazz/')


# 删除指定班级
def del_clazz(request):
    c_id = request.GET.get('c_id')
    execute_sql(('delete from class where c_id = "%s"' % c_id), False)
    return redirect('/clazz/')


# ====================教师操作=========================
# 获取老师列表
def teachers(request):
    data = execute_sql('select * from teacher', True)
    return render(request, 'teachers.html', {'data': data})


# ====================学生操作=========================
# 获取老师列表
def students(request):
    data = execute_sql('select student.s_name, class.c_name, student.s_id '
                       'from class '
                       'right join student on class.c_id = student.c_id order by s_id', True)
    return render(request, 'student.html', {'data': data})


# 添加学生
def add_student(request):
    if request.method == 'GET':
        data = execute_sql('select c_id,c_name from class', True)
        return render(request, 'add_student.html', {'clazz': data})
    else:
        c_id = request.POST.get('c_id')
        s_name = request.POST.get('s_name')
        execute_sql(('insert into student (c_id,s_name) values ("%s","%s")' % (c_id, s_name)), False)

        return redirect('/students/')


# 编辑指定学生
def edit_student(request):
    s_name = request.GET.get('s_name')
    if request.method == "GET":
        clazz_data = execute_sql('select c_id,c_name from class', True)
        stu = execute_sql(f'select c_id,s_id from student where s_name = "{s_name}"', True)
        return render(request,
                      'edit_student.html',
                      {'s_name': s_name, 'stu': stu[0], 'clazz': clazz_data})
    else:
        s_id = request.GET.get('s_id')
        c_id = request.POST.get('c_id')
        s_name = request.POST.get('s_name')
        execute_sql(('update student set s_name="%s",c_id = "%s" where s_id ="%s"' % (s_name, c_id, s_id)), False)

        return redirect('/students/')


# ====================操作数据库=========================
# 执行sql语句，并获取结果
def execute_sql(sql, is_select):
    conn = connector.connect(user='root', password='root', database='django', use_unicode=True)
    cursor = conn.cursor(CMySQLCursorDict)
    cursor.execute(sql)
    data = None
    if is_select:
        data = cursor.fetchall()
    else:
        conn.commit()
    cursor.close()
    conn.close()
    return data
