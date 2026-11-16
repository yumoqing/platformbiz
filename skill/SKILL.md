---
name: platformbiz-repo
version: 1.0.0
description: platformbiz
trigger_conditions:
  - 需要理解、修改或排障 platformbiz 的代码
  - 在 platformbiz 里定位入口、数据表、对外契约或构建方式
---

# platformbiz 仓库技能

> 由仓库实际内容生成的骨架（README/目录/模型定义/契约/构建脚本逐项取证）。新增判断与坑位请直接在下面对应小节补充。

## 定位

**platformbiz**

* 记账模块[accounting](https://git.kaiyuancloud.cn/yumoqing/accounting) 在客户用户界面点击【成为商户】，系统自动将此平台客户添加商户角色，成为平台商户 并为其开通商户经营所需的记账账号。 与平台或平台其他商户（供应商）线下协商成为其产品的分销商 新添一个分销协议，在协议中添加协议明细，设置分销折扣，或阶梯折扣，将自己的产品授权给分销商销售。 为所有客户提供一个以产品计价为基础的折扣 卖房提供的产品 借：买方-

- 远端：`https://github.com/yumoqing/platformbiz.git`
- 默认分支：`feat/modern-ui-platformbiz`（共 30 个提交）
- 最近提交：2026-05-26 `8e8baba` fix: add filler css + overflowY:auto to content container
- 规模：98 个文件；JSON 41，Python 15，Shell 2

## 目录结构

- `models/` — 表定义（`models/*.json`，DDL/表结构唯一源）（40 个文件）
- `json/` — CRUD/界面定义（`json/*.json`：tblname+params）（22 个文件）
- `wwwroot/` — 前端页面与 `.dspy` 契约（服务端渲染入口）（15 个文件）
- `platformbiz/` — Python 包源码（模块本体）（10 个文件）
- `test/` — 测试（5 个文件）
- `docs/` — 文档（1 个文件）
- `script/` — 脚本（1 个文件）
- 根文件：`README.md`、`pyproject.toml`、`setup.cfg`、`tables.xlsx`

## 数据表（`models/*.json`，20 张）

- `agreedetail`（协议明细） — 6 字段、1 索引
- `agreedetailstep`（协议阶梯折扣） — 5 字段
- `agreement`（分销协议） — 13 字段
- `agreeproduct`（协议授权产品） — 4 字段
- `biz_order`（订单） — 11 字段
- `biz_orderdetail`（订单明细） — 7 字段
- `coupon`（优惠券） — 8 字段
- `coupon_log`（优惠券使用日志） — 9 字段
- `coupontype`（优惠券类型） — 10 字段
- `distributionagreement`（分销协议） — 6 字段
- `paychannel`（支付渠道） — 5 字段
- `pr_link`（供销链） — 6 字段
- `prodpricing`（产品计费） — 6 字段
- `prodpricingtab`（产品计费表） — 6 字段
- `prodtype`（产品类型） — 5 字段
- `prodtypespec`（产品类型规格） — 6 字段
- `product`（产品） — 11 字段
- `recharge_log`（充值日志） — 13 字段
- `reseller`（商户） — 7 字段
- `resource`（客户资源） — 11 字段

> 表结构只改 `models/*.json`，DDL 由它生成；不要手改库。

## CRUD 定义（`json/*.json`，21 个）

- 合规：`agreedetail.json`→agreedetail、`agreedetailstep.json`→agreedetailstep、`agreement.json`→agreement、`agreeproduct.json`→agreeproduct、`biz_order.json`→biz_order、`choose_prodtype.json`→prodtype、`coupon.json`→coupon、`coupon_log.json`→coupon_log、`coupontype.json`→coupontype、`paychannel.json`→paychannel、`prodpricing.json`→prodpricing、`prodpricingtab.json`→prodpricingtab、`prodtype.json`→prodtype、`prodtypespec.json`→prodtypespec、`product.json`→product、`provide_agree.json`→agreement、`provide_agreedetail.json`→agreedetail、`provide_agreeproduct.json`→agreeproduct、`recgarge_log.json`→recharge_log、`resource.json`→resource

## 对外契约（`.dspy`，9 个）

- `wwwroot/`：9 个 — add_provider.dspy、agree_prodclone.dspy、agree_productauth.dspy、agreeproduct_auth.dspy、open_customer_accounts.dspy、open_owner_accounts.dspy、…

## 注册入口

- `platformbiz/init.py` → `load_platformbiz()`

## 构建与运行

- `pyproject.toml`：`?` v?，依赖 0 项
- Python 包 `platformbiz/`：`__init__.py`、`biz.py`、`biz_order.py`、`const.py`、`getdbname.py`、`init.py`、`pb_acc.py`、`pricing.py`

## README 要点与注意（摘自 `README.md`）

- 章节：依赖、功能

## 建议阅读顺序

1. `README.md`
2. `docs/`
3. `models/`
4. `platformbiz/init.py`
5. `wwwroot/`

