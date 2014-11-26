import csv;
import numpy as np;
import datetime;
import matplotlib.pyplot as plt;
#open the datafile and plotting tools
header=[];
#number of collumns containing non-data -1
metacols = 3;

def parse_time(date):
    if( '-' in date):
        return '';
    lst=date.split('/');
    ret_lst=[];
    for itm in lst:
        ret_lst.append( int(itm) );
    return datetime.datetime(year=2000+ret_lst[2], month=ret_lst[0], day=ret_lst[1]);
    
def create_barerror_plot(csv_file):
    lst=[];
    name_lst=[];
    date_lst=[];
    header=[];
    with open('NonFukushima.csv','rU') as csvfile:
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
                tmp_list.append(float(row[header[ind]]));
            lst.append(tmp_list);
            
    #change in the datatype for conv.
    lst=np.asarray(lst);
    
    #making labels for the chart
    for itm in range(0,len(name_lst)):
        name_lst[itm]=name_lst[itm]+"\n"+str(date_lst[itm]);
    data =np.zeros((len(name_lst),lst.shape[1]+2-metacols));
    error=np.zeros((len(name_lst),lst.shape[1]+2-metacols));
    legend_key=[];
    for itm in range(0,lst.shape[1],2):
        legend_key.append(header[metacols+itm]);
        data[:,itm]=lst[:,itm];
        error[:,itm]=lst[:,itm+1];
    print legend_key;
    ax,fig=generate_barerror_logy(sample_names=name_lst,data=data,error=error,legend_key=legend_key,log=True);

def generate_barerror_logy(sample_names,data,error,legend_key,log=True):
    num_samples=len(sample_names);
    
    ind = np.arange(num_samples);
    width=0.35;

    fig,ax=plt.subplots();
    
    axs=[];
    for samp in range(0,len(sample_names)):
        axs.append(left=ax.bar(ind+width*samp,height=data[ind,:],width=width,color='r',yerr=error[ind,:],log=True));

    ax.set_xticks( ind+width );
    ax.set_xticklabels( sample_names );
    ax.legend( [axs[:][0]], sample_names);
    plt.show();
    return ax,fig;

create_barerror_plot('NonFukushima.csv');
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
