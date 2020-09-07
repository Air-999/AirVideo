from django.shortcuts import render
import socket,os

def home(request):
    context = {}
    Rootpath = getRootPath()
    if request.method == "GET" and request.GET:
        CurrentPath = request.GET.get("CurrentPath") + "/" + request.GET.get("Dir")
        context['Dir'] = request.GET.get("Dir")
    else:
        context['CurrentPath'] = ""
        context['Dir'] = ""
        CurrentPath = ""

    context['RootList'] = []  # 根目录列表
    for file in os.listdir(Rootpath):
        if(os.path.isdir(Rootpath+"/"+file)):
            context['RootList'].append(file)
    FileList = os.listdir(Rootpath+CurrentPath)   # 当前目录列表下的目录
    context['FileList'] = []
    for file in FileList:
        JDpath = Rootpath+CurrentPath+"/"+file
        Title = ""
        if(os.path.isfile(JDpath)):
            TitleList = file.split(".")
            TitleList.pop(len(TitleList)-1)
            for i in range(len(TitleList)):
                Title += TitleList[i]
                if( i != len(TitleList) - 1 ):
                    Title += "."
        else:
            Title = file
        File = {"File": file, "Type": 0, "Title": Title, "Image": CurrentPath + "/" + Title+".png"}  # Type为0文件夹

        Imagepath = Rootpath + CurrentPath
        if (os.access(Imagepath + "/" + Title+ ".png", os.F_OK)):
            File["Image"] = CurrentPath + "/" + Title+".png"
        elif(os.access(Imagepath + "/" + Title+ ".jpg", os.F_OK)):
            File["Image"] = CurrentPath + "/" + Title+".jpg"
        else:
            p = getChildDirImage(Imagepath + "/" + Title)
            if(p != False):
                File["Image"] = CurrentPath + "/" + Title + "/" + p
            else:
                if (os.access(Imagepath + ".png", os.F_OK)):
                    File["Image"] = CurrentPath + ".png"
                elif (os.access(Imagepath + ".jpg", os.F_OK)):
                    File["Image"] = CurrentPath + ".jpg"

        splitext = os.path.splitext(JDpath)[1]
        if (os.path.isdir(JDpath)):
            context['FileList'].append(File)
        elif(splitext == ".mp4" or splitext == ".m4v" or splitext == ".ogg" or splitext == ".webm"
            or splitext == ".mkv" or splitext == ".mov" or splitext == ".rmvb" or splitext == ".flv"
            or splitext == ".avi" or splitext == ".wmv" or splitext == ".m2ts"):
            File["Type"] = 1  # Type为1文件
            context['FileList'].append(File)
    context['CurrentPath'] = CurrentPath
    if CurrentPath != "":
        PathList = CurrentPath.split("/")
        PathList.remove("")
        context['PathEnd'] = PathList.pop()
        context['PathList'] = PathList
        List = []
        path = ""
        for i in range(len(PathList)):
            List.append([PathList[i], path])
            path += "/" + PathList[i]
        context['PathList'] = List
    else:
        context['PathList'] = []
    context['ALLOWED_HOSTS'] = get_host_ip()                       # 主机IP
    context['views_list'] = ["1", "2", "3", "4", "5", "6", "7", "8"]

    context['CarouselFirstIndex'] = 0                              # 轮播（Carousel）第一个指标
    context['CarouselIndex'] = [1, 2, 3, 4, 5, 6, 7]            # 轮播（Carousel）指标
    context['CarouselFirst'] = 1                                   # 轮播（Carousel）第一个项目
    context['CarouselList'] = ["2", "3", "4", "5", "6", "7", "8"]  # 轮播（Carousel）项目

    return render(request, 'home.html', context)

def Video(request):
    context = {}
    Rootpath = getRootPath()
    if request.method == "GET" and request.GET:
        CurrentPath = request.GET.get("CurrentPath")
        context['File'] = request.GET.get("File")
        context['CurrentPath'] = CurrentPath
    else:
        context['CurrentPath'] = ""
        CurrentPath = ""
    context['ALLOWED_HOSTS'] = get_host_ip()

    Title = ""
    FileList = context['File'].split(".")
    FileEnd = FileList.pop(len(FileList) - 1)
    for i in range(len(FileList)):
        Title += FileList[i]
        if (i != len(FileList) - 1):
            Title += "."
    context['Title'] = Title

    FileAll = Title + "." + FileEnd
    FileList = os.listdir(Rootpath + CurrentPath)  # 当前目录列表下的目录

    I = 0
    TitleList = []
    for file in FileList:
        JDpath = Rootpath + CurrentPath + "/" + file
        if (os.path.isfile(JDpath)):
            splitext = os.path.splitext(JDpath)[1]
            if(splitext == ".mp4" or splitext == ".m4v" or splitext == ".ogg" or splitext == ".webm"
            or splitext == ".mkv" or splitext == ".mov" or splitext == ".rmvb" or splitext == ".flv"
            or splitext == ".avi" or splitext == ".wmv" or splitext == ".m2ts"):
                I+=1
                fileInfo = [file, I]
                TitleList.append(fileInfo)

    ID = 0
    Long = len(TitleList)
    for i in range(Long):
        if (TitleList[i][0] == FileAll):
            ID = i
            break
    context['ID'] = ID+1
    Cai = Long - ID

    context['PreviousEnbie'] = 1
    context['NextEnbie'] = 1
    if (ID == 0):
        context['PreviousEnbie'] = 0
        context['Previous'] = TitleList[ID][0]
    else:
        context['Previous'] = TitleList[ID - 1][0]
    if (ID == Long-1):
        context['NextEnbie'] = 0
        context['Next'] = TitleList[ID][0]
    else:
        context['Next'] = TitleList[ID + 1][0]
    if(Long<7):
        context['FileList'] = TitleList
        context['PreviousEnbie'] = 0
        context['NextEnbie'] = 0
    else:
        List = []
        if(ID<3):
            for i in range(6):
                List.append(TitleList.pop(0))
            context['FileList'] = List
        else:
            if (Cai < 4):
                for i in range(6):
                    List.append(TitleList.pop())
                List.reverse()
                context['FileList'] = List
            else:
                for i in range(6):
                    List.append(TitleList[ID-2+i])
                context['FileList'] = List

    return render(request, 'Video.html', context)

def text(request):
    context = {}
    context['ALLOWED_HOSTS'] = get_host_ip()
    context['hello'] = 'Hello World2!'
    context['views_list'] = ["1","2","3","4","5","6","7","8"]
    path2 = "F:/AirVideo/视频网站"
    context['DirList'] = str(os.listdir(path2))  # 目录列表
    return render(request, 'text.html', context)
# ----------------------------------------------------------------------------------------------------------------------
def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

def getRootPath():
    fo = open("D:/AirVideo/ProgramFiles/web/web/path.txt", "r", encoding="utf8")
    lines = fo.readlines()
    if (len(lines) > 0):
        return lines[0].strip()
    return ""

def getChildDirImage(Imagepath):
    if(os.path.isdir(Imagepath)):
        for file in os.listdir(Imagepath):
            if(os.path.isfile(Imagepath+"/"+file)):
                if(file.endswith(".jpg") or file.endswith(".png")):
                    return file
    return False
                                    
def get_filelist():
    return False