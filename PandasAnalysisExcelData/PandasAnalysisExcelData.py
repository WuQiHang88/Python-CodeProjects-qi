import pandas as pd  ##引入pandas库（常用来进行数据分析和分析库）
import matplotlib.pyplot as plt ## 引入matplotlib（用于数据据可视化的基础库）
import seaborn as sns  ##基于matplotlib构建的高级可视化库
from matplotlib import rcParams    ## rcParams是matplotlib的一个全局配置参数，用于设置图形的各种属性
from sklearn.linear_model import LinearRegression   ## sklearn是python中，广泛使用的机器学习库，可用于预测和建模
from scipy import stats  ## 科学计算的python库，stats是统计模块
import matplotlib.font_manager as fm ## 用来管理字体的模块
import warnings  ## 用于控制python中的警告信息
import os  ## 提供与操作系统进行交互的功能
import matplotlib  #

# ======================
# 1. 中文显示解决方案（增强版）
# ======================
warnings.filterwarnings('ignore')
plt.rcParams['axes.unicode_minus'] = False

# 动态字体配置（跨平台兼容）
try:  ##（try块后必须加except块，是异常处理机制的开始部分）
    # 尝试多平台字体路径
    font_path = None  ##初始化一个变量，让它赋值位none，用于存储找到的中文字体文件路径
    possible_paths = [   ## 定义一个列表，下面存放不同的字体路径
        'C:/Windows/Fonts/msyh.ttc',  # Windows
        '/System/Library/Fonts/STHeiti.ttc',  # macOS
        '/usr/share/fonts/wqy-zenhei.ttc'  # Linux
    ]

    # 查找存在的字体路径
    for path in possible_paths: ## 遍历前面的possible_paths列表
        if os.path.exists(path): ## os是一个函数，用于判断文件是否存在，所以这句代码是为了检查文字路径是否存在
            font_path = path  ## 如果当前路径对应的文件存在，将其赋值给前面的空变量font_path
            break  ##找到路径，就跳出for循环

    if font_path:  ##查看这个变量是否不为None，即是否找到字体文件路径
        # 注册字体并强制全局设置
        font_prop = fm.FontProperties(fname=font_path)  ##使用 matplotlib.font_manager.FontProperties 类创建一个字体属性对象font_prop，并指定文字字体的路径为font_path
        plt.rcParams['font.family'] = font_prop.get_name()  ##设置全局的字体属性，将字体家族设置为找到的字体的名称，其中，plt.rcParams是一个字典，用于存储全局配置参数
        matplotlib.rcParams.update({'font.family': font_prop.get_name()})  ## 更新matplotlib的全局字体属性，确保使用matplotlib绘图的地方都使用指定字体
        print(f"✅ 字体加载成功: {font_prop.get_name()}")  ##成功则打印文字加载成功
    else:
        raise FileNotFoundError("未找到系统级中文字体文件")

except Exception as e:  ## except块可以捕获任何类型的异常，并把异常的赋值对象给到变量e
    print(f"⚠️ 字体加载异常: {str(e)}")
    # 降级方案：直接指定字体名称
    fallback_fonts = ['Microsoft YaHei', 'SimHei', 'STHeiti', 'WenQuanYi Zen Hei'] ##定义一个备用字体名称列表，当之前根据字体路径加载失败时，尝试从这个列表中，选择可用字体
    available_fonts = [f for f in fallback_fonts if f in fm.get_font_names()] ##函数fm.get_font_names()可用返回所有可用字体名称列表，后面的 f for in fallback_fonts，相当于遍历fallback_fonts中，所有可用的字体名称，并把结果存储在available_fonts列表中
    if available_fonts: ##检查列表是否不为空
        plt.rcParams['font.family'] = available_fonts[0] ## 如果找到可用的备用字体，将matplotlib.pyplot的全局字体属性font_family设置为available_fonts 列表中的第一个字体名称。
        print(f"🔄 回退到字体: {available_fonts[0]}")
    else:
        print("❌ 警告：系统中未找到任何中文字体")

# 打印当前生效字体（调试用）
print("当前生效字体:", plt.rcParams['font.family'])

# ======================
# 2. 可视化样式配置（保持不变）
# ======================
PALETTE = sns.color_palette("ch:s=.25,rot=-.25", 10) ##用color_palette函数创建一个颜色调色板，ch:s=25,rot=-25，是一个基于连续色调的颜色空间定义，其中，s=0.25表示颜色的鲜艳程度，rot为旋转角度，最终将调色板赋值给变量PALETTE
sns.set_palette(PALETTE) ##使用set_palette函数将之前生成的调色板PALETTE设置为seaborn绘图时默认使用的调色板

sns.set_style("whitegrid", {  ##设置绘图风格，这里的whitegrid表示在白色背景上绘制网络线
    'grid.linestyle': ':',   ## 将网络线的样式设置为虚线
    'grid.color': '#E0E0E0',  ##网络线的颜色设置为浅灰色
    'axes.edgecolor': 'black',  ## 将坐标轴的边框设置为黑色
    'axes.linewidth': 0.8   ##将坐标轴的边框线宽度设置为0.8
})
## plt.rcParams 是 matplotlib.pyplot 中的一个全局参数配置字典，通过修改其中的键值对可以设置 matplotlib 绘图的各种属性
plt.rcParams['figure.figsize'] = [12, 7]  ## 将图形的大小设置为宽12英寸，高7英寸
plt.rcParams['savefig.dpi'] = 300   ##设置保存图形时的分辨率为300dpi，分辨率越高，保存的图形约清晰
plt.rcParams['font.size'] = 12  ## 将默认字体大小设置为12磅
plt.rcParams['axes.titlesize'] = 16  ##将坐标轴标题的字体大小设置为16磅
plt.rcParams['axes.labelsize'] = 14  ##将坐标轴标签的字体大小设置为14磅


# ======================
# 3. 增强可视化函数（关键修改：显式指定字体）
# ======================
def enhanced_barplot(data, x, y, title, filename):  ## 定义一个参数，该参数接受五个参数，data：pandas数据框，包含绘图所需参数；x：x轴列名；y：y轴列名；title：柱状图标题；filename：保存生成的文件名
    """专业级柱状图（修正字体问题）"""
    plt.figure(figsize=(12, 7))  ## 与前面类似，使用 matplotlib.pyplot 的 figure函数创建一个新的图形对象，并设置图形大小为宽12英寸，高7英寸
    ax = sns.barplot(x=x, y=y, data=data,  ## 使用seaborn的barplot函数绘制柱状图，其中，x=x，y=y，指定数据框data中用作x轴和y轴的数据列，data=data，即表示告诉函数，从右边的data数据框中，获取x和y所指定的数据列
                     hue=y, legend=False,  ##根据y列的值给柱状图上色，legend=False表示不显示图例
                     palette=PALETTE,  ## 使用之前定义好的颜色调色板PALETTE来给柱状图上色
                     edgecolor='black', ## 设置边框颜色为黑色
                     linewidth=0.8)  ## 设置柱状图边框线的宽度为0.8
     ## 最后，把这些设置好的值，赋值给ax
    # 显式设置字体属性
    ax.set_title(title, fontproperties=font_prop, pad=20)  ## title是传入标题的文本，fontproperties=font_prop使用之前加载好的字体属性对象font_prop来设置标题字体，pad=20表示标题与图表间的垂直间距为20个点
    ax.set_yticklabels(ax.get_yticklabels(), fontproperties=font_prop)  ## 获取Y轴标签，使用font_prop字体属性对象来设置标签字体
    ax.set_xlabel(None, fontproperties=font_prop)  ##设置x标签，其中None表示不显示x轴标签

    # 动态调整标签位置
    max_value = data[x].max()   ##获取数据框data中，x列的最大值
    for p in ax.patches: ## 遍历柱状图中，每个柱状图对象
        width = p.get_width()  ##获取当前柱状图宽度
        ax.text(width + max_value * 0.01,   ##ax.text表示在图片添加文本标签，width + max_value * 0.02：设置文本标签的 x 坐标，位置在柱状图宽度基础上加上 x 列最大值的 2%，用于动态调整标签位置使其在柱状图右侧。（即数据距离每个柱状图对象的距离）
                p.get_y() + p.get_height() / 2,  ##设置文本标签的y坐标，位于柱状图的垂直中心位置
                f'{width:.1f}',  ##格式化文本标签内容，显示柱状图宽度，保留一位小数
                va='center', ##设置文本标签垂直对齐方式位居中
                fontproperties=font_prop,  ##数值标签，即设置字体
                fontsize=10)    ##设置字体大小

    sns.despine(left=True, bottom=True)  ##移除图片左侧和底部的边框线
    plt.tight_layout()  ##自动调整子图参数，使图表元素，如标题，标签等，不会相互重叠，布局合理
    plt.savefig(filename, bbox_inches='tight')  ##使生成的图表保存为指定的文件名，bbox_inches='tight'表示只包含图表内容，不包含多余的空白区域
    plt.show()


def modern_pie(data, title, filename):  ##接受三个参数，分别是数据，标题和文件名称
    """现代化饼图（修正字体问题）"""
    data = data.sort_values(ascending=False).head(6)  ##这里对data进行处理，首先使用sort_values 方法对数据进行降序处理（ascending=False 表示降序），然后使用head（8）方法选取排序后数据的前8个元素
    explode = [0.1 if i == data.idxmax() else 0 for i in data.index]  ##创建一个叫explode的列表，在这里是指定最大的那块扇形，与其他扇形的偏移量为0.1，（即把最大的扇形与其他扇形用空白分隔开），然后把0给到其他data.index中的每个索引值

    fig, ax = plt.subplots()  ##创建一个新的图形对象fig和一个Axes对象ax，fig代表整个图形窗口而ax用来绘制具体的图形
    wedges, texts, autotexts = ax.pie(   ##用ax.pie()方法绘制饼图，该方法返回三个对象，wedges：包含饼图每个扇形的对象的matplotlib.patches.Wedge 的列表；texts：包含每个扇形对应标签文本的matplotlib.text.Text对象的列表；autotext：一个包含饼图中每个扇形对应百分比文本的 matplotlib.text.Text 对象的列表。
        data,   ##传入用于绘制饼图的数据
        labels=data.index,  ##使用data的索引作为每个扇形的标签
        autopct='%1.1f%%',  ##设置每个扇形上显示的百分比格式，这里显示保留一位小数
        startangle=90,      ##指定饼图起始角度是90度
        explode=explode,    ##传入之前创建的explode列表，用来设置扇形偏移量
        colors=PALETTE,     ##用之前定义的颜色调色板为扇形分配颜色
        wedgeprops={'edgecolor': 'black', 'linewidth': 0.8},  ##设置每个扇形属性，这里将边框颜色设置为黑色，边框线设置为0.8
        textprops={'fontproperties': font_prop}  # 设置字体，设置饼图中标签和百分比文本的字体属性
    )

    plt.setp(autotexts, color='white', weight='bold')  ##设置文本对象属性，这里将半分比文本颜色设置为白色，字体加粗
    ax.set_title(title, fontproperties=font_prop, pad=20)  ## 标题，fontproperties=font_prop 确保标题使用之前定义的字体属性，pad=20表示标题与饼图间垂直间距为20个点
    plt.savefig(filename, bbox_inches='tight')  ##将生成的饼图保存为指定文件
    plt.show()


def print_top10_ranking(data):
    """打印总量前十排名"""
    top10 = data[['部门', '总排放量']].sort_values('总排放量', ascending=False).head(10)   ##从data中选取“部门”和“总排放量”这两列数据；然后.sort_values('总排放量', ascending=False)对选取的“总排放量”这一列进行降序排序，ascending=False 表示降序，true则表示升序；.head(10)表示从排序后的结果中，选取前十行数据
    print("\n=== 总排放量前十排名 ===")
    print(top10.reset_index(drop=True).to_markdown(index=True)) ##top10.reset_index(drop=True）表示对top10这个DataFrame重置索引，drop=True表示丢弃原来的索引，重新生成从0开始的连续整数索引
    ##.to_markdown(index=True)：将重置索引后的 DataFrame 转换为 Markdown 表格格式的字符串。index=True 表示在表格中显示索引列。

def causality_analysis(df, energy_cols):  ##包含两个参数，一个df一个energy_cols
    """因果性分析（回归+显著性检验）"""
    from sklearn.preprocessing import StandardScaler ##从sklearn库的preprocessing模块导入standardscaler类，用于数据标准化

    # 数据标准化
    scaler = StandardScaler()  ##创建一个 StandardScaler 对象
    X_scaled = scaler.fit_transform(df[energy_cols])  ##对df中energy_cols所指定的列进行标准化处理，然后fit_transform方法会优先计算这些列的均值和标准差，然后将数据进行标准化
    y = df['总排放量']  ##将df中的“总排放量”列为因变量

    # 回归分析
    model = LinearRegression() ##创建一个线性回归模型对象
    model.fit(X_scaled, y)   ##使用标准化后的自变量X_scaled和因变量y对线性回归模型进行训练

    # 获取系数和p值
    coefficients = model.coef_  ##获得线性回归模型的系数，即每个自变量对因变量的影响程度
    p_values = []   ##初始化一个空列表，用于存储每个自变量的p值
    for i in range(X_scaled.shape[1]):  ##遍历X_scaled的每一列
        x_col = X_scaled[:, i]     ##取出当前列的数据
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_col, y)  ##使用 scipy.stats 模块的 linregress 函数进行简单线性回归，计算当前自变量与因变量之间的斜率、截距、相关系数、p 值和标准误差。
        p_values.append(p_value)  ##将计算得到的p值添加到p_values列表中

    # 构建结果表格
    result_df = pd.DataFrame({  ## 使用pd.DataFrame创建一个新的DataFrame，包含以下几列，来构建结果表格
        '能源类型': energy_cols,
        '标准化系数': coefficients,
        'p值': p_values,
        '显著性': ['***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else '不显著' for p in p_values]
    }).sort_values('标准化系数', key=abs, ascending=False)

    print("\n=== 因果性分析结果 ===")
    print(result_df.to_markdown(index=False)) ##index=False表示不显示索引列

    # 可视化重要影响因素
    plt.figure(figsize=(10, 6))  ##创建一个新的图形，设置图形大小为宽10英寸，高6英寸，原因同上
    significant_df = result_df[result_df['p值'] < 0.05].sort_values('标准化系数')  ##从结果表格筛选p值小于0.05额行，即显著影响因素，并进行排序
    ax = sns.barplot(x='标准化系数', y='能源类型', data=significant_df, palette="vlag")  ##使用seaborn库的barplot函数绘制条形图，x轴为标准化系数，y轴为能源类型，使用vlag调色板

    # ========= 新增字体配置 =========
    # 1. 标题字体
    ax.set_title('显著影响碳排放的能源类型（标准化系数）', fontproperties=font_prop, pad=20)

    # 2. X/Y轴标签字体
    ax.set_xlabel('标准化回归系数', fontproperties=font_prop)
    ax.set_ylabel('能源类型', fontproperties=font_prop)

    # 3. 刻度标签字体
    plt.setp(ax.get_xticklabels(), fontproperties=font_prop)
    plt.setp(ax.get_yticklabels(), fontproperties=font_prop)

    # 4. 其他文本（如网格线标签）
    plt.axvline(0, color='black', linestyle='--')

    plt.tight_layout()  ##调整子图参数，使图形更加紧凑
    plt.savefig('causality_analysis.png', bbox_inches='tight')  ##将图形保存在。。.png中，后面为图形只包含图形内容，不包含多余的空白区域
    plt.show()


def enhanced_heatmap(data, title, filename):
    """增强版热力图（支持中文）"""
    plt.figure(figsize=(12, 8))  ##同上
    ax = sns.heatmap(   ##sns.heatmap()是seaborn库的内置函数，具体的参数解释如下
        data.to_frame(),  ##将输入的data转换为dataframe格式
        annot=True,      ##在每个单元格中显示数据值
        cmap="coolwarm",  ##颜色映射
        center=0,         ##颜色映射的中心值为0，使正负值在颜色上有明显区分
        fmt=".2f",       ##显示的数据值的格式，保留两位小数
        linewidths=0.5,   ##设置热力图单元格间的分割线宽度为0.5
        annot_kws={
            'fontproperties': font_prop,  # 注释文本字体
            'size': 10,   ##字体大小为10
            'weight': 'bold'   ##字体加粗
        }
    )

    # ========= 关键字体设置 =========
    # 1. 标题字体
    ax.set_title(title, fontproperties=font_prop, pad=20)

    # 2. 坐标轴标签字体
    ax.set_xlabel(ax.get_xlabel(), fontproperties=font_prop)
    ax.set_ylabel(ax.get_ylabel(), fontproperties=font_prop)

    # 3. 刻度标签字体
    plt.setp(ax.get_xticklabels(),
             fontproperties=font_prop,   ##设置字体属性
             rotation=45,    ## 将刻度标签旋转45度
             ha='right')    ##对于y轴刻度标签，仅设置字体属性为font_prop
    plt.setp(ax.get_yticklabels(),
             fontproperties=font_prop)

    # 4. 色标字体（可选）
    cax = plt.gcf().axes[-1]
    cax.yaxis.label.set_fontproperties(font_prop)

    plt.tight_layout()   ##作用同上
    plt.savefig(filename, bbox_inches='tight')   ##指定名字保存文件
    plt.show()

# ======================
# 4. 修改后的主程序
# ======================
def main():
    # 数据加载
    df = pd.read_excel("2015年中国人类活动碳排放.xlsx", sheet_name="Sheet1")  ##读取excel文件，并把值存储在df中
    df = df[df['部门'] != '总消耗量'].reset_index(drop=True) ##从df中筛选出部门类不等于总消耗的行，使用reset_index重置索引，drop=True表示丢弃原来的索引，重新生成从0开始的连续整数索引

    # 分析1：排放量TOP10可视化
    top10 = df[['部门', '总排放量']].sort_values('总排放量', ascending=False).head(10)   ##从df中选取部门和总排放量两列数据，按照总排放量降序排序，选取前十行数据，存储在top10这个变量名中
    enhanced_barplot(top10, '总排放量', '部门',     ##调用之前定义的enhanced_barplot函数，绘制柱状图，并保存到emission_top10.png文件中
                     '2015年行业碳排放TOP10（单位：万吨）',
                     'emission_top10.png')

    # 新增：打印前十排名表格
    print_top10_ranking(df)

    # 分析2：能源结构
    energy_cols = df.columns[2:-1]   ##获取dy中（即之前基于的数据集excel）从第二列到倒数第一列的列名
    energy_totals = df[energy_cols].sum().sort_values(ascending=False)  ##对df中energy_cols所指定的列进行求和，得到每种能源的总消耗量，然后进行降序排序
    modern_pie(energy_totals, '主要能源消耗占比分析', 'energy_pie.png')  ##调用函数绘制饼图，设置标题并保存文件

    # 新增：因果性分析
    causality_analysis(df, energy_cols)

    # 原有相关性分析保持不变
    corr_series = df[energy_cols].corrwith(df['总排放量'])  ##计算df中energy_cols所指定的列与总排放量间列间的相关性，结果存在corr_series
    enhanced_heatmap(corr_series.sort_values(ascending=False),  ##调用之前定义的方法，降序处理，然后保存在文件中
                     '能源类型与碳排放相关性',
                     'correlation_heatmap.png')


if __name__ == "__main__":
    main()