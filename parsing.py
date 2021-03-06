#commment,file change
import csv;
import numpy as np;
import datetime;
import matplotlib.pyplot as plt;
#open the datafile and plotting tools
header=[];
#number of collumns containing non-data -1
metacols = 4;
colr_scheme=['#00B2A5','#D9661F','#00B0DA','#FDB515', '#ED4E33','#2D637F','#9DAD33','#53626F','#EE1F60','#6C3302','#C2B9A7','#CFDD45','#003262'];
colr_map={ 'k40':8, 'bi214':5, 'tl208':7, 'cs137':10, 'cs134':9 };
iso_key=['k40','bi214','tl208','cs137','cs134'];
colr_scheme=np.asarray([ colr_scheme[colr_map[key]] for key in iso_key ]);

def parse_time(date):
    if( '-' in date):
        return '';
    lst=date.split('/');
    ret_lst=[];
    for itm in lst:
        ret_lst.append( int(itm) );
    return datetime.datetime(year=2000+ret_lst[2], month=ret_lst[0], day=ret_lst[1]);
    
def combine_measurements_with_same_name(sample_array,sample_names,sample_dates):
    u_sample_names=unique_sample_names(sample_names);
    u_sample_array=[];
    u_sample_names_ret=[];
    for u_name in u_sample_names:
        lst=[];
        row=0;
        u_sample_dates=[];
        for name in sample_names:
            if(u_name == name):
                lst.append(sample_array[row,:]);
                if(sample_dates[row]==''):
                    continue;
                u_sample_dates.append(sample_dates[row]);
            row+=1;

        u_sample_dates=np.sort(u_sample_dates);
        if( len(u_sample_dates) ):
            u_sample_dates_= '('+str(len(u_sample_dates))+')';
        else:
            u_sample_dates_= '('+str(1)+')';

        for date in u_sample_dates[-3:]:
            u_sample_dates_+="\n"+date.strftime('%m-%d-%y');
        lst=np.asarray(lst);
        u_sample_array.append(np.max(lst,axis=0));
        u_sample_names_ret.append(u_name+u_sample_dates_);

    return np.asarray(u_sample_array),u_sample_names_ret;        
def unique_sample_names(sample_names):
    ret=[];
    for name in sample_names:
        if(not name in ret):
            ret.append(name);
    return ret;
def create_barerror_plot(csv_file,title,log=True):
    lst=[];
    name_lst=[];
    date_lst=[];
    header=[];
    with open(csv_file,'rU') as csvfile:
        #read the first line
        parser=csv.reader(csvfile);
        header=parser.next();
        #use the first line to create a dictionary to get values easily
        dictparser=csv.DictReader(csvfile,header);
        for row in dictparser:
            tmp_list=[];
            name_lst.append(row[header[0]]);
            date_lst.append(parse_time(row[header[1]]));
            for ind in range(metacols,len(row)):
                if('N.D.' in row[header[ind]]):
                    tmp_list.append(0);
                    continue;
                tmp_list.append(float(row[header[ind]]));
            lst.append(tmp_list);
            
    #change in the datatype for conv.
    lst=np.asarray(lst);

    #just reduce the data for plotting purposes
    lst,name_lst=combine_measurements_with_same_name(sample_array=lst,sample_names=name_lst,sample_dates=date_lst);
    data =np.zeros((len(name_lst),lst.shape[1]/2.));
    error=np.zeros((len(name_lst),lst.shape[1]/2.));
    legend_key=[];
    loop=0;
    #separate the build legend key,data,errors
    for itm in range(0,lst.shape[1],2):
        legend_key.append(header[metacols+itm]);
        data[:,loop]=lst[:,itm];
        error[:,loop]=lst[:,itm+1];
        loop+=1;
    print legend_key;
    ax,fig=generate_barerror_logy(sample_names=name_lst,data=data,error=error,legend_key=legend_key,title=title,log=log);

def generate_barerror_logy(sample_names,data,error,legend_key,title,log=True):
    num_samples=len(sample_names);
    
    ind = np.arange(0.5,num_samples,dtype=np.float64);
    width=float(0.15);

    fig,ax=plt.subplots();
    
    axs=[];
    mins=np.amin(data[np.nonzero(data)]);
    for samp in range(0,len(legend_key)):
        args=np.zeros((0));
        left_edge=ind+float(width)*float(samp);
        if( np.amin(data[:,samp])==0):
            args=np.where(data[:,samp]==0);
            data[args,samp]+=1e-9;
            draw_arrows(axes=ax,xlocs=(left_edge+0.5*float(width))[args],ylocs=error[args,samp],colr=colr_scheme[samp]);
        axs.append(ax.bar(left=left_edge,height=tuple(data[:,samp]),width=width,color=colr_scheme[samp],yerr=tuple(error[:,samp]),ecolor=colr_scheme[samp],edgecolor="none",log=log));
    
    ylims=ax.get_ylim();
    upper_mult=1;
    if(log):
        upper_mult=10;
    ax.set_ylim([mins/10,upper_mult*ylims[1]]);
    ax.set_xticks( ind+float(len(legend_key))/2.*width );
    ax.set_xticklabels( sample_names );
    ax.tick_params(axis='x',color='w');
    ax.legend( [ a[0] for a in axs ], legend_key,loc='upper left');
    ax.annotate('', xy=(0.88,0.8999), xycoords='axes fraction', xytext=(0.88,0.9),textcoords='axes fraction',arrowprops=dict(edgecolor='k',facecolor='k',arrowstyle='-|>') );
    ax.annotate('Limit of Detection',xy=(0.888,0.905),xytext=(0.888,0.905),textcoords='axes fraction',ha='left',va='center');
    ax.set_title(title);
    ax.set_ylabel('Specific Activity '+legend_key[0].split(' ')[1]);
    plt.gcf().subplots_adjust(bottom=0.15,left=0.05,right=0.95);
    plt.show();
    return ax,fig;

def draw_arrows(axes,xlocs,ylocs,colr):
    num_els=len(xlocs);
    if(num_els==0):
        return;
    if( len(ylocs.shape)>1 ):
        ylocs=np.squeeze(ylocs,axis=(0,));
    for ind in range(0,num_els):
        #dy=10**np.ceil(np.log10(ylocs[ind]));
        dy=1e-10;
        axes.annotate("",xy=(xlocs[ind], ylocs[ind]-dy), xycoords='data',xytext=(xlocs[ind], ylocs[ind]), textcoords='data',arrowprops=dict(edgecolor=colr,facecolor=colr,arrowstyle="-|>") );
        # has problems rendering with log scale. divergent
        #axes.arrow(xlocs[ind],ylocs[ind],0,-dy,head_starts_at_zero=False,fc='k',width=5e-3);
    return;

create_barerror_plot('NonFukushima.csv',title='Reference Sample Summary',log=True);
create_barerror_plot('Fukushima.csv',title='Bay Area Environmental Sample Summary',log=True);
with open('NonFukushima.csv','rU') as csvfile:
     #read the first line
     parser=csv.reader(csvfile);
     header=parser.next();
     #use the first line to create a dictionary to get values easily
     dictparser=csv.DictReader(csvfile,header);
     val_pre="var dataSet = [\n";
     val="";
     for row in dictparser:
          val+="['"
          for key in header:
               val+=row[key]+"','";
          val=val[:-2]+"],\n"
     val=val[:-2]+"\n];";
     val=val_pre+val;
val+="\n";

with open('jquery.header') as header_file:
     line=header_file.next();
     val+=line;
     while(not "\"columns\": [" in line):
          line=header_file.next();
          val+=line;
     for el in header:
          val+="{\"title\": \""+el+"\"},\n"
     val=val[:-1];
     for line in header_file:
          val+=line;
#print val;
     
with open('Data.js','w') as data:
     data.write(val_pre+val)
