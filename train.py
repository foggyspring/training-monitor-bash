#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试用训练脚本
模拟机器学习训练过程，支持命令行参数
"""

import time
import random
import argparse
import sys

def progress_bar(current, total, width=50):
    """生成进度条"""
    percent = current / total
    filled = int(width * percent)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {percent:.1%}"

def simulate_training(epochs, steps_per_epoch=10, error_test=False):
    """模拟训练过程"""
    print(f"🚀 开始训练模型...")
    print(f"📊 训练参数: epochs={epochs}, steps_per_epoch={steps_per_epoch}")
    print(f"⏰ 开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    total_steps = epochs * steps_per_epoch
    current_step = 0
    
    for epoch in range(epochs):
        print(f"\n📈 Epoch {epoch + 1}/{epochs}")
        print(f"🔄 开始第 {epoch + 1} 轮训练...")
        
        epoch_loss = 0
        epoch_accuracy = 0
        
        for step in range(steps_per_epoch):
            current_step += 1
            
            # 模拟训练过程
            base_loss = random.uniform(0.5, 2.0)
            base_accuracy = random.uniform(0.7, 0.95)
            
            # 随着训练进行，损失逐渐下降，准确率逐渐上升
            progress_factor = current_step / total_steps
            loss = base_loss * (1 - progress_factor * 0.8)
            accuracy = base_accuracy + (progress_factor * 0.2)
            
            epoch_loss += loss
            epoch_accuracy += accuracy
            
            # 生成进度条
            progress = progress_bar(step + 1, steps_per_epoch)
            
            # 输出训练信息
            print(f"  {progress} Loss: {loss:.4f}, Acc: {accuracy:.4f}")
            
            # 模拟错误测试
            if error_test and epoch == 2 and step == 5:
                print(f"  ❌ 模拟训练错误：数据维度不匹配")
                print(f"  🔄 尝试恢复训练...")
                time.sleep(1)
                print(f"  ✅ 错误已处理，继续训练")
            
            time.sleep(0.3)
        
        # 计算平均指标
        avg_loss = epoch_loss / steps_per_epoch
        avg_accuracy = epoch_accuracy / steps_per_epoch
        
        print(f"📊 Epoch {epoch + 1} 完成:")
        print(f"  平均损失: {avg_loss:.4f}")
        print(f"  平均准确率: {avg_accuracy:.4f}")
        
        # 保存检查点
        print(f"💾 保存检查点: checkpoint_epoch_{epoch + 1}.pth")
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("🎉 训练完成！")
    print(f"⏰ 结束时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📈 最终模型已保存到: final_model.pth")
    print(f"📊 训练报告已生成: training_report.txt")
    print("=" * 60)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='模拟机器学习训练过程')
    parser.add_argument('--epochs', type=int, default=5, help='训练轮数 (默认: 5)')
    parser.add_argument('--steps-per-epoch', type=int, default=10, help='每轮步数 (默认: 10)')
    parser.add_argument('--batch-size', type=int, default=32, help='批次大小 (默认: 32)')
    parser.add_argument('--lr', type=float, default=0.001, help='学习率 (默认: 0.001)')
    parser.add_argument('--error-test', action='store_true', help='启用错误测试模式')
    
    args = parser.parse_args()
    
    # 验证参数
    if args.epochs <= 0:
        print("❌ 错误: epochs 必须大于 0")
        sys.exit(1)
    
    if args.steps_per_epoch <= 0:
        print("❌ 错误: steps-per-epoch 必须大于 0")
        sys.exit(1)
    
    if args.batch_size <= 0:
        print("❌ 错误: batch-size 必须大于 0")
        sys.exit(1)
    
    if args.lr <= 0:
        print("❌ 错误: lr 必须大于 0")
        sys.exit(1)
    
    # 显示训练配置
    print("🔧 训练配置:")
    print(f"  Epochs: {args.epochs}")
    print(f"  Steps per epoch: {args.steps_per_epoch}")
    print(f"  Batch size: {args.batch_size}")
    print(f"  Learning rate: {args.lr}")
    print(f"  Error test mode: {'启用' if args.error_test else '禁用'}")
    print()
    
    try:
        simulate_training(args.epochs, args.steps_per_epoch, args.error_test)
    except KeyboardInterrupt:
        print("\n⚠️  训练被用户中断")
        print("💾 保存当前进度...")
        time.sleep(1)
        print("✅ 进度已保存")
    except Exception as e:
        print(f"\n❌ 训练过程中发生错误: {e}")
        print("💾 尝试保存当前进度...")
        time.sleep(1)
        print("✅ 进度已保存")
        sys.exit(1)

if __name__ == "__main__":
    main() 