"""
Parsing the Fact0rn project statistics of the ~/.factorn/debug.log
we create an histogram arround nBits as key and wOffset as a list
We operate with the wOffset list extracting it's statistics

messages like: 2026-04-30T14:18:40Z UpdateTip: new best=c0131e22a4856afdd9705a139da863e8f6d80435da64f896e29a531f1a3f6868 height=1 version=0x20000000 nBits=230 wOffset=-2672"
"""

import sys
import math
from statistics import *

def skew(data):
  m = mean(data)
  n = len(data)
  m3 = sum((x - m)**3 for x in data) / n
  m2 = sum((x - m)**2 for x in data) / n
  return m3 / (m2 ** 1.5)

def kurtosis(data):
  m = mean(data)
  n = len(data)
  m4 = sum((x - m)**4 for x in data) / n
  m2 = sum((x - m)**2 for x in data) / n
  return m4 / (m2 ** 2) - 3

def mad(data):
  m = mean(data)
  return mean([abs(x - m) for x in data])

def medad(data):
  med = median(data)
  return median([abs(x - med) for x in data])

def cv(data):
  m = mean(data)
  if m == 0:
    return 0.0
  return (stdev(data) / m) * 100

def stderr(data):
  return stdev(data) / math.sqrt(len(data))

histo = {}
for line in open(sys.argv[1],"r"):
  if "UpdateTip" in line:
    D = line.split()
    if len(D) > 7:
      bits = D[6].split("=")[1]
      wOffset = int(D[7].split("=")[1])
      if bits in histo:
        histo[bits].append(wOffset)
      else:
        histo[bits] = []

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
