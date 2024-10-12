from sklearn.impute import SimpleImputer
import numpy as np
import pandas as pd
import math
import plotly.express as px

dataset = pd.read_csv('synthetic_water_quality_data_bengaluru.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values
# print(X)
# print(y)
num_rows = len(X)
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer.fit(X[:, 3:-1])
X[:, 3:-1] = imputer.transform(X[:, 3:-1])


o2 = np.arange(0,8)
pH = np.arange(6,9)
conductivity = np.arange(200,2500)
bod = np.arange(5,40)
f_level = np.arange(0,2)
b_level = np.arange(0,5)
ca_level = np.arange(0,5)
phosphate_level = np.arange(0,2)
na_level = np.arange(20,150)
nh3_level = np.arange(0,1)
carb_level = np.arange(0,1)
bicarb_level = np.arange(0,8)
cod = np.arange(0,160)
turbidity = np.arange(20,60)
testers = [o2,pH,conductivity,bod,f_level,b_level,ca_level,phosphate_level,na_level,nh3_level,carb_level,bicarb_level,cod,turbidity]
def seperator(x) : 
    for i in range(num_rows) : 
        for j in range(14) :
            if int(x[i][j]) in testers[j] : 
                x[i][j] = -1
    df = pd.DataFrame(x)
    df.to_csv('seperated.csv')
    return x
req_X = X[:,3:-1]
seperated_x = seperator(req_X)

def find_max(x) :
    A = [max(x[:,i]) for i in range(14)]
    return A

def find_min(x) :
    A = []
    for i in range(14) : 
        curr_min = math.inf
        for j in x[:,i] : 
            if j != -1 :
                if curr_min >= j :
                    curr_min = j
        if curr_min == math.inf : 
            curr_min = -1
        A.append(curr_min)
    return A
max_x = find_max(seperated_x)
min_x = find_min(seperated_x)
# print(max_x)
# print(min_x)
# quit()
def normalizer(x) : 
    for i in range(num_rows) : 
        for j in range(14) : 
            if x[i][j] == -1 :
                pass
            else : 
                if max_x[j] == min_x[j] : 
                    x[i][j] = 0.1
                else : 
                    x[i][j] = (max_x[j] - x[i][j])/(max_x[j]-min_x[j])
    df = pd.DataFrame(x)
    df.to_csv("normalized.csv")
    
    return x
def normalize_use(x) : 
    max1 = max(x)
    min1 = min(x)
    for i in range(num_rows):
        x[i] = (x[i]-min1)/(max1-min1)
    return x

useful = normalize_use(X[:,-1])
                     
normal_x = normalizer(seperated_x)
# testers = [o2,pH,conductivity,bod,f_level,b_level,ca_level,phosphate_level,na_level,nh3_level,carb_level,bicarb_level,cod,turbidity]
def worst_index(x) : 
    for i in range(num_rows) : 
        if x[i][1] == -1 :
            pass
        else : 
            x[i][1] = 1-x[i][1]
        
        if x[i][2] == -1 :
            pass
        else : 
            x[i][2] = 1-x[i][2]
    worst_measure = []
    for i in range(num_rows) : 
        curr_sum = 0
        
        for j in x[i,:] :   
            # if i == 1064 :
            #     print(x[i,:])
            #     print(j) 
            #     if j==-1 :
            #         pass
            #     else :   
            #         curr_sum+=j
            #     print(curr_sum)
            if j==-1 :
                pass
            else : 
                curr_sum+=j
        worst_measure.append(curr_sum)
        # worst_measure.append(sum(x[i,:]))
    # print(worst_measure)
    # print(min(worst_measure))
    # print(worst_measure.index(min(worst_measure)))
    return worst_measure
lake_index = worst_index(normal_x)

L = [i for i in enumerate(lake_index)]
  
L = sorted(L, key=lambda x: x[1],reverse=True)

def output_worst_to_best(x) : 
    info = X[:,:3]
    out = []
    for i in x :
        print_out =np.append(info[i[0]],i[1])
        out.append(print_out)
    df = pd.DataFrame(out)
    df.to_csv("sorted.csv")
    return out

new_L = output_worst_to_best(L)
def plot_graph(height, xdomain,names, dimensions=(960,540)) :
    measure = []
    for i in range(len(height)-1):
        measure.append(height[i]*xdomain[i])
    # print(measure)
    # print(max(measure))
    # print(min(measure))
    df = pd.DataFrame(list(zip(xdomain,height,names,measure)))
    df.columns=['Useful','Fatal-rate','names','measure']

    fig = px.scatter(
        df, x="Useful", y="Fatal-rate", 
        color="measure", color_continuous_scale="jet",range_color=[min(measure),max(measure)],title="Lake Fatality index",hover_name="names")
    fig.update_xaxes(range=[0, 1])
    fig.update_yaxes(range=[0, 5])
#     fig.update_layout(
#     coloraxis={
#         'colorbar': {
#             'len': 1,  
#             'y': 0.5,     
#             'x': 1.05,    
#         }
#     }
# )
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)","paper_bgcolor": "rgba(15, 17, 20, 1)",})
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(
    font_family="Roboto",
    font_color="white",
    title_font_family="Times New Roman",
    title_font_color="white",
    # legend_title_font_color="green"
)
    fig.show()
    return fig
heigh = []
for i in L : 
    heigh.append(i[1])
L2 = []
for i in new_L : 
    L2.append(i[2])
fig = plot_graph(heigh,useful,L2)
fig.write_image(f"C:\\Users\\Naveen\\Desktop\\Speech Competition\\main-code\\images\\graph.png",scale=2,format="png")