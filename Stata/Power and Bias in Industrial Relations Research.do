*** Stata file for Doucouliagos, Doucouliagos and Stanley, "Power and bias in industrial relations research", British Journal of Industrial Relations.
*** Use the data file "Power and Bias.dta" for Figure 1 and 2 and Table 2.


** Construction of Figure 1, Panel A
scatter effectsize standarderror if filename == "Copy of Employee Ownership_With Authors.xlsx"
** Construction of Figure 1, Panel B
scatter effectsize standarderror if filename == "7. MA_Union&Satisfaction_PL authors.xlsx"

** Construction of Figure 2, Panel A
scatter effectsize standarderror if filename == "Own price elasticity of labour with authors.xlsx"
** Construction of Figure 2, Panel B
scatter effectsize standarderror if filename == "wage impact of teachers unions.xlsx"


*** Construction of Table 2
encode journal, gen(Njournal)
encode filename , gen(Nresearcharea)

*** The variable 'IR1' identifies industrial relations journals
gen IR1 = 0 
replace IR1 = 1 if journal == "Journal of industrial relations"
replace IR1 = 1 if journal == "Relations industrielles/industrial relations"
replace IR1 = 1 if journal == "Economic and industrial democracy"
replace IR1 = 1 if journal == "Advances in industrial and labor relations"
replace IR1 = 1 if journal == "British journal of industrial relations"
replace IR1 = 1 if journal == "European journal of industrial relations"
replace IR1 = 1 if journal == "Industrial relations: a journal of economy and society"
replace IR1 = 1 if journal == "Industrial relations journal"
replace IR1 = 1 if journal == "Industrial and labor relations review"
replace IR1 = 1 if journal == "Labour: review of labour economics and industrial relations"
replace IR1 = 1 if journal == "Work and occupations"
tabulate journal if IR1 ==1

*** The variable 'IR2' identifies labour economics journals
gen IR2 = 0 
replace IR2 = 1 if journal == "Monthly labor review"
replace IR2 = 1 if journal == "Labour economics"
replace IR2 = 1 if journal == "Journal of human resources"
replace IR2 = 1 if journal == "Journal of labor economics"
replace IR2 = 1 if journal == "Journal of labor research"
replace IR2 = 1 if journal == "The indian journal of labour economics"
replace IR2 = 1 if journal == "Research in labor economics"
replace IR2 = 1 if journal == "Australian journal of labour economics"
replace IR2 = 1 if journal == "International labour review"
replace IR2 = 1 if journal == "Iza journal of european labor studies"
replace IR2 = 1 if journal == "Iza journal of labor economics"
replace IR2 = 1 if journal == "International journal of manpower"
tabulate journal if IR2 ==1

*** The variable 'TOP5' identifies the top 5 economics journals
gen TOP5 = 0
replace TOP5 = 1 if journal == "Econometrica" 
replace TOP5 = 1 if journal == "Journal of political economy"
replace TOP5 = 1 if journal == "The american economic review"
replace TOP5 = 1 if journal == "The review of economic studies"
replace TOP5 = 1 if journal == "The quarterly journal of economics"
tabulate journal if TOP5 ==1

*** The variable 'Management' identifies management journals
gen Management = 0 
replace Management = 1 if journal == "Academy of management journal"
replace Management = 1 if journal == "Administrative science quarterly"
replace Management = 1 if journal == "Administration and society"
replace Management = 1 if journal == "African journal of business management"
replace Management = 1 if journal == "Asia pacific journal of management"
replace Management = 1 if journal == "Asian academy of management journal of accounting and finance"
replace Management = 1 if journal == "Australian journal of management"
replace Management = 1 if journal == "European management review"
replace Management = 1 if journal == "Hospitality management"
replace Management = 1 if journal == "Human resource management"
replace Management = 1 if journal == "Human resource management journal"
replace Management = 1 if journal == "Human resource planning"
replace Management = 1 if journal == "International journal of commerce and management"
replace Management = 1 if journal == "International journal of human resource management"
replace Management = 1 if journal == "International journal of management"
replace Management = 1 if journal == "International public management journal"
replace Management = 1 if journal == "Journal of management"
replace Management = 1 if journal == "Journal of management and governance"
replace Management = 1 if journal == "Journal of management and organization"
replace Management = 1 if journal == "Journal of management and strategy"
replace Management = 1 if journal == "Journal of management development"
replace Management = 1 if journal == "Journal of management studies"
replace Management = 1 if journal == "Journal of organizational behavior"
replace Management = 1 if journal == "Journal of service management"
replace Management = 1 if journal == "Journal of small business management"
replace Management = 1 if journal == "Management international review"
replace Management = 1 if journal == "Management research review"
replace Management = 1 if journal == "Management revue"
replace Management = 1 if journal == "Management science"
replace Management = 1 if journal == "Public performance and management review"
replace Management = 1 if journal == "Scandinavian journal management"
replace Management = 1 if journal == "Strategic management journal"
replace Management = 1 if journal == "The international journal of human resource management"
replace Management = 1 if journal == "Journal of occcupational behavior"
replace Management = 1 if journal == "Group and organization management"
replace Management = 1 if journal == "Personnel review"
replace Management = 1 if journal == "Taiwan academy of management journal"
replace Management = 1 if journal == "Organization science"
replace Management = 1 if journal == "German journal of human resource research" 

*** The variable 'ALLEco' identifies all economics research
gen OtherEco = 0
replace OtherEco = 1 if journal == "Applied economics"
replace OtherEco = 1 if journal == "The journal of development studies"
replace OtherEco = 1 if journal == "Southern economic journal"
replace OtherEco = 1 if journal == "Review of economics of the household" 
replace OtherEco = 1 if journal == "Regional studies"
replace OtherEco = 1 if journal == "Oxford economic papers"
replace OtherEco = 1 if journal == "Journal of population economics" 
replace OtherEco = 1 if journal == "Economics of education review"
replace OtherEco = 1 if journal == "Economics letters"
replace OtherEco = 1 if journal == "Economica"
replace OtherEco = 1 if journal == "Brookings papers on economic activity"
replace OtherEco = 1 if journal == "Cambridge journal of economics"
replace OtherEco = 1 if journal == "China economic review"
replace OtherEco = 1 if journal == "China economic journal" 
replace OtherEco = 1 if journal == "Applied economics letters" 
replace OtherEco = 1 if journal == "Canadian journal of economics"
replace OtherEco = 1 if journal == "Journal of law and economics" 
replace OtherEco = 1 if journal == "Journal of evolutionary economics" 
replace OtherEco = 1 if journal == "Journal of economics and business"
replace OtherEco = 1 if journal == "Journal of economic literature"
replace OtherEco = 1 if journal == "Economic inquiry" 
replace OtherEco = 1 if journal == "Economia"
replace OtherEco = 1 if journal == "Economic policy" 
replace OtherEco = 1 if journal == "Economic systems" 
replace OtherEco = 1 if journal == "Eastern european economics"
replace OtherEco = 1 if journal == "Eastern economic journal"
replace OtherEco = 1 if journal == "Bulletin of indonesian economic studies" 
replace OtherEco = 1 if journal == "The american economist" 
replace OtherEco = 1 if journal == "Small business economics"
replace OtherEco = 1 if journal == "Review of development economics"
replace OtherEco = 1 if journal == "Post-communist economies" 
replace OtherEco = 1 if journal == "Oxford bulletin of economics and statistics"
replace OtherEco = 1 if journal == "Australian economic papers"
replace OtherEco = 1 if journal == "Australian economic review" 
replace OtherEco = 1 if journal == "Brookings papers on economic activity. microeconomics"
replace OtherEco = 1 if journal == "Brookings papers on economic activity"
replace OtherEco = 1 if journal == "Contemporary economic policy"
replace OtherEco = 1 if journal == "Developing economies"
replace OtherEco = 1 if journal == "Economics of transition"
replace OtherEco = 1 if journal == "Education economics"
replace OtherEco = 1 if journal == "Empirical economics"
replace OtherEco = 1 if journal == "European journal of law and economics"
replace OtherEco = 1 if journal == "Scottish journal of political economy"
replace OtherEco = 1 if journal == "Review of social economy"
replace OtherEco = 1 if journal == "Research in economics"
replace OtherEco = 1 if journal == "Pacific economic review"
replace OtherEco = 1 if journal == "Oecd economic studies"
replace OtherEco = 1 if journal == "Economic development and cultural change"
replace OtherEco = 1 if journal == "Fiscal studies" 
replace OtherEco = 1 if journal == "The economic record"
replace OtherEco = 1 if journal == "Structural change and economic dynamics" 
replace OtherEco = 1 if journal == "Economic bulletin"
replace OtherEco = 1 if journal == "Economic change and restructuring"
replace OtherEco = 1 if journal == "Economic modelling"
replace OtherEco = 1 if journal == "Economics of innovation and new technology"
replace OtherEco = 1 if journal == "Journal of international economics"
replace OtherEco = 1 if journal == "Journal of economic studies"
replace OtherEco = 1 if journal == "Journal of macroeconomics" 
replace OtherEco = 1 if journal == "National institute economic review"
replace OtherEco = 1 if journal == "Nber paper series"
replace OtherEco = 1 if journal == "New zealand economic papers" 
replace OtherEco = 1 if journal == "Manchester school" 
replace OtherEco = 1 if journal == "Kyklos"
replace OtherEco = 1 if journal == "Journal of productivity analysis"
replace OtherEco = 1 if journal == "Journal of the asia pacific economy"
replace OtherEco = 1 if journal == "Journal of comparative economics"
replace OtherEco = 1 if journal == "Journal of asian economics"
replace OtherEco = 1 if journal == "Journal of applied econometrics"
replace OtherEco = 1 if journal == "Journal of agricultural economics"
replace OtherEco = 1 if journal == "German economic review"
replace OtherEco = 1 if journal == "International journal of industrial organization"
replace OtherEco = 1 if journal == "Jahrbucher fur nationalokonomie und statistik"
replace OtherEco = 1 if journal == "Scandinavian journal of economics" 
replace OtherEco = 1 if journal == "Revista brasileira de economia" 
replace OtherEco = 1 if journal == "Review of world economics"
replace OtherEco = 1 if journal == "Managerial and decision economics" 
replace OtherEco = 1 if journal == "Journal of the japanese and international economies"
replace OtherEco = 1 if journal == "Journal of applied economics"
replace OtherEco = 1 if journal == "International economic journal"
replace OtherEco = 1 if journal == "Schmalenbach business review"
replace OtherEco = 1 if journal == "Journal of risk and uncertainty"
replace OtherEco = 1 if journal == "Journal of economic perspectives" 
replace OtherEco = 1 if journal == "International journal of the economics of business"
replace OtherEco = 1 if journal == "Growth and change"
replace OtherEco = 1 if journal == "Finnish economic papers"
replace OtherEco = 1 if journal == "European journal of political economy"
replace OtherEco = 1 if journal == "Economic analysis"
replace OtherEco = 1 if journal == "Atlantic economic journal"
replace OtherEco = 1 if journal == "American journal of agricultural economics"
replace OtherEco = 1 if journal == "The journal of economics" 
replace OtherEco = 1 if journal == "The journal of economic perspectives"
replace OtherEco = 1 if journal == "Review of economic dynamics"
replace OtherEco = 1 if journal == "Review of black political economy"
replace OtherEco = 1 if journal == "Review of industrial organization"
replace OtherEco = 1 if journal == "Review of international economics"
replace OtherEco = 1 if journal == "The journal of socio-economics"
replace OtherEco = 1 if journal == "Socio-economic review"
replace OtherEco = 1 if journal == "World development"
replace OtherEco = 1 if journal == "World economy"
replace OtherEco = 1 if journal == "The be journal of economic analysis and policy" 
replace OtherEco = 1 if journal == "Swedish economic policy review"
replace OtherEco = 1 if journal == "Studies on economics"
replace OtherEco = 1 if journal == "South african journal of economics"
replace OtherEco = 1 if journal == "Revue économique" 
replace OtherEco = 1 if journal == "Seoul journal of economics"
replace OtherEco = 1 if journal == "Empirica" 
replace OtherEco = 1 if journal == "Colombian economic journal"
replace OtherEco = 1 if journal == "Comparative economic studies"
replace OtherEco = 1 if journal == "Economic systems research"
gen TOP31 = 0
replace TOP31 = 1 if journal == "American economic journal: applied economics"
replace TOP31 = 1 if journal == "American economic journal: macroeconomics"
replace TOP31 = 1 if journal == "American economic journal: economic policy"
replace TOP31 = 1 if journal == "American economic journal: microeconomics"
replace TOP31 = 1 if journal == "Econometrica" 
replace TOP31 = 1 if journal == "European economic review"
replace TOP31 = 1 if journal == "Games and economic behavior"
replace TOP31 = 1 if journal == "Health economics" 
replace TOP31 = 1 if journal == "International economic review" 
replace TOP31 = 1 if journal == "Journal of the european economic association"
replace TOP31 = 1 if journal == "Journal of political economy"
replace TOP31 = 1 if journal == "Journal of business and economic statistics"
replace TOP31 = 1 if journal == "Journal of development economics"
replace TOP31 = 1 if journal == "Journal of econometrics" 
replace TOP31 = 1 if journal == "Journal of human resources"
replace TOP31 = 1 if journal == "Journal of labor economics"
replace TOP31 = 1 if journal == "Journal of money credit and banking"  
replace TOP31 = 1 if journal == "Journal of economic growth"
replace TOP31 = 1 if journal == "Journal of industrial economics" 
replace TOP31 = 1 if journal == "Journal of financial economics" 
replace TOP31 = 1 if journal == "Journal of economic theory"
replace TOP31 = 1 if journal == "Journal of health economics"
replace TOP31 = 1 if journal == "Journal of monetary economics"
replace TOP31 = 1 if journal == "Journal of public economics"
replace TOP31 = 1 if journal == "Public choice" 
replace TOP31 = 1 if journal == "Rand journal of economics"
replace TOP31 = 1 if journal == "The quarterly journal of economics"
replace TOP31 = 1 if journal == "The american economic review"
replace TOP31 = 1 if journal == "The economic journal"
replace TOP31 = 1 if journal == "The review of economic studies"
replace TOP31 = 1 if journal == "The review of economics and statistics" 
replace TOP31 = 1 if journal == "The journal of finance"
gen ALLEco = 0
replace ALLEco = 1 if OtherEco == 1
replace ALLEco = 1 if TOP31 == 1
tabulate journal if ALLEco ==1
tabulate filename if ALLEco ==1

*** Following commands create TABLE 2 Power, significance and bias in industrial relations research
** Row (1) all industrial relations research
sum power_196 tstat , detail
sum tstat if tstat >=1.96
sum ex_sig_196
reg effect, cluster(filename)
** Row (2) industrial relations journals
sum power_196 tstat if IR1 == 1, detail
sum tstat if tstat >=1.96 & IR1 ==1
sum ex_sig_196 if IR1 == 1
reg effect if IR1 == 1, cluster(filename)
** Row (3) labour economics journals
sum power_196 tstat if IR2 == 1, detail
sum tstat if tstat >=1.96 & IR2 ==1
sum ex_sig_196 if IR2 == 1
reg effect if IR2 == 1, cluster(filename)
** Row (4) Top 5 journals
sum power_196 tstat if TOP5 == 1, detail
sum tstat if tstat >=1.96 & TOP5 ==1
sum ex_sig_196 if TOP5 == 1
reg effect if TOP5 == 1, cluster(filename)
** Row (5) All other economics journals
sum power_196 tstat if ALLEco ==1 & TOP5 !=1 & IR2 !=1, detail
sum tstat if tstat >=1.96 & ALLEco ==1 & TOP5 !=1 & IR2 !=1
sum ex_sig_196 if ALLEco ==1 & TOP5 !=1 & IR2 !=1
reg effect if ALLEco ==1 & TOP5 !=1 & IR2 !=1, cluster(filename)
** Row (6) management journals
sum power_196 tstat if Management == 1, detail
sum tstat if tstat >=1.96 & Management ==1
sum ex_sig_196 if Management == 1
reg effect if Management == 1, cluster(filename)
** Row (7) All other research
sum power_196 tstat if ALLEco !=1 & TOP5 !=1 & IR2 !=1 & IR1 !=1 & Management != 1, detail
sum tstat if tstat >=1.96 & IR1 !=1 & IR2 !=1 & TOP5 !=1 & ALLEco !=1 & Management != 1
sum ex_sig_196 if ALLEco !=1 & TOP5 !=1 & IR2 !=1 & IR1 !=1 & Management != 1 
reg effect if ALLEco !=1 & TOP5 !=1 & IR2 !=1 & IR1 !=1 & Management != 1 , cluster(filename)


*** Other results reported in the paper
** comparison of sample size, top 5 vs all other research (reported in Section 3)
sum samplesize if TOP5 ==1, detail
sum samplesize if TOP5 !=1, detail


*** The variable 'best' identifies those research areas with power > 80%
gen best = 0
replace best = 1 if filename == "Job security and comitment.xlsx"
replace best = 1 if filename == "Organisational Democracy and comitment.xlsx"
replace best = 1 if filename == "Copy of returns to education in China_With Authors.xlsx"
replace best = 1 if filename == "Job security and job satisfaction.xlsx"
replace best = 1 if filename == "Wanberg et al Age and Reemployment Speed.xlsx"
replace best = 1 if filename == "Organisational Democracy and organisation climate.xlsx"
replace best = 1 if filename == "Organisational Democracy and perceived influence.xlsx"
replace best = 1 if filename == "Discrimination in hiring.xlsx"
replace best = 1 if filename == "Organisational Democracy and civic behavior.xlsx"
replace best = 1 if filename == "Job satisfaction and job performance.xlsx"
replace best = 1 if filename == "Organisational Democracy and prosocial work.xlsx"
replace best = 1 if filename == "Organisational Democracy and work motivation.xlsx"

*** The variable 'IRarear' identifies research areas using correlation coefficients as the effect size 
gen IRarear = 0
replace IRarear = 1 if filename == "7. MA_Union&Satisfaction_PL authors.xlsx"
replace IRarear = 1 if filename == "5. Unions and capital.xlsx"
replace IRarear = 1 if filename == "6. Unions and Intangilbe Capital (2).xlsx"
replace IRarear = 1 if filename == "r partiel January 2016 111 studies.xlsx"
replace IRarear = 1 if filename == "Unions and Productivity Growth Feb 2016 (k=42).xlsx"
replace IRarear = 1 if filename == "Collective Ownership.xlsx"
replace IRarear = 1 if filename == "wage impact of teachers unions.xlsx"
replace IRarear = 1 if filename == "Participation and Productivity Capitalist Firms.xlsx"
replace IRarear = 1 if filename == "Organisational Democracy and perceived alienating work.xlsx"
replace IRarear = 1 if filename == "Organisational Democracy and work motivation.xlsx"
replace IRarear = 1 if filename == "Organisational Democracy and civic behavior.xlsx"
replace IRarear = 1 if filename == "Organisational Democracy and job satisfaction.xlsx"
replace IRarear = 1 if filename == "Organisational Democracy and perceived influence.xlsx"
replace IRarear = 1 if filename == "Organisational Democracy and prosocial work.xlsx"
replace IRarear = 1 if filename == "Organisational Democracy and comitment.xlsx"
replace IRarear = 1 if filename == "Organisational Democracy and organisation climate.xlsx"
replace IRarear = 1 if filename == "Copy of MRA (profitability) April 12 2016 for book with leading.xlsx"
replace IRarear = 1 if filename == "Technological innovation and employment.xlsx"
replace IRarear = 1 if filename == "Participation and Productivity Labor Managed Firms.xlsx"
replace IRarear = 1 if filename == "Copy of returns to education in China_With Authors.xlsx"
replace IRarear = 1 if filename == "participation and satisfaction.xlsx"
replace IRarear = 1 if filename == "Job satisfaction and job performance.xlsx"
replace IRarear = 1 if filename == "Competition and Cooperation in Corporate Governance.xlsx"
replace IRarear = 1 if filename == "Wanberg et al Age and Reemployment Status.xlsx"
replace IRarear = 1 if filename == "Wanberg et al Age and Reemployment Speed.xlsx"
replace IRarear = 1 if filename == "employment protection and unemployment.xlsx"
replace IRarear = 1 if filename == "Tuition and demand for higher education.xlsx"
replace IRarear = 1 if filename == "Copy of Employee Ownership_With Authors.xlsx"
replace IRarear = 1 if filename == "Heavey et al 2013 Collective Turnover.xlsx"
replace IRarear = 1 if filename == "43. UK CEO Pay Douc-Haman-Stanley authors.xlsx"
replace IRarear = 1 if filename == "Turnover Rates and Organizational Performance.xlsx"
replace IRarear = 1 if filename == "Job security and comitment.xlsx"
replace IRarear = 1 if filename == "Job security and job satisfaction.xlsx"

*** compare characteristics of research areas with adequate power to those without adequate power
sum power_196 ex_sig_196 samplesize effectsize UWLS if best ==1 & IRarear ==1, detail
sum power_196 ex_sig_196 samplesize effectsize UWLS if best ==0 & IRarear ==1, detail


*** Construction of Figure 5.
*** Use the data file 'Data for Figure 5'; this removes very large biases
graph dot relativedifference if relativedifference < 8, over( area)
** alternate graph with all research areas included
graph dot relativedifference , over( area)


