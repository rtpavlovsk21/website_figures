import csv;
#open the datafile
header=[];
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
