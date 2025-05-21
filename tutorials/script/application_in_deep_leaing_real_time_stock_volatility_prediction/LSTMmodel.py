import torch
import torch.nn as nn
import torch.optim as optim
import dolphindb as ddb
from dolphindb_tools.dataloader import DDBDataLoader
from torch.nn.parallel import DistributedDataParallel
from torch.utils.data import Subset
import pandas as pd
import warnings
import time

# 模型定义
class LSTMModel(nn.Module):
    def __init__(self, inputSize, units):
        super(LSTMModel, self).__init__()
        self.lstm1 = nn.LSTM(input_size=inputSize, hidden_size=units, batch_first=True, dropout=0.4)
        self.lstm2 = nn.LSTM(input_size=units, hidden_size=128, batch_first=True, dropout=0.3)
        self.lstm3 = nn.LSTM(input_size=128, hidden_size=32, batch_first=True, dropout=0.1)
        self.fc = nn.Linear(32, 1)

    def forward(self, x):
        out, _ = self.lstm1(x)
        out, _ = self.lstm2(out)
        out, _ = self.lstm3(out)
        out = out[:, -1, :]  
        out = self.fc(out)
        return out

# 定义主函数
def main():
    # 设置设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 数据预处理，并切分训练集和测试集
    conn = ddb.session("192.168.100.201", 8848, "admin", "123456")
    conn.run("""startDay = 2021.01.01
                endDay = 2021.12.31
                splitDay = (startDay..endDay)[((endDay-startDay)*0.8).floor()]
                Data = select FactorValues from loadTable("dfs://tenMinutesFactorDB", "tenMinutesFactorTB") where date(DateTime) >= objByName('startDay') and date(DateTime) <= objByName('endDay') and SecurityID=`600030 pivot by DateTime, SecurityID, FactorNames 
                Data = Data[each(isValid, Data.values()).rowAnd()]
                """)
    
    # Dataloader 参数
    targetColumns = ["LogReturn0_realizedVolatility"]
    excludedColumns = ["SecurityID", "DateTime", "LogReturn0_realizedVolatility"]
    batchSize = 256
    windowSize = [120, 1]
    windowStride=[1, 1]
    offset = 120
    trainSql = """select * from objByName('Data') where date(DateTime) >= objByName('startDay') and date(DateTime) <= objByName('splitDay')"""
    testSql = """select * from objByName('Data') where date(DateTime) > objByName('splitDay') and date(DateTime) <= objByName('endDay')"""  

    # 实例化 DDBDataloader
    trainLoader = DDBDataLoader(ddbSession=conn, sql=trainSql, targetCol=targetColumns, excludeCol=excludedColumns, batchSize=batchSize, device=device, windowSize=windowSize, windowStride=windowStride, offset=offset)
    testLoader = DDBDataLoader(ddbSession=conn, sql=testSql, targetCol=targetColumns, excludeCol=excludedColumns, batchSize=batchSize, device=device, windowSize=windowSize, windowStride=windowStride, offset=offset)
    print("Using DDBDataLoader, data is ready")
    
    # 初始化模型
    model = LSTMModel(inputSize=675, units=256)
    model.to(device)

    # 设置损失函数、优化器和学习率调度器
    criterion = nn.SmoothL1Loss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=3, factor=0.5)

    # 模型训练
    startTime = time.time()
    bestLoss = float('inf')
    for epoch in range(100):
        epochStartTime = time.time()
        
        # 训练阶段
        model.train()
        trainLoss = 0.0
        trainLen = 0
        for inputs, targets in trainLoader:
            inputs = inputs.float().to(device)
            targets = targets.float().to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            trainLoss += loss.item()
            loss.backward()
            optimizer.step()
            trainLen += 1
        trainLoss /= trainLen

        # 测试阶段
        model.eval()
        testLoss = 0.0
        testLen = 0
        with torch.no_grad():
            for inputs, targets in testLoader:
                inputs = inputs.float().to(device)
                targets = targets.float().to(device)
                outputsTest = model(inputs)
                testLoss += criterion(outputsTest, targets).item()
                testLen += 1
        testLoss /= testLen
        print(f'Epoch {epoch+1}, Train Loss: {trainLoss}, Test Loss: {testLoss}')

        # 如果当前测试损失较好，保存模型
        if testLoss < bestLoss:
            bestLoss = testLoss
            torchScriptModel = torch.jit.script(model)
            torchScriptModel.save("/home/lnfu/ytxie/LSTMmodel.pt")
            print(f'New best model saved with test loss: {bestLoss}')

        # 学习率调整
        scheduler.step(testLoss)

        epochEndTime = time.time()
        print(f"Epoch {epoch+1} training time: {epochEndTime - epochStartTime} seconds")

    endTime = time.time()
    print(f"Total training time: {endTime - startTime} seconds")

if __name__ == "__main__":
    main()