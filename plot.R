library(argparser, quietly=TRUE)
library(dplyr, quietly=TRUE)
library(tidyr, quietly=TRUE)
library(ggplot2, quietly=TRUE)
library(ggsci, quietly=TRUE)
#library(gcamdata, quietly=TRUE)
library(MetBrewer, quietly = TRUE)
library(plyr, quietly = TRUE)
library(rgcam)
library(stringr)
library(data.table)
library(xlsx)

path_base='/Users/haozheyang/Documents/GCAM/gcam-v6.0-Mac-Release-Package/'

prj <- loadProject(paste0(path_base,'CO2_sectoral/temp_CO2_sectoral_regroup.dat') )# load database

## Five query results used in the re-group process
energy_consumption <- getQuery(prj, 'Energy consumption by technology')  # query name
input_subsector <- getQuery(prj, 'inputs by subsector')  # query name
service_output_tech <- getQuery(prj, 'Service output by technology')  # query name
output_subsector <- getQuery(prj, 'outputs by subsector')  # query name
CO2_emission <- getQuery(prj, 'CO2 emissions by sector (excluding resource production)')  # query name

energy_consumption=data.table(energy_consumption)
energy_consumption_national=energy_consumption[,.(fuel=sum(value)),by=c('scenario','year','input','Units')]

input_subsector=data.table(input_subsector)
input_subsector_national=input_subsector[,.(input=sum(value)),by=c('scenario','year','input','Units')]

output_subsector=data.table(output_subsector)
output_subsector_national=output_subsector[output_subsector$year>2015,.(output=sum(value)),by=c('scenario','year','subsector...5','Units')]

service_output_tech = data.table(service_output_tech)
service_national=service_output_tech[(service_output_tech$year>2015) & (service_output_tech$sector=='trn_pass_road_LDV_4W'),.(service=sum(value)),by=c('scenario','year','technology','Units')]

CO2_USA=read.csv(paste0(path_base,"CO2_sectoral/CO2_sector_trade_USA.csv"))%>%setDT()
CO2_China=read.csv(paste0(path_base,"CO2_sectoral/CO2_sector_trade_China.csv"))%>%setDT()
CO2_base=read.csv(paste0(path_base,"CO2_sectoral/CO2_sector_base.csv"))%>%setDT()

CO2_USA_national=CO2_USA[CO2_USA$region!="USA" & CO2_USA$Year>2015,.(CO2=sum(co2.emiss)),by=list(sector,scenario,Year)]
CO2_China_national=CO2_China[CO2_China$region!="USA" & CO2_China$Year>2015,.(CO2=sum(co2.emiss)),by=.(sector,scenario,Year)]
CO2_base_national=CO2_base[CO2_base$region!="USA" & CO2_base$Year>2015,.(CO2=sum(co2.emiss)),by=.(sector,scenario,Year)]

sector_code=CO2_USA_national[CO2_USA_national$Year==2050,.(sector)]
sector_code[,old_id:=list(c(1:32))]

CO2_national= rbind(CO2_USA_national,CO2_China_national,CO2_base_national)
CO2_national= merge(CO2_national,sector_code)


sector=read.xlsx('sector_aggregate.xlsx',1,header=TRUE)%>%setDT()
CO2_national=sector[CO2_national,on = .(old_id)]
CO2_scenario=CO2_national[,.(CO2_emission=sum(CO2)),by=c('scenario','Year','new_sector')]

ggplot(data=CO2_scenario, aes(x=scenario, y=CO2_emission,fill=new_sector))+
  geom_bar(stat="identity")+
  facet_grid(~Year)+
  scale_x_discrete(labels=c("trade_China" = "Import", "trade_USA" = "Domestic"))+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  guides(fill=guide_legend(title="Sector"))+
  ylab("Carbon emissions (Million tonne)")


ggplot(data=output_subsector_national, aes(x=scenario,y=output, fill=subsector...5))+
  geom_bar(stat="identity")+
  facet_grid(~year)+
  scale_x_discrete(labels=c("trade_China" = "Import", "trade_USA" = "Domestic"))+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  guides(fill=guide_legend(title="Energy source"))+
  ylab("energy output (EJ)")

ggplot(data=service_national, aes(x=scenario,y=service, fill=technology))+
  geom_bar(stat="identity")+
  facet_grid(~year)+
  scale_x_discrete(labels=c("trade_China" = "Import", "trade_USA" = "Domestic"))+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  guides(fill=guide_legend(title="Energy source"))+
  ylab("million pass-km")

       

