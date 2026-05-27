#!/usr/bin/env python3
"""
platformbiz 模块 RBAC 权限管理脚本

使用方法:
    cd ~/repos/sage
    ./py3/bin/python ~/platformbiz/scripts/load_path.py

每次代码变更如有新 path 出现，需同步更新此脚本。
"""

import subprocess
import os
import sys

def find_sage_root():
    candidates = [
        os.path.expanduser("~/repos/sage"),
        os.path.expanduser("~/sage"),
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    ]
    for c in candidates:
        if os.path.isdir(os.path.join(c, "py3")) and os.path.isdir(os.path.join(c, "wwwroot")):
            return c
    return None

SAGE_ROOT = find_sage_root()
if not SAGE_ROOT:
    print("ERROR: Cannot find Sage root directory")
    sys.exit(1)

PYTHON = os.path.join(SAGE_ROOT, "py3", "bin", "python")
SET_PERM_SCRIPT = os.path.join(SAGE_ROOT, "set_role_perm.py")

MOD = "platformbiz"

# ============================================================
# 权限路径定义 — 每次新增页面或API时同步更新
# ============================================================

# any — 无需登录（菜单、登录页等）
PATHS_ANY = [
    f"/platformbiz/menu.ui",
    f"/platformbiz/owner.operator.menu.ui",
    f"/platformbiz/reseller.operator.menu.ui",]

# logined — 需要认证的页面和 API
PATHS_LOGINED = [
    f"/platformbiz",
    f"/platformbiz/add_provider.dspy",
    f"/platformbiz/add_provider.ui",
    f"/platformbiz/agree_prodclone.dspy",
    f"/platformbiz/agree_productauth.dspy",
    f"/platformbiz/agreedetail",
    f"/platformbiz/agreedetailstep",
    f"/platformbiz/agreement",
    f"/platformbiz/agreeproduct",
    f"/platformbiz/agreeproduct_auth.dspy",
    f"/platformbiz/biz_order",
    f"/platformbiz/choose_prodtype",
    f"/platformbiz/coupon",
    f"/platformbiz/coupon_log",
    f"/platformbiz/coupontype",
    f"/platformbiz/index.ui",
    f"/platformbiz/open_customer_accounts.dspy",
    f"/platformbiz/open_owner_accounts.dspy",
    f"/platformbiz/paychannel",
    f"/platformbiz/prodpricing",
    f"/platformbiz/prodpricingtab",
    f"/platformbiz/prodtype",
    f"/platformbiz/prodtypespec",
    f"/platformbiz/product",
    f"/platformbiz/product_query_price.dspy",
    f"/platformbiz/provide_agree",
    f"/platformbiz/provide_agreedetail",
    f"/platformbiz/provide_agreeproduct",
    f"/platformbiz/query_orders.dspy",
    f"/platformbiz/recgarge_log",
    f"/platformbiz/recharge.dspy",
    f"/platformbiz/recharge.ui",
    f"/platformbiz/resource",
    f"/platformbiz/retail_agree",]

# ============================================================
# 执行注册
# ============================================================

def run_set_perm(role, path):
    cmd = [PYTHON, SET_PERM_SCRIPT, role, path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def register_role_paths(role, paths):
    count = 0
    for p in paths:
        if run_set_perm(role, p):
            count += 1
    print(f"  {role}: {count}/{len(paths)} paths registered")
    return count

def main():
    print(f"Sage root: {SAGE_ROOT}")
    total = 0
    total += register_role_paths("any", PATHS_ANY)
    total += register_role_paths("logined", PATHS_LOGINED)
    print(f"\nDone. Total {total} permission entries registered.")
    print("NOTE: Restart Sage after permission changes to reload RBAC cache.")

if __name__ == "__main__":
    main()
