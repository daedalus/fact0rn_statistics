"""
Parsing the Fact0rn project statistics of the ~/.factorn/debug.log
we create an histogram arround nBits as key and wOffset as a list
We operate with the wOffset list extracting it's statistics

messages like: 2026-04-30T14:18:40Z UpdateTip: new best=c0131e22a4856afdd9705a139da863e8f6d80435da64f896e29a531f1a3f6868 height=1 version=0x20000000 nBits=230 wOffset=-2672"
"""

import sys
from statistics import mean, median, mode, stdev
from lib.stats_lib import skew, kurtosis, mad, medad, cv, stderr, pvariance, variance
from lib.parser_lib import parse_debug_log

histo = parse_debug_log(sys.argv[1])
valid_rows = sum(len(v) for v in histo.values())
sys.stderr.write(f"Total valid rows {valid_rows}\n")


print("For each nBits calculate their wOffset stats:")
print("nBits count min median mean mode stdev skew kurtosis pvariance variance max mad cv medad stderr")
for bits in histo:
  h = histo[bits]
  print(bits, len(h), min(h), median(h), round(mean(h),2), mode(h), round(stdev(h),2), round(skew(h),2), round(kurtosis(h),2), round(pvariance(h),2), round(variance(h)), max(h), round(mad(h),2), round(cv(h),2), round(medad(h),2), round(stderr(h),2))


print("grouped nBits stats:")
print("min median mean mode stdev skew kurtosis pvariance variance max mad cv medad stderr")
h = []
for bits in histo:
  h += histo[bits]
print(min(h), median(h), round(mean(h),2), mode(h), round(stdev(h),2), round(skew(h),2), round(kurtosis(h),2), round(pvariance(h),2), round(variance(h)), max(h), round(mad(h),2), round(cv(h),2), round(medad(h),2), round(stderr(h),2))
