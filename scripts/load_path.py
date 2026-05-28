#!/usr/bin/env python3
"""
platformbiz 模块 RBAC 权限管理脚本

使用方法:
    cd ~/repos/sage
    ./py3/bin/python ~/repos/platformbiz/scripts/load_path.py
"""

import subprocess
import os
import sys


def find_sage_root():
    candidates = [
        os.path.expanduser("~/repos/sage"),
        os.path.expanduser("~/sage"),
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
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
# 权限路径定义
# ============================================================

# any — 无需登录
PATHS_ANY = [
    f"/{MOD}/menu.ui",
    f"/{MOD}/owner.operator.menu.ui",
    f"/{MOD}/reseller.operator.menu.ui",
]

# logined — 所有已登录用户
PATHS_LOGINED = [
    # 模块入口
    f"/{MOD}",
    f"/{MOD}/index.ui",

    # 顶层 .ui 页面
    f"/{MOD}/add_provider.ui",
    f"/{MOD}/recharge.ui",

    # 顶层 .dspy — 通配
    f"/{MOD}/%.dspy",

    # CRUD 子目录 — 通配
    f"/{MOD}/agreedetail/%",
    f"/{MOD}/agreedetailstep/%",
    f"/{MOD}/agreement/%",
    f"/{MOD}/agreeproduct/%",
    f"/{MOD}/biz_order/%",
    f"/{MOD}/choose_prodtype/%",
    f"/{MOD}/coupon/%",
    f"/{MOD}/coupon_log/%",
    f"/{MOD}/coupontype/%",
    f"/{MOD}/paychannel/%",
    f"/{MOD}/prodpricing/%",
    f"/{MOD}/prodpricingtab/%",
    f"/{MOD}/prodtype/%",
    f"/{MOD}/prodtypespec/%",
    f"/{MOD}/product/%",
    f"/{MOD}/provide_agree/%",
    f"/{MOD}/provide_agreedetail/%",
    f"/{MOD}/provide_agreeproduct/%",
    f"/{MOD}/recharge_log/%",
    f"/{MOD}/resource/%",
    f"/{MOD}/retail_agree/%",
]

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
