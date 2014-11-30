import csv;
import numpy as np;
import datetime;
import matplotlib.pyplot as plt;
#open the datafile and plotting tools
header=[];
#number of collumns containing non-data -1
metacols = 3;
colr_scheme=['#00B2A5','#D9661F','#00B0DA','#FDB515', '#ED4E33','#2D637F','#9DAD33','#53626F','#EE1F60','#6C3302','#C2B9A7','#CFDD45','#003262'];
colr_map={ 'k40':6, 'bi214':3, 'tl208':5, 'cs137':8, 'cs134':7 };
colr_scheme=[ colr_scheme[colr_map[key]] for key in colr_map ];
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
        u_sample_dates='';
        for name in sample_names:
            if(u_name == name):
                lst.append(sample_array[row,:]);
                if(sample_dates[row]==''):
                    continue;
                u_sample_dates+='\n'+sample_dates[row].strftime('%m-%d-%y');
            row+=1;
        lst=np.asarray(lst);
        u_sample_array.append(np.max(lst,axis=0));
        u_sample_names_ret.append(u_name+u_sample_dates);

    return np.asarray(u_sample_array),u_sample_names_ret;        
def unique_sample_names(sample_names):
    ret=[];
    for name in sample_names:
        if(not name in ret):
            ret.append(name);
    return ret;
def create_barerror_plot(csv_file,title):
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
    print data.shape, error.shape;
    ax,fig=generate_barerror_logy(sample_names=name_lst,data=data,error=error,legend_key=legend_key,title=title,log=True);

def generate_barerror_logy(sample_names,data,error,legend_key,title,log=True):
    num_samples=len(sample_names);
    
    ind = np.arange(0.5,num_samples);
    width=0.15;

    fig,ax=plt.subplots();
    
    axs=[];
    mins=np.amin(data[np.nonzero(data)]);
    for samp in range(0,len(legend_key)):
        if( np.amin(data[:,samp])==0):
            args=np.where(data[:,samp]==0);
            data[args,samp]+=mins;    
        axs.append(ax.bar(left=ind+width*samp,height=tuple(data[:,samp]),width=width,color=colr_scheme[samp],yerr=tuple(error[:,samp]),ecolor=colr_scheme[samp],edgecolor="none",log=True));
    
    ylims=ax.get_ylim();
    ax.set_ylim([mins,ylims[1]]);
    ax.set_xticks( ind+float(len(legend_key))/2.*width );
    ax.set_xticklabels( sample_names );
    ax.tick_params(axis='x',color='w');
    ax.legend( [ a[0] for a in axs ], legend_key,loc='upper left');
    ax.set_title(title);
    ax.set_ylabel(legend_key[0].split(' ')[1]);
    plt.gcf().subplots_adjust(bottom=0.15,left=0.05,right=0.95);
    plt.show();
    return ax,fig;


create_barerror_plot('NonFukushima.csv',title='Bay Area Environmental Sample Summary');
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
