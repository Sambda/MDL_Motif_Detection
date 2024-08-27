# MDL_Motif_Detection


This project deals with the area of time series clustering, aiming to discover structures and recurring patterns in time series by clustering similar subsequences. Such clusters of patterns are referred to as motifs. 

The clustering is performed in a parameter-free manner so that even motifs in unknown data can be successfully detected. 

For this reason the minimum description length (MDL) principle is used to identify similar subsequences and evaluate the resulting motifs. The MDL principle states that the best model for describing a data set is the model that minimizes the description length of the entire data set. Based on this assumption, the motif discovery algorithm searches for the model that best compresses the data. In other words, it looks for recurring patterns in the data in order to describe the data based on them. This method can thus also be used for aggregating time series data. 
