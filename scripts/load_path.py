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

    # 顶层 .dspy
    f"/{MOD}/add_provider.dspy",
    f"/{MOD}/agree_prodclone.dspy",
    f"/{MOD}/agree_productauth.dspy",
    f"/{MOD}/agreeproduct_auth.dspy",
    f"/{MOD}/open_customer_accounts.dspy",
    f"/{MOD}/open_owner_accounts.dspy",
    f"/{MOD}/product_query_price.dspy",
    f"/{MOD}/query_orders.dspy",
    f"/{MOD}/recharge.dspy",

    # CRUD 子目录 — agreedetail (alias: agreedetail)
    f"/{MOD}/agreedetail/index.ui",
    f"/{MOD}/agreedetail/get_agreedetail.dspy",
    f"/{MOD}/agreedetail/add_agreedetail.dspy",
    f"/{MOD}/agreedetail/update_agreedetail.dspy",
    f"/{MOD}/agreedetail/delete_agreedetail.dspy",

    # CRUD 子目录 — agreedetailstep (alias: agreedetailstep)
    f"/{MOD}/agreedetailstep/index.ui",
    f"/{MOD}/agreedetailstep/get_agreedetailstep.dspy",
    f"/{MOD}/agreedetailstep/add_agreedetailstep.dspy",
    f"/{MOD}/agreedetailstep/update_agreedetailstep.dspy",
    f"/{MOD}/agreedetailstep/delete_agreedetailstep.dspy",

    # CRUD 子目录 — agreement (alias: agreement)
    f"/{MOD}/agreement/index.ui",
    f"/{MOD}/agreement/get_agreement.dspy",
    f"/{MOD}/agreement/add_agreement.dspy",
    f"/{MOD}/agreement/update_agreement.dspy",
    f"/{MOD}/agreement/delete_agreement.dspy",

    # CRUD 子目录 — agreeproduct (alias: agreeproduct)
    f"/{MOD}/agreeproduct/index.ui",
    f"/{MOD}/agreeproduct/get_agreeproduct.dspy",
    f"/{MOD}/agreeproduct/add_agreeproduct.dspy",
    f"/{MOD}/agreeproduct/update_agreeproduct.dspy",
    f"/{MOD}/agreeproduct/delete_agreeproduct.dspy",

    # CRUD 子目录 — biz_order (alias: biz_order)
    f"/{MOD}/biz_order/index.ui",
    f"/{MOD}/biz_order/get_biz_order.dspy",
    f"/{MOD}/biz_order/add_biz_order.dspy",
    f"/{MOD}/biz_order/update_biz_order.dspy",
    f"/{MOD}/biz_order/delete_biz_order.dspy",

    # CRUD 子目录 — choose_prodtype (alias: choose_prodtype)
    f"/{MOD}/choose_prodtype/index.ui",
    f"/{MOD}/choose_prodtype/get_choose_prodtype.dspy",
    f"/{MOD}/choose_prodtype/add_choose_prodtype.dspy",
    f"/{MOD}/choose_prodtype/update_choose_prodtype.dspy",
    f"/{MOD}/choose_prodtype/delete_choose_prodtype.dspy",

    # CRUD 子目录 — coupon (alias: coupon)
    f"/{MOD}/coupon/index.ui",
    f"/{MOD}/coupon/get_coupon.dspy",
    f"/{MOD}/coupon/add_coupon.dspy",
    f"/{MOD}/coupon/update_coupon.dspy",
    f"/{MOD}/coupon/delete_coupon.dspy",

    # CRUD 子目录 — coupon_log (alias: coupon_log)
    f"/{MOD}/coupon_log/index.ui",
    f"/{MOD}/coupon_log/get_coupon_log.dspy",
    f"/{MOD}/coupon_log/add_coupon_log.dspy",
    f"/{MOD}/coupon_log/update_coupon_log.dspy",
    f"/{MOD}/coupon_log/delete_coupon_log.dspy",

    # CRUD 子目录 — coupontype (alias: coupontype)
    f"/{MOD}/coupontype/index.ui",
    f"/{MOD}/coupontype/get_coupontype.dspy",
    f"/{MOD}/coupontype/add_coupontype.dspy",
    f"/{MOD}/coupontype/update_coupontype.dspy",
    f"/{MOD}/coupontype/delete_coupontype.dspy",

    # CRUD 子目录 — paychannel (alias: paychannel)
    f"/{MOD}/paychannel/index.ui",
    f"/{MOD}/paychannel/get_paychannel.dspy",
    f"/{MOD}/paychannel/add_paychannel.dspy",
    f"/{MOD}/paychannel/update_paychannel.dspy",
    f"/{MOD}/paychannel/delete_paychannel.dspy",

    # CRUD 子目录 — prodpricing (alias: prodpricing)
    f"/{MOD}/prodpricing/index.ui",
    f"/{MOD}/prodpricing/get_prodpricing.dspy",
    f"/{MOD}/prodpricing/add_prodpricing.dspy",
    f"/{MOD}/prodpricing/update_prodpricing.dspy",
    f"/{MOD}/prodpricing/delete_prodpricing.dspy",

    # CRUD 子目录 — prodpricingtab (alias: prodpricingtab)
    f"/{MOD}/prodpricingtab/index.ui",
    f"/{MOD}/prodpricingtab/get_prodpricingtab.dspy",
    f"/{MOD}/prodpricingtab/add_prodpricingtab.dspy",
    f"/{MOD}/prodpricingtab/update_prodpricingtab.dspy",
    f"/{MOD}/prodpricingtab/delete_prodpricingtab.dspy",

    # CRUD 子目录 — prodtype (alias: prodtype)
    f"/{MOD}/prodtype/index.ui",
    f"/{MOD}/prodtype/get_prodtype.dspy",
    f"/{MOD}/prodtype/add_prodtype.dspy",
    f"/{MOD}/prodtype/update_prodtype.dspy",
    f"/{MOD}/prodtype/delete_prodtype.dspy",

    # CRUD 子目录 — prodtypespec (alias: prodtypespec)
    f"/{MOD}/prodtypespec/index.ui",
    f"/{MOD}/prodtypespec/get_prodtypespec.dspy",
    f"/{MOD}/prodtypespec/add_prodtypespec.dspy",
    f"/{MOD}/prodtypespec/update_prodtypespec.dspy",
    f"/{MOD}/prodtypespec/delete_prodtypespec.dspy",

    # CRUD 子目录 — product (alias: product)
    f"/{MOD}/product/index.ui",
    f"/{MOD}/product/get_product.dspy",
    f"/{MOD}/product/add_product.dspy",
    f"/{MOD}/product/update_product.dspy",
    f"/{MOD}/product/delete_product.dspy",

    # CRUD 子目录 — provide_agree (alias: provide_agree)
    f"/{MOD}/provide_agree/index.ui",
    f"/{MOD}/provide_agree/get_provide_agree.dspy",
    f"/{MOD}/provide_agree/add_provide_agree.dspy",
    f"/{MOD}/provide_agree/update_provide_agree.dspy",
    f"/{MOD}/provide_agree/delete_provide_agree.dspy",

    # CRUD 子目录 — provide_agreedetail (alias: provide_agreedetail)
    f"/{MOD}/provide_agreedetail/index.ui",
    f"/{MOD}/provide_agreedetail/get_provide_agreedetail.dspy",
    f"/{MOD}/provide_agreedetail/add_provide_agreedetail.dspy",
    f"/{MOD}/provide_agreedetail/update_provide_agreedetail.dspy",
    f"/{MOD}/provide_agreedetail/delete_provide_agreedetail.dspy",

    # CRUD 子目录 — provide_agreeproduct (alias: provide_agreeproduct)
    f"/{MOD}/provide_agreeproduct/index.ui",
    f"/{MOD}/provide_agreeproduct/get_provide_agreeproduct.dspy",
    f"/{MOD}/provide_agreeproduct/add_provide_agreeproduct.dspy",
    f"/{MOD}/provide_agreeproduct/update_provide_agreeproduct.dspy",
    f"/{MOD}/provide_agreeproduct/delete_provide_agreeproduct.dspy",

    # CRUD 子目录 — recgarge_log (alias: recgarge_log, json file: recgarge_log.json)
    f"/{MOD}/recgarge_log/index.ui",
    f"/{MOD}/recgarge_log/get_recgarge_log.dspy",
    f"/{MOD}/recgarge_log/add_recgarge_log.dspy",
    f"/{MOD}/recgarge_log/update_recgarge_log.dspy",
    f"/{MOD}/recgarge_log/delete_recgarge_log.dspy",

    # CRUD 子目录 — resource (alias: resource)
    f"/{MOD}/resource/index.ui",
    f"/{MOD}/resource/get_resource.dspy",
    f"/{MOD}/resource/add_resource.dspy",
    f"/{MOD}/resource/update_resource.dspy",
    f"/{MOD}/resource/delete_resource.dspy",

    # CRUD 子目录 — retail_agree (alias: retail_agree)
    f"/{MOD}/retail_agree/index.ui",
    f"/{MOD}/retail_agree/get_retail_agree.dspy",
    f"/{MOD}/retail_agree/add_retail_agree.dspy",
    f"/{MOD}/retail_agree/update_retail_agree.dspy",
    f"/{MOD}/retail_agree/delete_retail_agree.dspy",
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
