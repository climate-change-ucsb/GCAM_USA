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
library(readxl)
library(ggpattern)

path_base='/Users/hy4174/Documents/gcam-v6.0/output/'
path_CO2='/Users/hy4174/Documents/gcam-v6.0/'

prj <- loadProject(paste0(path_base,'sectoral_CO2_emission_regroup/temp_CO2_sectoral_regroup_trade.dat') )# load database

## Five query results used in the re-group process
CO2_price <- getQuery(prj, 'CO2 prices')  # query name
energy_consumption <- getQuery(prj, 'Energy consumption by technology')  # query name
input_subsector <- getQuery(prj, 'inputs by subsector')  # query name
service_output_tech <- getQuery(prj, 'Service output by technology')  # query name
output_subsector <- getQuery(prj, 'outputs by subsector')  # query name
CO2_emission <- getQuery(prj, 'CO2 emissions by sector (excluding resource production)')  # query name
market_price <- getQuery(prj, "prices of all markets")
market_supply <- getQuery(prj, "supply of all markets")
cost_tech <- getQuery(prj, "Cost by technology")

transportation <- getQuery(prj, "transport service output by tech (new)")
transportation = data.table(transportation)
transportation = transportation [transportation$region == "AK" & transportation$scenario == "only_stick_80p",]

CO2_price = data.table(CO2_price)
CO2_price = CO2_price[CO2_price$market == "USACO2" & CO2_price$year>2030 & CO2_price$year<2055,]
CO2_price = CO2_price[CO2_price$scenario %in% c('only_stick_80p','baseline_80p','free_80p_l' , 'onshoring_80p_l')]

energy_consumption=data.table(energy_consumption)
energy_consumption_national=energy_consumption[,.(fuel=sum(value)),by=c('scenario','year','input','Units')]

input_subsector=data.table(input_subsector)
input_subsector_national=input_subsector[,.(input=sum(value)),by=c('scenario','year','input','Units')]

output_subsector=data.table(output_subsector)
output_subsector_national=output_subsector[output_subsector$year>2015,.(output=sum(value)),by=c('scenario','year','subsector...5','Units')]

service_output_tech = data.table(service_output_tech)
service_national=service_output_tech[(service_output_tech$year>2015) & (service_output_tech$sector=='trn_pass_road_LDV_4W'),]

cost_tech = data.table(cost_tech)
service_tech_cost = merge(service_output_tech, cost_tech, by = c('scenario','sector','subsector','technology','year','region'), all = TRUE)
service_tech_cost = data.table(service_tech_cost)
check = service_tech_cost[service_tech_cost$region == 'AK' & service_tech_cost$year>2010 & service_tech_cost$scenario == 'only_stick_80p' & service_tech_cost$sector == 'trn_pass_road_LDV_4W',]

service_tech_total_cost=service_tech_cost[, .(total_cost=sum(value.x*value.y)), by =c('scenario','year','sector','subsector','technology')] 
sector = service_tech_total_cost[service_tech_total_cost$year == 2020, .(sector,subsector,technology)]

CO2_emission = data.table(CO2_emission)
CO2_total=CO2_emission[(CO2_emission$year>2015) & CO2_emission$region != 'USA',.(CO2=sum(value)),by=c('scenario','year','Units')]


CO2_USA=read.csv(paste0(path_CO2,"CO2_sectoral/CO2_sector.csv"))%>%setDT()
CO2_USA_national=CO2_USA[CO2_USA$region!="USA" & CO2_USA$Year>2010,]
CO2_USA_national=CO2_USA_national[,.(CO2=sum(co2.emiss)),by=list(sector,scenario,Year)]

sector_code=CO2_USA_national[CO2_USA_national$scenario == "baseline_80p" & CO2_USA_national$Year==2050,.(sector)]
sector_code[,old_id:=list(c(1:35))]

CO2_national= CO2_USA_national
CO2_national= merge(CO2_national,sector_code)


sector=read_xlsx(paste0(path_CO2,'CO2_sectoral/sector_aggregate.xlsx'))%>%setDT()
CO2_national=sector[CO2_national,on = .(old_id)]
CO2_scenario=CO2_national[,.(CO2_emission=sum(CO2)*44/12),by=c('scenario','Year','new_sector')]
#=================================================================================================
#CO2_price
#CO2_price$scenario <- factor(CO2_price$scenario, levels = c("baseline_80p", "onshoring_80p_l","onshoring_80p_s","free_80p_l", "free_80p_s","tariff_80p_l","tariff_80p_s"))
CO2_price$scenario <- factor(CO2_price$scenario, levels = c("only_stick_80p","baseline_80p", "onshoring_80p_l","free_80p_l"))
ggplot(data=CO2_price, aes(x=year, y=value,color=scenario))+
  #geom_line(aes(linetype = scenario))+
  geom_line()+
  scale_color_manual(values=c('baseline_80p'= rgb(236/256,126/256,72/256),
                              "onshoring_80p_l" = rgb(252/255,197/255,59/255),
                              "only_stick_80p" = rgb(157/255,76/255,29/255),
                              "free_80p_l"= rgb(117/255,176/255,86/255)
                              ),
                     labels= c(
                     "only_stick_80p"="Immediate stick",
                     "baseline_80p"= "Carrots then stick",
                     "onshoring_80p_l" = "Trade restricktion",
                     "free_80p_l" = "Trade relaxation"
                    # "tariff_80p_l"= "Import tariff"
                     )
                     )+
  #scale_linetype_manual(values = c('solid','solid','dashed','solid','dashed','solid','dashed'))+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  guides(color=guide_legend(title="Scenario"))+
  ylab("Carbon price $/tonne")

CO2_scenario$scenario <- factor(CO2_scenario$scenario, levels = c("only_stick_80p","baseline_80p", "onshoring_80p_l","onshoring_80p_s","tariff_80p_l","tariff_80p_s","free_80p_l", "free_80p_s"))
CO2_scenario = CO2_scenario[! (CO2_scenario$scenario %in% c("baseline_80p",'free_80p_l','onshoring_80p_l', 'tariff_80p_l') & CO2_scenario$Year ==2015), ]
ggplot(data=CO2_scenario[scenario %in% c("only_stick_80p",'baseline_80p', 'free_80p_l','onshoring_80p_l', 'tariff_80p_l') &
                         Year %in% c(2015,2035,2050),
                         ], 
       aes(x=scenario, y=CO2_emission,fill=new_sector))+
  #geom_col_pattern(aes(pattern=scenario), pattern_size = 0.1)+
  geom_bar(stat="identity")+
  facet_grid(~Year,
             scales = "free_x",
             space = "free")+
  scale_x_discrete(labels= c(
    "only_stick_80p" = "Immediate stick",
    "baseline_80p"= "Carrots then stick",
    "onshoring_80p_l" = "Add Onshoring",
    #"onshoring_80p_s" = "Onshoring + short-term",
    "tariff_80p_l"= "Import tariff",
    "free_80p_l" = "Add free trade"
    #"free_80p_s" = "Free trade + short-term",
    #"tariff_80p_s"= "Add import tariff + short-term"
    )
                     )+
  #scale_pattern_manual(values=c('none', 'none', 'stripe','none','stripe','none','stripe'),guide='none') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  guides(fill=guide_legend(title="Sector"))+
  ylab("Carbon emissions (Million tonne)")

options(repr.plot.width = 10, repr.plot.height =2)


CO2_total = CO2_total[CO2_total$scenario %in% c('only_stick_80p','baseline_80p','free_80p_l' , 'onshoring_80p_l')]
CO2_total$scenario <- factor(CO2_total$scenario, levels = c("only_stick_80p","baseline_80p", "onshoring_80p_l","free_80p_l"))

ggplot(data=CO2_total, aes(x=year,y= CO2/1000*44/12,color=scenario))+
  geom_line()+
  scale_color_manual(values=c('baseline_80p'= rgb(236/256,126/256,72/256),
                              "onshoring_80p_l" = rgb(252/255,197/255,59/255),
                              "only_stick_80p" = rgb(157/255,76/255,29/255),
                              "free_80p_l"= rgb(117/255,176/255,86/255)
  ),
  labels= c(
    "only_stick_80p"="Immediate stick",
    "baseline_80p"= "Carrots then stick",
    "onshoring_80p_l" = "Trade restricktion",
    "free_80p_l" = "Trade relaxation"
    # "tariff_80p_l"= "Import tariff"
  )
  )+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  guides(color=guide_legend(title="Scenario"))+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  guides(fill=guide_legend(title="CO2 emission"))+
  ylab("Carbon emissions (giga tonne)")

output_subsector_national$scenario <- factor(output_subsector_national$scenario, levels = c("baseline_80p", "onshoring_80p_l","onshoring_80p_s","free_80p_l", "free_80p_s","tariff_80p_l","tariff_80p_s"))
ggplot(data=output_subsector_national, aes(x=scenario,y=output, fill=subsector...5))+
  geom_col_pattern(aes(pattern=scenario), pattern_size = 0.1)+
  #geom_bar(stat="identity")+
  facet_grid(~year)+
  scale_x_discrete(labels= c(
    "baseline_80p"= "Baseline",
    "onshoring_80p_l" = "Onshoring + persistent",
    "onshoring_80p_s" = "Onshoring + short-term",
    "free_80p_l" = "Free trade + persistent",
    "free_80p_s" = "Free trade + short-term",
    "tariff_80p_l"= "Import tariff + persistent",
    "tariff_80p_s"= "Import tariff + short-term")
    )+
  scale_pattern_manual(values=c('none', 'none', 'stripe','none','stripe','none','stripe'),guide='none') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  guides(fill=guide_legend(title="Energy source"))+
  ylab("energy output (EJ)")

service_national$scenario <- factor(service_national$scenario, levels = c("baseline_80p", "onshoring_80p_l","onshoring_80p_s","free_80p_l", "free_80p_s","tariff_80p_l","tariff_80p_s"))
ggplot(data=service_national, aes(x=scenario,y=service, fill=technology))+
  #geom_bar(stat="identity")+
  geom_col_pattern(aes(pattern=scenario), pattern_size = 0.1)+
  facet_grid(~year)+
  scale_x_discrete(labels= c(
    "baseline_80p"= "Baseline",
    "onshoring_80p_l" = "Onshoring + persistent",
    "onshoring_80p_s" = "Onshoring + short-term",
    "free_80p_l" = "Free trade + persistent",
    "free_80p_s" = "Free trade + short-term",
    "tariff_80p_l"= "Import tariff + persistent",
    "tariff_80p_s"= "Import tariff + short-term")
  )+
  scale_pattern_manual(values=c('none', 'none', 'stripe','none','stripe','none','stripe'),guide='none') +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  guides(fill=guide_legend(title="Energy source"))+
  ylab("million pass-km")

       

