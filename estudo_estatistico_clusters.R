library(EMCluster)
library(RWeka)


# carregamento  dados
path_history_data <- "E:/TickDataDownloader/tickdata/____COMPLETE_DATA_____/"
setwd("E:/Desenvolvimento/analise_dados_ob")
NROM_TO_ANALISES = 10000

# 
# function readdata
# 
# LER OS DADOS DO PRECO EM UM DETERMINADO MES OU ANO DE UM DETERMINADO PAR
#
# if month==0 entao retorna o ano inteiro
# output format: datetime, O, H, L, C
readData <- function(asset, year, timeframe = "M1", prefix="PRICE", nrow=500){
  dataframe <- read.csv(paste(getwd(), "/datasets/csv/", year,"/",prefix, "-",  asset, "_",timeframe,".csv", sep=""), header= T, nrows = nrow) # experimental_data
  return(dataframe)
}  
readPriceData <- function(asset, year, timeframe = "M1", prefix="PRICE", nrow=500){
  data <- readData(asset, year, timeframe, nrow=nrow)
  # rename colums
  names(data)[1] <- "DATETIME"
  names(data)[2] <- "O"
  names(data)[3] <- "H"
  names(data)[4] <- "L"
  names(data)[5] <- "C"
  names(data)[6] <- "V"
  day = c()
  hour = c()
  min = c()
  for (index in seq(from=1, to=dim(data)[1] )) {
    datestr = strsplit(as.character(data$DATETIME[index])," ", fixed = T)[[1]][1]
    timestr = strsplit(as.character(data$DATETIME[index])," ", fixed = T)[[1]][2]
    day[index] = as.numeric(strsplit(datestr, ".", fixed = T)[[1]][3])
    hour[index] = as.numeric(strsplit(timestr, ":", fixed = T)[[1]][1])
    min[index] = as.numeric(strsplit(timestr, ":", fixed = T)[[1]][2])
    #hour[index] = data$T[index]
  }
  data["D"]= day
  data["TH"]= hour
  data["TM"]= min
  return(data)
}

# function result_BO
# adiciona a um dataset que veio do readdata as seguintes  colunas:
#  * winPUT{tf} (eg: winPUT_5M) 
#  * e a coluna winCALL_{tf}

result_BO <- function(dataset, tf_bars=5, all = T){
  typeWIN_xM = c()
  WINcall_xM = c()
  
  for (index in seq(from=1, to=dim(dataset)[1]-tf_bars)) { 
    
      #typeWIN_xM[index] <- dataset$C[index+tf_bars] > dataset$O[index+1]
      if (dataset$C[index+tf_bars] > dataset$O[index+1]){
        typeWIN_xM[index] <- as.character("WINCALL")
        WINcall_xM[index] <- 1
      } else if (dataset$C[index+tf_bars] < dataset$O[index+1]) {
        typeWIN_xM[index] <- as.character("WINPUT")
        WINcall_xM[index] <- 0
      } else {
        typeWIN_xM[index] <- as.character("TIE")
        WINcall_xM[index] <- 0
        
      }
  }
      
    
  # add missing rows
  for (index in seq(from=dim(dataset)[1]-tf_bars+1, to=dim(dataset)[1])) { 
    typeWIN_xM[index] <- "TIE"
    WINcall_xM[index] <- 0

  }
  nm_callcol <- paste("TYPEWIN_", tf_bars, "M", sep="" )
  nm_Wcallcol <- paste("WINCALL_", tf_bars, "M", sep="" )
  dataset[nm_callcol] <- typeWIN_xM
  dataset[nm_Wcallcol] <- WINcall_xM
  if (all==F){
    return(dataset[, c(nm_callcol, "V", "D")])
  } else {
    return(dataset)
  }
}

pin_detect <- function(dataset) {
  
}

clear_dataset <- function(dataset){
  return(dataset[!(names(dataset) %in% c("DATETIME", "T", "O", "C", "H", "L", "V") )])
}




export_to_wekafile <- function(dataset){
  w <- read.arff(system.file("arff","weather.arff",
                             package = "RWeka"))
  ## Normalize (response irrelevant)
  m1 <- Normalize(~., data = w)
  m1
  ## Discretize
  m2 <- Discretize(play ~., data = w)
  m2
  
}

cluster_test <- function(dataset, k = 10) {
  km <- init.EM(dataset, nclass = k, method = "em.EM")
  return(km) 
  #table(km$cluster, dataset$Species)
}



AUDUSD <- readPriceData("AUDUSD",year=2005, nrow=NROM_TO_ANALISES)
AUDUSD_BO <- result_BO(AUDUSD, all = T)
AUDUSD_BO <- result_BO(AUDUSD_BO, 15, all = T)
AUDUSD_BO <- merge(readData("AUDUSD", year = 2005, nrow = NROM_TO_ANALISES, prefix = "MA"), AUDUSD_BO)
AUDUSD_BO <- merge(readData("AUDUSD", year = 2005, nrow = NROM_TO_ANALISES, prefix = "INFOCANDLE"), AUDUSD_BO)
AUDUSD_BO <- clear_dataset(AUDUSD_BO)
write.arff(AUDUSD_BO, "datasets/weka/AUDUSD.arff")


library (rpart) 
library(rpart.plot) 

attach(AUDUSD_BO)
# Gerar o modelo

rm(WINCALL_5M)
WINCALL_15M[WINCALL_5M==0] <- "CALL {LOSS}" 
WINCALL_15M[WINCALL_5M==1] <- "CALL {WIN}"

model.rpart <- rpart (WINCALL_15M ~  MTREND_20 + MTREND_130 + COLORC ) 

# Visualizar o modelo
rpart.plot (model.rpart, type=0, extra=2, varlen=10) 


#returnem<-cluster_test(AUDUSD_BO, 6)
#print(returnem)
