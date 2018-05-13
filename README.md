# semantix
################################################################################
Teste engenheiro de dados - Semantix
Carlos Tafinel
13/05/2018

################################################################################
Questões descritivas:
################################################################################

1 - Qual o objetivo do comando cache em Spark?
 => Com o cache você poderá persistir seu RDD com todas as transformações 
    realizadas até o momento, desta maneira você pode acessar as informações 
    a partir de um status específico sem realizar todas as transformações desde 
    o princípio.

2 - O mesmo código implementado em Spark é normalmente mais rápido que a 
    implementação equivalente em MapReduce. Por quê?
 => O código implementado em Spark tende a ser mais rápido em situações onde 
    existe muito acesso aos dados pois trabalha os mesmos em memória evitando 
    operações de IO excessivas.

3 - Qual é a função do SparkContext?
 => Conectar sua aplicação ao cluster onde você irá executar passando 
    informações sobre a mesma

4 - Explique com suas palavras o que é Resilient Distributed Datasets (RDD).
 => RDD é um conjunto de operações que podem ser aplicadas sobre uma coleção de 
    dados distribuidos gerando novos datasets. 
    Talvez o aspecto mais interessante que o RDD traz é que ele não representa 
    somente os dados mas sim as operações que precisam ser aplicadas, isso 
    possibilita que você prepare N "transformations" que somente serão 
    executadas quando uma "action" solicita uma verificação dos dados como em 
    um collect para exibir os mesmos trafegando apenas o resultado do dados 
    trabalhados até aquele ponto.

5 - GroupByKey é menos eficiente que reduceByKey em grandes dataset. Por quê?
 => Apesar de ambos resultarem em outputs similares a utilização do reduceByKey 
    vai diminuir o gargalo de rede pois ele pré-agrupa os dados dentro da 
    partição antes de enviar as tuplas para as partições onde a lambda será 
    finalmente executada. Em grandes datasets como o groupByKey irá trafegar 
    todas as tuplas antes da lambda do reduce ser executada você vai gastar 
    tempo desnecessário no shuffle.

6 - Explique o que o código Scala abaixo faz
    val textFile = sc . textFile ( "hdfs://..." )
    val counts = textFile . flatMap ( line => line . split ( " " ))
    . map ( word => ( word , 1 ))
    . reduceByKey ( _ + _ )
    counts . saveAsTextFile ( "hdfs://..." )
 => Este é o exemplo cássico do wordcount realizado com Spark, abaixo tento 
    detalhar o passo a passo para esta execução:
    a. Prepara a carga o conteúdo do arquivo indicado no path "hdfs://..." para 
       o RDD textFile
    b. Prepara a execução de tranformação no conteúdo a ser carregado separando 
       este em conjunto elementos a cada espaço em branco
    c. A essa lista de dados separados por espaços em branco é preparada a 
       atribuição de um valor numérico 1 gerando uma tupla onde a chave será 
       cada um dos elementos separados pelo comando anterior
    d. Prepara a operação de soma dos valores(1) de cada um dos elementos de uma 
       chave com o valor já computado para a mesma chave, em resumo soma todos 
       os números 1 de cada chave
    => As operações b, c e d são armazenadas no RDD de nome counts
    e. Neste ponto todas as operações registradas no RDD counts serão executadas 
       e os elementos do dataset resultante serão gravados no path do hdfs. 

################################################################################
Questões práticas:
################################################################################

OBS: O formato original dos arquivos era texto compactado como gzip
     desta maneira o spark seria forcado a processar todas as informacoes em
     apenas uma particao o que pode gerar atrasos em situacoes reais de 
     processamento de grandes arquivos sub-utilizando as funcionalidades de
     paralelismo
     Neste exercício, mesmo que desnecessário pelo ambiente utilizado, 
     foi criado o script decompress.sh para descompactar os 
     arquivos para posterior processamento. Ao final da rotina o arquivo 
     descompactado e apagado

- As rotinas que informam os resultados das 5 questões práticas são executadas 
  através do shell nasa.sh com os seguintes parametros:

$ sh nasa.sh NASA

- Após o pré processamento com o shell decompress.sh os scripts são realizados 
  com o programa nasa.py (Python 3.6.0)
- São utilizados neste script apenas as bibliotecas básicas do pySpark e de 
  sistema para tratamento de data e argumentos
- Guardei os resultados de uma execução no arquivo result.txt

################################################################################