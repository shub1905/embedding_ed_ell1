clc;clear;
data = dlmread('data_norm.time', '\t',1,0);

data2 = sortrows(data, [2,3]);
plot(data2(:,2),data2(:,4));