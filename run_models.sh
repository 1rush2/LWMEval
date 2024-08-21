#!/bin/bash

# 定义日期和 lead-time 变量
DATE="20230920"
LEAD_TIME=6

export CUDA_VISIBLE_DEVICES=5
# FuXi
ai-models --input cds --date $DATE --time 0000 fuxi --assets FuXi_EC --lead-time $LEAD_TIME

# PanGu
ai-models --input cds --date $DATE --time 0000 --assets assets-panguweather panguweather --lead-time $LEAD_TIME

# Fourcastnet
ai-models --download-assets --assets assets-fourcastnetv2-small --input cds --date $DATE --time 0000 fourcastnetv2-small --lead-time $LEAD_TIME
ai-models --download-assets --assets assets-fourcastnet --input cds --date $DATE --time 0000 fourcastnet --lead-time $LEAD_TIME

# FengWu
ai-models --input cds --date $DATE --time 0000 fengwuv2 --assets assets-fengwu --lead-time $LEAD_TIME
ai-models --input cds --date $DATE --time 0000 fengwu --assets assets-fengwu --lead-time $LEAD_TIME

# Graphcast
ai-models --assets assets-graphcast --input cds --date $DATE --time 0000 graphcast --lead-time $LEAD_TIME

#chmod +x run_models.sh
#./run_models.sh
