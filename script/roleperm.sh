#!/usr/bin/bash

python ~/py/rbac/script/roleperm.py sage platformbiz provider sale retail_agree agreedetail agreedetailstep agreeproduct organization
python ~/py/rbac/script/roleperm.py sage platformbiz provider sale product prodpricing prodpricingtab 
python ~/py/rbac/script/roleperm.py sage platformbiz reseller sale reseller retail_agree agreedetail agreedetailstep agreeproduct organization
python ~/py/rbac/script/roleperm.py sage platformbiz reseller operator provide_agree coupontype agreedetail agreedetailstep agreeproduct organization product prodpricing prodpricingtab coupontype coupon coupon_log recharge_log resource biz_order
python ~/py/rbac/script/roleperm.py sage platformbiz owner operator paychannel prodtype
python ~/py/rbac/script/roleperm.py sage platformbiz customer customer coupon coupon_log biz_order recharge_log resource
