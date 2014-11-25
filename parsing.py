import csv;
import numpy as np;
import datetime;
import matplotlib.pyplot as plt;
#open the datafile and plotting tools
header=[];

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
            for ind in range(2,len(row)):
                tmp_list.append(float(row[header[ind]]));
            lst.append(tmp_list);
            
    #change in the datatype for conv.
    lst=np.asarray(lst);
    for itm in range(0,len(name_lst)):
        name_lst[itm]=name_lst[itm]+"\n"+str(date_lst[itm]);
    print name_lst;


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
print val;
     
with open('Data.js','w') as data:
     data.write(val_pre+val)
