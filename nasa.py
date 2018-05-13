# ==============================================================================
# Teste - Semantix - 13/May/2018 -  Carlos Tafinel
# HTTP requests to the NASA Kennedy Space Center WWW server
#
# ==============================================================================

from sys import argv, exit
from pyspark import SparkContext, SparkConf
import datetime

def print_(detail, *type_):
    if (type_ == "E"):
        type_ = "ERROR"
    else:
        type_ = "INFO"
    
    msg = ("[" + type_ + "]"+
           "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") +  "] "+
           detail)
    print(msg)

#Main
#Define arguments
if (len(argv[0:]) < 2):
    print_(("Informar nome do arquivo"), 
           "E")
    exit(1)
else:
    source_file = "files/d/"+argv[1]
    print_("------------------------------------------------------------------")
    print_("HTTP requests to the NASA Kennedy Space Center WWW server")
    print_("------------------------------------------------------------------")
    print_("Arquivo a processar: "+ source_file)
    print_("------------------------------------------------------------------")

#Declare Spark objects
conf = SparkConf().setAppName('nasa_semantix')
sc = SparkContext(conf=conf)

# source_file = "files/d/NASA"     
rdd = sc.textFile(source_file)

#1 Número de hosts únicos.
unique = rdd.map(lambda x: (x.split(' - - ')[0])).distinct().count()

#2 O total de erros 404.
rdd_404 = rdd.filter(lambda x: x[-5:] == '404 -')
sum_of_404 = rdd_404.count()

#3 Os 5 URLs que mais causaram erro 404.
top_404 = rdd.filter(lambda x: x[-5:] == '404 -')\
    .map(lambda x: ((x.split(' - - ')[0]), 1))\
    .reduceByKey(lambda a, b: a + b)\
    .takeOrdered(5, lambda x: -x[1])

#4 Quantidade de erros 404 por dia.
daily_404 = rdd.filter(lambda x: x[-5:] == '404 -')\
    .map(lambda x: (x[x.find("[")+1:][:11], 1))\
    .reduceByKey(lambda a, b: a + b)

#5 O total de bytes retornados.
bytes_total = rdd.map(lambda x: x.split(" ")[-1])\
    .map(lambda x: int(x) if(x.isdigit()) else 0).sum()

#Results
print_("#1 Número de hosts únicos: "+str(unique))
print_("#2 O total de erros 404: "+str(sum_of_404))
print_("#3 Os 5 URLs que mais causaram erro 404: "+str(top_404))
print_("#4 Quantidade de erros 404 por dia:  "+
    '[%s]' % ', '.join(map(str, daily_404.collect())))
print_("#5 O total de bytes retornados: "+str(bytes_total))

print_("Rotina finalizada com sucesso!")