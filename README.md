# 项目路由表

各项目对应的电路设计仓库与程序仓库索引。

可视化索引页：[index.html](index.html) — 浏览器直接打开即可，纯静态、无外部依赖。

数据源为 `routes.json`，本文件与 `index.html` 均由脚本生成，只改数据源、不改生成结果。

<!-- routes:begin 生成区 — 由 scripts/build_route.py 从 routes.json 生成，请勿手改 -->

## 1. 骨密度电源控制拓展板

| 类型 | 仓库 |
| --- | --- |
| 电路 | [GK_C132](https://github.com/darwinstudio/GK_C132) |
| 程序 · App | [BMD_PowerRelay](https://github.com/darwinstudio/BMD_PowerRelay) |

## 2. 人体成分转盘驱动板

| 类型 | 仓库 |
| --- | --- |
| 电路 | [GK_C129](https://github.com/darwinstudio/GK_C129) |
| 程序 · Boot | [HumanDisk_Boot](https://github.com/darwinstudio/HumanDisk_Boot) |
| 程序 · App | [HumanDisk](https://github.com/darwinstudio/HumanDisk) |

## 3. 四诊仪LED电路板

| 类型 | 仓库 |
| --- | --- |
| 电路 · 主控板 | [GK_C130](https://github.com/darwinstudio/GK_C130) |
| 电路 · 圆环灯板 | [GK_C131](https://github.com/darwinstudio/GK_C131) |
| 程序 · Boot | [LEDDriver_FourDiagnostic_Boot](https://github.com/darwinstudio/LEDDriver_FourDiagnostic_Boot) |
| 程序 · App | [LEDDriver_FourDiagnostic](https://github.com/darwinstudio/LEDDriver_FourDiagnostic) |

## 4. 人体成分通信转接电路板

| 类型 | 仓库 |
| --- | --- |
| 电路 | [GK_C123](https://github.com/darwinstudio/GK_C123) |

## 5. 体检一体机身高体重电路板

| 类型 | 仓库 |
| --- | --- |
| 程序 | [BodySense_Node](https://github.com/darwinstudio/BodySense_Node) |

## 6. 移送样模块控制板

| 类型 | 仓库 |
| --- | --- |
| 电路 | [GK_C122](https://github.com/darwinstudio/GK_C122) |
| 程序 · Boot | [TransferSampleModule_Boot](https://github.com/darwinstudio/TransferSampleModule_Boot) |
| 程序 · App | [TransferSampleModule](https://github.com/darwinstudio/TransferSampleModule) |

## 7. 白带分析仪主控板

| 类型 | 仓库 |
| --- | --- |
| 电路 | [GK_C113](https://github.com/darwinstudio/GK_C113) |
| 程序 · Boot | [TrackAnalyzerControllerBoot](https://github.com/darwinstudio/TrackAnalyzerControllerBoot) |
| 程序 · App | [TrackAnalyzerController](https://github.com/darwinstudio/TrackAnalyzerController) |

## 8. 轨道式检测仪器公共小板

| 类型 | 仓库 |
| --- | --- |
| 电路 · 槽型限位 | [GK_C101](https://github.com/darwinstudio/GK_C101) |
| 电路 · 漫反射传感器 | [GK_C102](https://github.com/darwinstudio/GK_C102) |
| 电路 · 采样臂转接板 | [GK_C106](https://github.com/darwinstudio/GK_C106) |

## 9. 微量同杯检测电路板

| 类型 | 仓库 |
| --- | --- |
| 电路 · 信号板 | [GK_C127](https://github.com/darwinstudio/GK_C127) |
| 电路 · 传感器板 | [GK_C128](https://github.com/darwinstudio/GK_C128) |

## 10. 电子脊柱测量仪

| 类型 | 仓库 |
| --- | --- |
| 电路 · 按键板 | [GK_C116](https://github.com/darwinstudio/GK_C116) |
| 电路 · 指示灯板 | [GK_C117](https://github.com/darwinstudio/GK_C117) |
| 电路 · USB无线模块 | [GK_C119](https://github.com/darwinstudio/GK_C119) |
| 程序 · Boot | [SpineScannerBoot](https://github.com/darwinstudio/SpineScannerBoot) |
| 程序 · App | [SpineScanner](https://github.com/darwinstudio/SpineScanner) |
| 程序 · UI | [SpineScannerUI](https://github.com/darwinstudio/SpineScannerUI) |
| 程序 · Client | [SpineScannerApp](https://github.com/darwinstudio/SpineScannerApp) |
| 程序 · Docs | [SpineScannerDocs](https://github.com/darwinstudio/SpineScannerDocs) |

## 11. 程序复用模块

| 类型 | 仓库 |
| --- | --- |
| 程序 · 步进电机控制 | [MultiStepMotor](https://github.com/darwinstudio/MultiStepMotor) |
| 程序 · LED控制 | [MultiLED](https://github.com/darwinstudio/MultiLED) |
| 程序 · 限位检测 | [MultiSlotLimit](https://github.com/darwinstudio/MultiSlotLimit) |
| 程序 · 串口通信 | [MultiUartStream](https://github.com/darwinstudio/MultiUartStream) |
| 程序 · 蜂鸣器控制 | [BuzzerPattern](https://github.com/darwinstudio/BuzzerPattern) |

<!-- routes:end -->

## 维护方式

修改 `routes.json` 后执行：

```bash
python scripts/build_route.py
```

- `kind`：`hw` = 电路，`fw` = 程序
- `role`：可选的角色细分（`App`、`Boot`、`主控板`、`槽型限位固定` 等）；不填则只显示大类
- 序号由数组顺序自动生成，中间插入新项目不需要重新编号
- `--check` 只校验不写文件，生成结果与 `routes.json` 不一致时返回退出码 1
