import subprocess
import time
import numpy as np
import pandas as pd

# 监控间隔（秒）
interval = 1.0
gpu_id = 7  # 要监控的 GPU 编号

# 定义命令字典
DATE = "20230301"
LEAD_TIME = 6
my_dict = {
    "fuxi": f"ai-models --input cds --date {DATE} --time 0000 fuxi --assets FuXi_EC --lead-time {LEAD_TIME}",
    "pangu": f"ai-models --input cds --date {DATE} --time 0000 --assets assets-panguweather panguweather --lead-time {LEAD_TIME}",
    "fourcastnetv2-small": f"ai-models --download-assets --assets assets-fourcastnetv2-small --input cds --date {DATE} --time 0000 fourcastnetv2-small --lead-time {LEAD_TIME}",
    "fourcastnet": f"ai-models --download-assets --assets assets-fourcastnet --input cds --date {DATE} --time 0000 fourcastnet --lead-time {LEAD_TIME}",
    "fengwuv2": f"ai-models --input cds --date {DATE} --time 0000 fengwuv2 --assets assets-fengwu --lead-time {LEAD_TIME}",
    "fengwu": f"ai-models --input cds --date {DATE} --time 0000 fengwu --assets assets-fengwu --lead-time {LEAD_TIME}",
    "graphcast": f"ai-models --assets assets-graphcast --input cds --date {DATE} --time 0000 graphcast --lead-time {LEAD_TIME}"
}

def get_gpu_usage(gpu_id):
    """使用 nvidia-smi 获取指定 GPU 的利用率和内存使用情况"""
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,nounits,noheader"],
        stdout=subprocess.PIPE,
        text=True
    )
    usage_info = [x.split(",") for x in result.stdout.strip().split("\n")]
    gpu_utilization = int(usage_info[gpu_id][0])
    memory_used = int(usage_info[gpu_id][1])
    memory_total = int(usage_info[gpu_id][2])
    memory_percent = memory_used / memory_total * 100
    return gpu_utilization, memory_used, memory_total, memory_percent

# 初始化数据列表
data = []

for name, command in my_dict.items():
    # GPU 利用率和内存占用列表
    gpu_utilizations = []
    memory_usages = []
    memory_percentages = []

    # 记录推理开始时间
    start_time = time.time()

    # 启动推理命令
    process = subprocess.Popen(command, shell=True)

    try:
        # 当推理命令在运行时，每隔 interval 秒收集一次 GPU 利用率和内存使用情况
        while process.poll() is None:
            gpu_utilization, memory_used, _, memory_percent = get_gpu_usage(gpu_id)
            gpu_utilizations.append(gpu_utilization)
            memory_usages.append(memory_used)
            memory_percentages.append(memory_percent)
            time.sleep(interval)

        # 确保捕获最后一次数据
        gpu_utilization, memory_used, _, memory_percent = get_gpu_usage(gpu_id)
        gpu_utilizations.append(gpu_utilization)
        memory_usages.append(memory_used)
        memory_percentages.append(memory_percent)

    finally:
        # 等待进程结束
        process.wait()

    # 记录推理结束时间
    end_time = time.time()

    # 计算平均和最大值
    average_gpu_utilization = np.mean(gpu_utilizations)
    max_gpu_utilization = np.max(gpu_utilizations)
    average_memory_usage = np.mean(memory_usages)
    max_memory_usage = np.max(memory_usages)
    average_memory_percentage = np.mean(memory_percentages)
    max_memory_percentage = np.max(memory_percentages)

    # 存储结果
    data.append({
        "Model": name,
        "Total Time (s)": end_time - start_time,
        "Average GPU Utilization (%)": average_gpu_utilization,
        "Max GPU Utilization (%)": max_gpu_utilization,
        "Average Memory Usage (MiB)": average_memory_usage,
        "Max Memory Usage (MiB)": max_memory_usage,
        "Average Memory Percentage (%)": average_memory_percentage,
        "Max Memory Percentage (%)": max_memory_percentage,
    })

# 将结果保存到CSV文件
df = pd.DataFrame(data)
df.to_csv("gpu_performance_metrics.csv", index=False)
print("结果已保存到 gpu_performance_metrics.csv")
