from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django import views
from blog.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.

V_CODE = ""


# 登录
class Login(views.View):

    def get(self, request):
        form_obj = LoginForm()
        return render(request, "login.html", {"form_obj": form_obj})

    def post(self, request):
        res = {"code": 0}
        print(request.POST)
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        v_code = request.POST.get('v_code')
        print(v_code)
        print(V_CODE)
        # 先判断验证码是否正确
        if v_code.upper() != request.session.get("v_code", ""):
            res["code"] = 1
            res["msg"] = "验证码错误"
        else:
            # 校验用户名密码是否正确
            user = authenticate(username=username, password=pwd)
            if user:
                # 用户名密码正确
                login(request, user)
            else:
                # 用户名或密码错误
                res["code"] = 1
                res["msg"] = "用户名或密码错误"
        return JsonResponse(res)


# 首页
class Index(views.View):
    def get(self, request):
        return render(request, "index.html")


# 专门用来返回验证码图片的视图
def v_code(request):
    # 随机生成图片
    from PIL import Image, ImageDraw, ImageFont
    import random
    # 生成随机颜色的方法
    def random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    # 生成图片对象
    image_obj = Image.new(
        "RGB",  # 生成图片的模式
        (250, 35),  # 图片大小
        random_color()
    )
    # 生成一个准备写字的画笔
    draw_obj = ImageDraw.Draw(image_obj)  # 在哪里写
    font_obj = ImageFont.truetype('static/font/kumo.ttf', size=28)  # 加载本地的字体文件

    # 生成随机验证码
    tmp = []
    for i in range(5):
        n = str(random.randint(0, 9))
        l = chr(random.randint(65, 90))
        u = chr(random.randint(97, 122))
        r = random.choice([n, l, u])
        tmp.append(r)
        # 每一次取到要写的东西之后，往图片上写
        draw_obj.text(
            (i*45+20, 0),  # 坐标
            r,  # 内容
            fill=random_color(),  # 颜色
            font=font_obj  # 字体
        )

    # # 加干扰线
    # width = 250  # 图片宽度（防止越界）
    # height = 35
    # for i in range(5):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw_obj.line((x1, y1, x2, y2), fill=random_color())
    #
    # # 加干扰点
    # for i in range(40):
    #     draw_obj.point([random.randint(0, width), random.randint(0, height)], fill=random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=random_color())

    v_code = "".join(tmp)  # 得到最终的验证码
    # global V_CODE
    # V_CODE = v_code  # 保存在全局变量不行！！！
    # 将该次请求生成的验证码保存在该请求对应的session数据中
    request.session['v_code'] = v_code.upper()

    # 将上一步生成的图片保存在本地的static目录下
    # 每一次 都在硬盘中保存再读取都涉及IO操作，会慢
    # with open('static/oo.png', 'wb') as f:
    #     image_obj.save(f)
    #
    # with open('static/oo.png', "rb") as f:
    #     data = f.read()
    # 直接将生成的图片保存在内存中
    from io import BytesIO
    f = BytesIO()
    image_obj.save(f, "png")
    # 从内存读取图片数据
    data = f.getvalue()
    return HttpResponse(data, content_type="image/png")

