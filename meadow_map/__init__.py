"""
Python implementation of Meadow Map by Yintao, Xu

The method bases on Arkin, Ronald C.'s report "Path planning for a vision-based autonomous robot".

@inproceedings{arkin1987path,
  title={Path planning for a vision-based autonomous robot},
  author={Arkin, Ronald C},
  booktitle={Mobile Robots I},
  volume={727},
  pages={240--250},
  year={1987},
  organization={SPIE}
}
"""

from .convex_no_hole import convexify
from .convex_with_hole import merge_hole
