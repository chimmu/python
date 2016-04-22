from matplotlib import pyplot as plt
from matplotlib.figure import Figure

colors = ['red', 'orange', 'green', 'yellow', 'blue', 'purple', 'gray', 'gold']
def draw_circle(labels, percents, fileName):
    plt.figure(figsize=(6,9))
#     labels =['John', 'Jim', 'Jerry', 'Jack']
#     percent = [60, 20, 10, 10]
    color = colors[0:len(labels)]
#     explode = (0, 0, 0, 0)
    patches,l_text,p_text = plt.pie(percents,labels=labels,colors=color,
                                labeldistance = 1.05,autopct = '%3.1f%%',shadow = False,
                                startangle = 90,pctdistance = 0.5)

#labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
#autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
#shadow，饼是否有阴影
#startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
#pctdistance，百分比的text离圆心的距离
#patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本

#改变文本的大小
#方法是把每一个text遍历。调用set_size方法设置它的属性
    for t in l_text:
        t.set_size=(30)
    for t in p_text:
        t.set_size=(20)
# 设置x，y轴刻度一致，这样饼图才能是圆的
    plt.axis('equal')
    plt.legend()
    plt.savefig(fileName)
    plt.close()
#     with open(fileName, 'wb') as f:
#         f.write(plt.)
#     plt.show()
    
if __name__ == '__main__':
    draw_circle(['John', 'Jim', 'Jerry'], [60, 20, 10], 'demo.jpg')