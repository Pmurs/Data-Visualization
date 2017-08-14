
install.packages("RSQLite")
install.packages("ggplot2")

library("RSQLite")
library(ggplot2)

setwd("~/Projects/MassMutual/recruitment/recruit-viz/R/")

drv <- dbDriver("SQLite")
connection = dbConnect(drv=drv, dbname="../recruit.db")

#alltables = dbListTables(connection)
#alltables

#modifier <- "ALTER TABLE customer ADD percent_travel (travel_spending/income)"
#dbExecute(connection, modifier)

query <- 'SELECT income, gender, AVG(sports_leisure_spending), CAST(sports_leisure_spending AS float)/(CAST(income AS float) * 10.0) AS percent_sports FROM customer WHERE income < 100 GROUP BY income, gender ' 

df_customer = dbGetQuery(connection, query)


head(df_customer)

p <- ggplot(df_customer, aes(x= as.factor(income), y = percent_sports * ((-1)^(gender == "M")), fill = gender)) + 
	geom_bar(stat="identity")+
	ggtitle("Average Sports Leisure Spending by Gender (Lower Income)")+
	scale_x_discrete(name = "Annual Income ($1000's)", breaks=seq(0, 100, 10)) +
	scale_y_continuous(name = "Income Spent on Sports Leisure (%)", breaks=seq(-8, 8, .5))
p
	
dbDisconnect(connection)
